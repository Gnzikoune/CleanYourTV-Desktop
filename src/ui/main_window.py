"""
Main Desktop Application Window (Microsoft Fluent 2 Design)
"""

import os
import threading
from tkinter import messagebox
from typing import Any, Callable
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
from src.services.network_scanner import NetworkScannerService
from src.services.update_checker import UpdateCheckerService
from src.ui.components.tab_remote import RemoteTab
from src.ui.components.tab_debloat import DebloatTab
from src.ui.components.tab_system import SystemTab
from src.ui.components.tab_themes import ThemesTab
from src.ui.components.update_banner import UpdateBanner


class MainWindow(ctk.CTk):
    """Fluent 2 Desktop Application Window."""

    def __init__(self) -> None:
        super().__init__()

        self.title("CleanYourTV — Desktop Manager")
        self.geometry("1020x780")
        self.minsize(880, 680)
        self.configure(fg_color=COLOR_BG_MAIN)

        # Core Services
        self.adb = AdbClient()
        self.debloat_service = DebloatService(self.adb)
        self.system_service = SystemService(self.adb)
        self.screen_service = ScreenService(self.adb)

        self.config = ConfigManager.load()
        self.connected_host: str = ""

        # Window Icon
        icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self._build_shell()
        self._load_saved_state()
        self._check_for_updates_async()

    def run_async(self, fn: Callable[..., Any], *args: Any) -> None:
        """Execute background task without blocking UI thread."""
        threading.Thread(target=fn, args=args, daemon=True).start()

    def set_status(self, text: str) -> None:
        """Update bottom status bar message (thread-safe)."""
        self.after(0, lambda: self.status_bar.configure(text=text))

    def _build_shell(self) -> None:
        # 1. Top Connection Bar
        top_frame = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=10)
        top_frame.pack(fill="x", padx=16, pady=(16, 8))

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

        self.btn_scan = ctk.CTkButton(
            conn_box, text="🔍 Scan Réseau", width=110, height=32,
            font=ctk.CTkFont(size=11, weight="bold"), fg_color="#333333", hover_color="#444444",
            command=self._on_scan_network
        )
        self.btn_scan.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(conn_box, text="IP :", font=ctk.CTkFont(size=12), text_color="#A0A0A0").pack(side="left", padx=(0, 4))
        self.entry_ip = ctk.CTkEntry(conn_box, width=140, height=32, placeholder_text="192.168.1.50")
        self.entry_ip.pack(side="left", padx=(0, 8))

        ctk.CTkLabel(conn_box, text="Port :", font=ctk.CTkFont(size=12), text_color="#A0A0A0").pack(side="left", padx=(0, 4))
        self.entry_port = ctk.CTkEntry(conn_box, width=60, height=32)
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
            text="⚪ Non connecté — Renseignez l'IP ci-dessus ou cliquez sur 'Scan Réseau'.",
            font=ctk.CTkFont(size=12), text_color="#888888"
        )
        self.lbl_device_info.pack(padx=12, pady=6, anchor="w")

        # Container for Update Banner (if available)
        self.update_container = ctk.CTkFrame(self, fg_color="transparent")
        self.update_container.pack(fill="x", padx=16, pady=(0, 8))

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

    def _load_saved_state(self) -> None:
        saved_ip = self.config.get("last_ip", "")
        if saved_ip:
            self.entry_ip.insert(0, saved_ip)

    def _check_for_updates_async(self) -> None:
        def _task() -> None:
            has_update, tag, dl_url, _ = UpdateCheckerService.check_for_updates()
            if has_update and dl_url:
                def _show_banner() -> None:
                    banner = UpdateBanner(self.update_container, self, tag, dl_url)
                    banner.pack(fill="x")
                self.after(0, _show_banner)
        self.run_async(_task)

    def _on_scan_network(self) -> None:
        self.set_status("Scan réseau local en cours (recherche des ports ADB 5555)...")
        self.btn_scan.configure(state="disabled", text="Scan...")

        def _task() -> None:
            devices = NetworkScannerService.scan_subnet()
            def _apply() -> None:
                self.btn_scan.configure(state="normal", text="🔍 Scan Réseau")
                if devices:
                    first_ip = devices[0][0]
                    self.entry_ip.delete(0, "end")
                    self.entry_ip.insert(0, first_ip)
                    msg = f"🟢 {len(devices)} appareil(s) ADB trouvé(s) ! IP pré-remplie : {first_ip}"
                    self.set_status(msg)
                    self.lbl_device_info.configure(text=msg, text_color="#4CC2FF")
                else:
                    self.set_status("Aucun appareil ADB détecté sur le sous-réseau local.")
                    messagebox.showinfo("Scan Réseau", "Aucun téléviseur avec le port 5555 actif n'a été détecté.\nVérifiez que la TV est allumée et sur le même Wi-Fi.")
            self.after(0, _apply)
        self.run_async(_task)

    def _on_toggle_connect(self) -> None:
        if self.adb.is_connected():
            self.adb.disconnect()
            self.on_disconnected()
            return

        host = self.entry_ip.get().strip()
        port_s = self.entry_port.get().strip() or "5555"
        if not host:
            messagebox.showwarning("Adresse requise", "Veuillez entrer l'IP ou lancer un Scan Réseau.")
            return

        try:
            port = int(port_s)
        except ValueError:
            messagebox.showerror("Port invalide", "Le port doit être un nombre valide.")
            return

        self.set_status(f"Connexion à {host}:{port}...")
        self.btn_connect.configure(state="disabled", text="En cours...")

        def _task() -> None:
            ok, msg = self.adb.connect(host, port)
            def _apply_ui() -> None:
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
            self.after(0, _apply_ui)
        self.run_async(_task)

    def on_disconnected(self) -> None:
        """Reset connection UI controls."""
        self.btn_connect.configure(text="⚡ Connecter", fg_color=COLOR_ACCENT)
        self.lbl_device_info.configure(text="⚪ Déconnecté.", text_color="#888888")
        self.set_status("Déconnecté.")
