"""
Main Desktop Application Window (Microsoft Fluent 2 Design)
"""

import os
import threading
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image

from src.core.config import (
    COLOR_BG_MAIN, COLOR_BG_CARD, COLOR_ACCENT, COLOR_ACCENT_HOVER,
    COLOR_DANGER, COLOR_DANGER_HOVER, ConfigManager, get_resource_path
)
from src.infra.adb_client import AdbClient
from src.services.debloat_service import DebloatService
from src.services.system_service import SystemService
from src.services.screen_service import ScreenService
from src.ui.components.tab_remote import RemoteTab
from src.ui.components.tab_debloat import DebloatTab
from src.ui.components.tab_system import SystemTab
from src.ui.components.tab_themes import ThemesTab


class MainWindow(ctk.CTk):
    """Fluent 2 Desktop Application Window."""

    def __init__(self):
        super().__init__()

        self.title("CleanYourTV — Desktop Manager")
        self.geometry("980x760")
        self.minsize(860, 680)
        self.configure(fg_color=COLOR_BG_MAIN)

        # Core Services
        self.adb = AdbClient()
        self.debloat_service = DebloatService(self.adb)
        self.system_service = SystemService(self.adb)
        self.screen_service = ScreenService(self.adb)

        self.config = ConfigManager.load()
        self.connected_host = ""

        # Window Icon
        icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self._build_shell()
        self._load_saved_state()

    def run_async(self, fn, *args):
        """Execute background task without blocking UI thread."""
        threading.Thread(target=fn, args=args, daemon=True).start()

    def set_status(self, text: str):
        """Update bottom status bar message."""
        self.status_bar.configure(text=text)

    def _build_shell(self):
        # 1. Top Connection Bar
        top_frame = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=10)
        top_frame.pack(fill="x", padx=16, pady=(16, 8))

        # Title & Icon
        t_box = ctk.CTkFrame(top_frame, fg_color="transparent")
        t_box.pack(side="left", padx=12, pady=10)

        icon_png = get_resource_path(os.path.join("assets", "icon.png"))
        if os.path.exists(icon_png):
            try:
                pil_img = Image.open(icon_png).resize((32, 32), Image.Resampling.LANCZOS)
                self.logo_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(32, 32))
                ctk.CTkLabel(t_box, text="", image=self.logo_img).pack(side="left", padx=(0, 8))
            except Exception:
                pass

        ctk.CTkLabel(t_box, text="CleanYourTV", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        # IP & Connect Box
        conn_box = ctk.CTkFrame(top_frame, fg_color="transparent")
        conn_box.pack(side="right", padx=12, pady=10)

        ctk.CTkLabel(conn_box, text="IP TV :", font=ctk.CTkFont(size=12), text_color="#A0A0A0").pack(side="left", padx=(0, 4))
        self.entry_ip = ctk.CTkEntry(conn_box, width=150, height=32, placeholder_text="192.168.1.50")
        self.entry_ip.pack(side="left", padx=(0, 8))

        ctk.CTkLabel(conn_box, text="Port :", font=ctk.CTkFont(size=12), text_color="#A0A0A0").pack(side="left", padx=(0, 4))
        self.entry_port = ctk.CTkEntry(conn_box, width=65, height=32)
        self.entry_port.insert(0, "5555")
        self.entry_port.pack(side="left", padx=(0, 8))

        self.btn_connect = ctk.CTkButton(
            conn_box, text="⚡ Connecter", width=100, height=32,
            font=ctk.CTkFont(size=12, weight="bold"), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
            command=self._on_toggle_connect
        )
        self.btn_connect.pack(side="left")

        # 2. Hardware Info Banner
        self.device_badge = ctk.CTkFrame(self, fg_color="#242424", corner_radius=8)
        self.device_badge.pack(fill="x", padx=16, pady=(0, 8))
        self.lbl_device_info = ctk.CTkLabel(
            self.device_badge,
            text="⚪ Non connecté — Veuillez renseigner l'adresse IP de votre téléviseur Android ci-dessus.",
            font=ctk.CTkFont(size=12), text_color="#888888"
        )
        self.lbl_device_info.pack(padx=12, pady=6, anchor="w")

        # 3. Navigation Tabs
        self.tabview = ctk.CTkTabview(
            self, fg_color=COLOR_BG_MAIN, segmented_button_fg_color=COLOR_BG_CARD,
            segmented_button_selected_color=COLOR_ACCENT, segmented_button_selected_hover_color=COLOR_ACCENT_HOVER,
            corner_radius=10
        )
        self.tabview.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        tab_rem = self.tabview.add("Télécommande & Écran")
        tab_deb = self.tabview.add("Débloat & Applications")
        tab_sys = self.tabview.add("Boost & Sécurité Système")
        tab_thm = self.tabview.add("Thèmes & Lanceur")

        self.tab_remote = RemoteTab(tab_rem, self)
        self.tab_debloat = DebloatTab(tab_deb, self)
        self.tab_system = SystemTab(tab_sys, self)
        self.tab_themes = ThemesTab(tab_thm, self)

        # 4. Status Bar
        self.status_bar = ctk.CTkLabel(self, text="Prêt.", font=ctk.CTkFont(size=12), text_color="#888888")
        self.status_bar.pack(side="bottom", fill="x", padx=16, pady=(0, 6))

    def _load_saved_state(self):
        saved_ip = self.config.get("last_ip", "")
        if saved_ip:
            self.entry_ip.insert(0, saved_ip)

    def _on_toggle_connect(self):
        if self.adb.is_connected():
            self.adb.disconnect()
            self.on_disconnected()
            return

        host = self.entry_ip.get().strip()
        port_s = self.entry_port.get().strip() or "5555"
        if not host:
            messagebox.showwarning("Adresse requise", "Veuillez entrer l'adresse IP de votre téléviseur.")
            return

        try:
            port = int(port_s)
        except ValueError:
            messagebox.showerror("Port invalide", "Le port doit être un nombre valide.")
            return

        self.set_status(f"Connexion à {host}:{port}...")
        self.btn_connect.configure(state="disabled", text="En cours...")

        def _task():
            ok, msg = self.adb.connect(host, port)
            self.btn_connect.configure(state="normal")
            if ok:
                self.connected_host = host
                self.config["last_ip"] = host
                ConfigManager.save(self.config)

                props = self.adb.get_device_props()
                desc = f"{props['brand']} {props['model']} (Android {props['version']} / SDK {props['sdk']})"

                self.btn_connect.configure(text="Déconnecter", fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER)
                self.lbl_device_info.configure(text=f"🟢 Connecté à : {desc} — IP : {host}:{port}", text_color="#4CC2FF")
                self.set_status(f"Connecté avec succès à {desc}.")
                self.tab_debloat.refresh_list()
            else:
                self.btn_connect.configure(text="⚡ Connecter", fg_color=COLOR_ACCENT)
                self.lbl_device_info.configure(text=f"🔴 Échec de connexion : {msg}", text_color="#FFA0A0")
                self.set_status(f"Erreur: {msg}")

        self.run_async(_task)

    def on_disconnected(self):
        """Reset connection UI controls."""
        self.btn_connect.configure(text="⚡ Connecter", fg_color=COLOR_ACCENT)
        self.lbl_device_info.configure(text="⚪ Déconnecté.", text_color="#888888")
        self.set_status("Déconnecté.")
