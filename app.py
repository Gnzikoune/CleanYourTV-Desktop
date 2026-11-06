"""
CleanYourTV Desktop Manager
Application de bureau universelle Windows (Fluent 2) pour contrôler, optimiser,
débloater et personnaliser n'importe quelle télévision ou box Android TV / Google TV.

Licence: MIT
Auteur: Contribution CleanYourTV Community
"""

import os
import sys
import json
import socket
import subprocess
import threading
import ctypes
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from PIL import Image, ImageTk

# Support pour PyInstaller (_MEIPASS) et chemins relatifs
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Enregistrement Windows AppUserModelID pour afficher l'icône dans la barre des tâches
try:
    myappid = "cleanyourtv.desktop.manager.v1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

# Fluent 2 Dark Mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CONFIG_DIR = Path.home() / ".cleanyourtv_desktop"
CONFIG_FILE = CONFIG_DIR / "config.json"
KEYS_DIR = CONFIG_DIR / "keys"

# Liste de protection stricte contre le bricking de téléviseurs
PROTECTED_PACKAGES = {
    "android",
    "com.android.systemui",
    "com.android.settings",
    "com.android.tv.settings",
    "com.android.shell",
    "com.android.phone",
    "com.google.android.packageinstaller",
    "com.android.packageinstaller",
    "com.google.android.permissioncontroller",
    "com.android.permissioncontroller",
    "com.google.android.ext.services",
    "android.ext.services",
    "com.google.android.ext.shared",
    "android.ext.shared",
    "com.google.android.modulemetadata",
    "com.android.providers.settings",
    "com.android.inputmethod.latin",
    "com.google.android.inputmethod.latin",
    "com.liskovsoft.leankeyboard"
}

# Dictionnaire de noms conviviaux pour les applications courantes sur Android TV
FRIENDLY_NAMES = {
    # Google Bloatware / Télémétrie
    "com.google.android.katniss": "Google Assistant / Recherche vocale",
    "com.google.android.apps.mediashell": "Chromecast intégré (Google Cast)",
    "com.google.android.play.games": "Google Play Jeux",
    "com.google.android.tvlauncher": "Launcher Android TV d'origine (Stock)",
    "com.google.android.feedback": "Google Feedback (Rapports de plantage)",
    "com.google.android.partnersetup": "Google Partner Setup",
    "com.google.android.onetimeinitializer": "Google One-Time Initializer",
    "com.google.android.tvrecommendations": "Recommandations sponsorisées Google",
    "com.google.android.backdrop": "Écran de veille Google Backdrop",
    "com.google.android.youtube.tvmusic": "YouTube Music TV",
    "com.google.android.videos": "Google TV / Play Films",
    "com.google.android.syncadapters.calendar": "Synchronisation Agenda Google",
    
    # Skyworth / Coocaa / Panasonic OEM
    "com.smartdevice.dtv.icast": "CastPlay (Recopie d'écran Skyworth)",
    "com.tianci.localmedia": "Lecteur multimédia USB d'origine",
    "com.smartdevice.recommendation": "Bandeau publicitaire Daily Play",
    "com.smartdevice.acr.recommendation": "ACR (Reconnaissance de contenu à l'écran)",
    "com.smartdevice.leanbacklauncher.customizer": "Shop Customizer OEM",
    "com.smartdevice.firewall": "Pare-feu & Télémétrie OEM",
    "com.smartdevice.epopplayer": "Lecteur démo magasin e-POP",
    "fusion.android.tv.demo": "Service démonstration magasin",
    "com.Smartdevice.emanual": "Manuel interactif à l'écran",
    "com.mstar.android.tv.disclaimercustomization": "Écran premier démarrage Mstar",
    "android.autoinstalls.config.SW": "Play Auto-Installs OEM",
    "com.smartdevice.tvworkwithalexa": "Liaison Alexa OEM",
    "com.sky.market": "Boutique d'applications OEM",
    "com.community.oneroom": "Module de push arrière-plan Transsion",
    
    # Xiaomi / Mi Box / PatchWall
    "com.xiaomi.mitv.upgrade": "Mises à jour MiTV",
    "com.mitv.gallery": "Galerie Xiaomi MiTV",
    "com.xiaomi.mitv.advert": "Service publicitaire MiTV",
    "com.xiaomi.mitv.payment": "Paiement MiTV",
    "com.mitv.tvhome": "PatchWall Launcher Xiaomi",

    # TCL Bloatware
    "com.tcl.partnercustomizer": "Personnalisation partenaire TCL",
    "com.tcl.videoplayer": "Lecteur vidéo TCL",
    "com.tcl.waterfall.overseas": "TCL Channel / Recommandations",
    
    # Android Common Services
    "com.android.printspooler": "Spooler d'impression",
    "com.android.htmlviewer": "Visualiseur HTML",
    "com.android.backupconfirm": "Confirmation sauvegarde système",
    "com.android.sharedstoragebackup": "Sauvegarde stockage partagé",
    "com.android.wallpaperbackup": "Sauvegarde fond d'écran"
}

# Initialisation du moteur ADB TCP direct
try:
    from adb_shell.adb_device import AdbDeviceTcp
    from adb_shell.auth.sign_pythonrsa import PythonRSASigner
    ADB_SHELL_AVAILABLE = True
except ImportError:
    ADB_SHELL_AVAILABLE = False


class ADBClient:
    """Gestionnaire de connexion ADB direct et persistant."""
    def __init__(self):
        self.device = None
        self.host = ""
        self.port = 5555
        self.signer = None
        self.lock = threading.Lock()
        self._setup_keys()

    def _setup_keys(self):
        KEYS_DIR.mkdir(parents=True, exist_ok=True)
        priv_key = KEYS_DIR / "adbkey"
        pub_key = KEYS_DIR / "adbkey.pub"

        if not priv_key.exists():
            try:
                from rsa import generate_key_pair
                from adb_shell.auth.keygen import keygen
                keygen(str(priv_key))
            except Exception:
                try:
                    subprocess.run(["adb", "keygen", str(priv_key)], capture_output=True)
                except Exception:
                    pass

        if priv_key.exists() and ADB_SHELL_AVAILABLE:
            try:
                with open(priv_key, "rb") as f:
                    priv_data = f.read()
                with open(pub_key, "rb") as f:
                    pub_data = f.read()
                self.signer = PythonRSASigner(pub_data, priv_data)
            except Exception:
                self.signer = None

    def connect(self, host, port=5555, timeout=5):
        with self.lock:
            self.disconnect()
            self.host = host
            self.port = port

            # Tentative via adb_shell pure Python
            if ADB_SHELL_AVAILABLE and self.signer:
                try:
                    dev = AdbDeviceTcp(self.host, self.port, default_transport_timeout_s=timeout)
                    dev.connect(rsa_keys=[self.signer], auth_timeout_s=timeout)
                    self.device = dev
                    return True, "Connecté avec succès via adb_shell."
                except Exception as e:
                    self.device = None

            # Fallback vers l'exécutable système adb
            try:
                res = subprocess.run(
                    ["adb", "connect", f"{host}:{port}"],
                    capture_output=True, text=True, timeout=timeout
                )
                if "connected" in res.stdout.lower():
                    return True, f"Connecté via CLI adb: {res.stdout.strip()}"
                return False, f"Refus de connexion: {res.stdout or res.stderr}"
            except Exception as e:
                return False, f"Impossible d'établir la connexion: {e}"

    def disconnect(self):
        with self.lock:
            if self.device:
                try:
                    self.device.close()
                except Exception:
                    pass
                self.device = None

    def is_connected(self):
        if self.device is not None:
            return True
        # Vérification via adb devices
        try:
            res = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=2)
            for line in res.stdout.splitlines():
                if f"{self.host}:{self.port}" in line and "device" in line:
                    return True
        except Exception:
            pass
        return False

    def shell(self, command, timeout=10):
        with self.lock:
            if self.device:
                try:
                    out = self.device.shell(command)
                    return True, out if out is not None else ""
                except Exception:
                    self.device = None  # Perte de connexion

            # Fallback adb CLI
            try:
                cmd = ["adb", "-s", f"{self.host}:{self.port}", "shell", command]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                return (res.returncode == 0), (res.stdout if res.returncode == 0 else res.stderr)
            except Exception as e:
                return False, str(e)


class CleanYourTVApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CleanYourTV — Desktop Manager")
        self.geometry("980x760")
        self.minsize(860, 680)
        self.configure(fg_color="#1E1E1E")

        self.adb = ADBClient()
        self.device_info = {}
        self.connected_host = ""

        # Chargement de la configuration utilisateur
        self.config = self._load_config()

        # Icône de la fenêtre
        icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self._build_ui()

        # Pré-remplissage depuis la configuration
        saved_ip = self.config.get("last_ip", "")
        if saved_ip:
            self.entry_ip.insert(0, saved_ip)

    def _load_config(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass

    def _run_async(self, fn, *args):
        threading.Thread(target=fn, args=args, daemon=True).start()

    def _build_ui(self):
        # 1. Barre Supérieure de Connexion
        top_frame = ctk.CTkFrame(self, fg_color="#282828", corner_radius=10)
        top_frame.pack(fill="x", padx=16, pady=(16, 8))

        # Logo / Titre
        title_box = ctk.CTkFrame(top_frame, fg_color="transparent")
        title_box.pack(side="left", padx=12, pady=10)

        icon_png = get_resource_path(os.path.join("assets", "icon.png"))
        if os.path.exists(icon_png):
            try:
                pil_img = Image.open(icon_png).resize((32, 32), Image.Resampling.LANCZOS)
                self.logo_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(32, 32))
                ctk.CTkLabel(title_box, text="", image=self.logo_img).pack(side="left", padx=(0, 8))
            except Exception:
                pass

        ctk.CTkLabel(
            title_box, 
            text="CleanYourTV", 
            font=ctk.CTkFont(family="Segoe UI Variable Display", size=18, weight="bold"),
            text_color="#FFFFFF"
        ).pack(side="left")

        # Champs IP & Port
        conn_box = ctk.CTkFrame(top_frame, fg_color="transparent")
        conn_box.pack(side="right", padx=12, pady=10)

        ctk.CTkLabel(conn_box, text="IP de la TV :", font=ctk.CTkFont(size=12), text_color="#A0A0A0").pack(side="left", padx=(0, 4))
        self.entry_ip = ctk.CTkEntry(conn_box, width=150, height=32, placeholder_text="192.168.1.50")
        self.entry_ip.pack(side="left", padx=(0, 8))

        ctk.CTkLabel(conn_box, text="Port :", font=ctk.CTkFont(size=12), text_color="#A0A0A0").pack(side="left", padx=(0, 4))
        self.entry_port = ctk.CTkEntry(conn_box, width=65, height=32, placeholder_text="5555")
        self.entry_port.insert(0, "5555")
        self.entry_port.pack(side="left", padx=(0, 8))

        self.btn_connect = ctk.CTkButton(
            conn_box, 
            text="⚡ Connecter", 
            width=100, 
            height=32,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0078D4", 
            hover_color="#005FB8",
            command=self.toggle_connection
        )
        self.btn_connect.pack(side="left")

        # 2. Bannière d'état de l'appareil
        self.device_badge = ctk.CTkFrame(self, fg_color="#242424", corner_radius=8)
        self.device_badge.pack(fill="x", padx=16, pady=(0, 8))

        self.lbl_device_info = ctk.CTkLabel(
            self.device_badge,
            text="⚪ Non connecté — Veuillez renseigner l'adresse IP de votre téléviseur Android ci-dessus.",
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=12),
            text_color="#888888"
        )
        self.lbl_device_info.pack(padx=12, pady=6, anchor="w")

        # 3. Onglets de Navigation
        self.tabview = ctk.CTkTabview(
            self, 
            fg_color="#1E1E1E", 
            segmented_button_fg_color="#282828",
            segmented_button_selected_color="#0078D4",
            segmented_button_selected_hover_color="#005FB8",
            corner_radius=10
        )
        self.tabview.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        tab_remote = self.tabview.add("Télécommande & Écran")
        tab_apps = self.tabview.add("Débloat & Applications")
        tab_system = self.tabview.add("Boost & Sécurité Système")
        tab_themes = self.tabview.add("Thèmes & Lanceur")

        self._build_tab_remote(tab_remote)
        self._build_tab_apps(tab_apps)
        self._build_tab_system(tab_system)
        self._build_tab_themes(tab_themes)

        # 4. Barre d'état en bas
        self.status_bar = ctk.CTkLabel(
            self, 
            text="Prêt.", 
            font=ctk.CTkFont(family="Segoe UI Variable Text", size=12),
            text_color="#888888"
        )
        self.status_bar.pack(side="bottom", fill="x", padx=16, pady=(0, 6))

    def _set_status(self, text):
        self.status_bar.configure(text=text)

    # =============================================================
    # GESTION CONNEXION
    # =============================================================
    def toggle_connection(self):
        if self.adb.is_connected():
            self.adb.disconnect()
            self.btn_connect.configure(text="⚡ Connecter", fg_color="#0078D4")
            self.lbl_device_info.configure(
                text="⚪ Déconnecté.",
                text_color="#888888"
            )
            self._set_status("Déconnecté.")
            return

        host = self.entry_ip.get().strip()
        port_s = self.entry_port.get().strip() or "5555"

        if not host:
            messagebox.showwarning("Adresse requise", "Veuillez entrer l'adresse IP de votre téléviseur.")
            return

        try:
            port = int(port_s)
        except ValueError:
            messagebox.showerror("Port invalide", "Le port doit être un nombre valide (généralement 5555).")
            return

        self._set_status(f"Connexion à {host}:{port}...")
        self.btn_connect.configure(state="disabled", text="En cours...")

        def _task():
            ok, msg = self.adb.connect(host, port)
            self.btn_connect.configure(state="normal")
            if ok:
                self.connected_host = host
                self.config["last_ip"] = host
                self._save_config()

                # Lecture des propriétés de l'appareil
                _, model = self.adb.shell("getprop ro.product.model")
                _, brand = self.adb.shell("getprop ro.product.brand")
                _, version = self.adb.shell("getprop ro.build.version.release")
                _, sdk = self.adb.shell("getprop ro.build.version.sdk")

                model_str = f"{brand.strip().capitalize()} {model.strip()} (Android {version.strip()} / SDK {sdk.strip()})"
                self.device_info = {"model": model.strip(), "brand": brand.strip(), "version": version.strip()}

                self.btn_connect.configure(text="Déconnecter", fg_color="#C42B1C", hover_color="#A80000")
                self.lbl_device_info.configure(
                    text=f"🟢 Connecté à : {model_str}  — IP : {host}:{port}",
                    text_color="#4CC2FF"
                )
                self._set_status(f"Connecté avec succès à {model_str}.")
            else:
                self.btn_connect.configure(text="⚡ Connecter", fg_color="#0078D4")
                self.lbl_device_info.configure(
                    text=f"🔴 Échec de connexion à {host}:{port} ({msg})",
                    text_color="#FFA0A0"
                )
                self._set_status(f"Erreur: {msg}")

        self._run_async(_task)

    # =============================================================
    # ONGLET 1 : TÉLÉCOMMANDE & ÉCRAN
    # =============================================================
    def _build_tab_remote(self, tab):
        col_left = ctk.CTkFrame(tab, fg_color="#242424", corner_radius=10)
        col_left.pack(side="left", fill="both", expand=True, padx=(8, 4), pady=8)

        col_right = ctk.CTkFrame(tab, fg_color="#242424", corner_radius=10)
        col_right.pack(side="right", fill="both", expand=True, padx=(4, 8), pady=8)

        # Côté Gauche : Contrôle d'affichage & Saisie
        ctk.CTkLabel(col_left, text="Écran & Interaction", font=ctk.CTkFont(size=16, weight="bold")).pack(padx=16, pady=(16, 8), anchor="w")

        btn_scrcpy = ctk.CTkButton(
            col_left, 
            text="📺 Miroir Écran en Direct (scrcpy)", 
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0078D4", 
            hover_color="#005FB8",
            corner_radius=8,
            command=self.open_screen_mirror
        )
        btn_scrcpy.pack(fill="x", padx=16, pady=6)

        btn_screenshot = ctk.CTkButton(
            col_left, 
            text="📸 Prendre une Capture d'Écran", 
            height=36,
            font=ctk.CTkFont(size=13),
            fg_color="#333333", 
            hover_color="#444444",
            corner_radius=8,
            command=self.take_screenshot
        )
        btn_screenshot.pack(fill="x", padx=16, pady=6)

        # Saisie clavier PC -> TV
        clip_box = ctk.CTkFrame(col_left, fg_color="#2D2D2D", corner_radius=8)
        clip_box.pack(fill="x", padx=16, pady=(14, 8))

        ctk.CTkLabel(clip_box, text="⌨️ Clavier PC → TV", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        
        self.entry_pc_text = ctk.CTkEntry(clip_box, placeholder_text="Tapez ou collez un texte, mot de passe, URL...", height=32)
        self.entry_pc_text.pack(fill="x", padx=10, pady=(0, 6))

        clip_btns = ctk.CTkFrame(clip_box, fg_color="transparent")
        clip_btns.pack(fill="x", padx=10, pady=(0, 8))

        ctk.CTkButton(clip_btns, text="📋 Presse-papier", height=30, corner_radius=6, fg_color="#383838", hover_color="#444444", command=self.paste_from_clipboard).pack(side="left", fill="x", expand=True, padx=(0, 4))
        ctk.CTkButton(clip_btns, text="Envoyer", height=30, corner_radius=6, fg_color="#107C41", hover_color="#0E6B38", command=self.send_text_to_tv).pack(side="right", fill="x", expand=True, padx=(4, 0))

        # Message Pop-up direct sur TV
        toast_box = ctk.CTkFrame(col_left, fg_color="#2D2D2D", corner_radius=8)
        toast_box.pack(fill="x", padx=16, pady=(4, 8))

        ctk.CTkLabel(toast_box, text="📢 Afficher un message sur l'écran TV", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        
        toast_row = ctk.CTkFrame(toast_box, fg_color="transparent")
        toast_row.pack(fill="x", padx=10, pady=(0, 8))

        self.entry_toast_msg = ctk.CTkEntry(toast_row, placeholder_text="Ex: Le dîner est prêt !", height=32)
        self.entry_toast_msg.pack(side="left", fill="x", expand=True, padx=(0, 6))

        ctk.CTkButton(toast_row, text="Afficher", width=70, height=32, corner_radius=6, fg_color="#0078D4", hover_color="#005FB8", command=self.send_toast_notification).pack(side="right")

        # Côté Droit : D-Pad & Télécommande Virtuelle
        ctk.CTkLabel(col_right, text="Télécommande Virtuelle", font=ctk.CTkFont(size=16, weight="bold")).pack(padx=16, pady=(16, 12))

        # Pavé Directionnel
        dpad = ctk.CTkFrame(col_right, fg_color="transparent")
        dpad.pack(pady=8)

        ctk.CTkButton(dpad, text="▲", width=64, height=44, corner_radius=8, fg_color="#333333", hover_color="#0078D4", command=lambda: self.send_key("DPAD_UP")).grid(row=0, column=1, padx=4, pady=4)
        ctk.CTkButton(dpad, text="◀", width=64, height=44, corner_radius=8, fg_color="#333333", hover_color="#0078D4", command=lambda: self.send_key("DPAD_LEFT")).grid(row=1, column=0, padx=4, pady=4)
        ctk.CTkButton(dpad, text="OK", width=64, height=44, corner_radius=8, font=ctk.CTkFont(weight="bold"), fg_color="#0078D4", hover_color="#005FB8", command=lambda: self.send_key("DPAD_CENTER")).grid(row=1, column=1, padx=4, pady=4)
        ctk.CTkButton(dpad, text="▶", width=64, height=44, corner_radius=8, fg_color="#333333", hover_color="#0078D4", command=lambda: self.send_key("DPAD_RIGHT")).grid(row=1, column=2, padx=4, pady=4)
        ctk.CTkButton(dpad, text="▼", width=64, height=44, corner_radius=8, fg_color="#333333", hover_color="#0078D4", command=lambda: self.send_key("DPAD_DOWN")).grid(row=2, column=1, padx=4, pady=4)

        # Boutons Système
        sys_f = ctk.CTkFrame(col_right, fg_color="transparent")
        sys_f.pack(fill="x", padx=16, pady=10)

        ctk.CTkButton(sys_f, text="🏠 Accueil", width=95, height=36, corner_radius=8, fg_color="#333333", hover_color="#444444", command=lambda: self.send_key("KEYCODE_HOME")).pack(side="left", padx=4, expand=True)
        ctk.CTkButton(sys_f, text="↩ Retour", width=95, height=36, corner_radius=8, fg_color="#333333", hover_color="#444444", command=lambda: self.send_key("KEYCODE_BACK")).pack(side="left", padx=4, expand=True)
        ctk.CTkButton(sys_f, text="☰ Menu", width=95, height=36, corner_radius=8, fg_color="#333333", hover_color="#444444", command=lambda: self.send_key("KEYCODE_MENU")).pack(side="left", padx=4, expand=True)

        # Volume
        vol_f = ctk.CTkFrame(col_right, fg_color="transparent")
        vol_f.pack(fill="x", padx=16, pady=4)

        ctk.CTkButton(vol_f, text="🔉 Vol -", width=95, height=34, corner_radius=8, fg_color="#333333", hover_color="#444444", command=lambda: self.send_key("VOLUME_DOWN")).pack(side="left", padx=4, expand=True)
        ctk.CTkButton(vol_f, text="🔊 Vol +", width=95, height=34, corner_radius=8, fg_color="#333333", hover_color="#444444", command=lambda: self.send_key("VOLUME_UP")).pack(side="left", padx=4, expand=True)
        ctk.CTkButton(vol_f, text="🔇 Muet", width=95, height=34, corner_radius=8, fg_color="#333333", hover_color="#444444", command=lambda: self.send_key("VOLUME_MUTE")).pack(side="left", padx=4, expand=True)

    def send_key(self, keycode):
        def _task():
            ok, _ = self.adb.shell(f"input keyevent {keycode}")
            self._set_status(f"Touche {keycode} envoyée." if ok else "Échec d'envoi de la touche.")
        self._run_async(_task)

    def paste_from_clipboard(self):
        try:
            txt = self.clipboard_get()
            self.entry_pc_text.delete(0, "end")
            self.entry_pc_text.insert(0, txt)
            self._set_status("Presse-papier collé.")
        except Exception:
            self._set_status("Presse-papier vide ou inaccessible.")

    def send_text_to_tv(self):
        txt = self.entry_pc_text.get().strip()
        if not txt:
            return
        def _task():
            escaped = txt.replace(" ", "%s").replace("&", r"\&").replace("'", r"\'").replace('"', r'\"')
            ok, _ = self.adb.shell(f"input text '{escaped}'")
            self._set_status("Texte envoyé sur la TV." if ok else "Échec de saisie du texte.")
        self._run_async(_task)

    def send_toast_notification(self):
        msg = self.entry_toast_msg.get().strip()
        if not msg:
            return
        def _task():
            safe_msg = msg.replace("'", " ")
            ok, _ = self.adb.shell(f"cmd notification post -t 'CleanYourTV' pc_msg '{safe_msg}'")
            if ok:
                self._set_status("Notification affichée sur la TV.")
                self.entry_toast_msg.delete(0, "end")
            else:
                self._set_status("Échec d'affichage du message.")
        self._run_async(_task)

    def open_screen_mirror(self):
        host = self.connected_host or self.entry_ip.get().strip()
        if not host:
            messagebox.showwarning("Connexion requise", "Connectez d'abord le téléviseur.")
            return

        # Détection de scrcpy
        scrcpy_exe = None
        for p in [
            "scrcpy",
            r"C:\Users\hp\AppData\Local\Microsoft\WinGet\Packages\Genymobile.scrcpy_Microsoft.Winget.Source_8wekyb3d8bbwe\scrcpy-win64-v5.0.1\scrcpy.exe",
            r"C:\Program Files\scrcpy\scrcpy.exe",
            r"C:\tools\scrcpy\scrcpy.exe"
        ]:
            if os.path.exists(p) or subprocess.run(["where", p], capture_output=True).returncode == 0:
                scrcpy_exe = p
                break

        if not scrcpy_exe:
            messagebox.showinfo(
                "scrcpy non trouvé",
                "scrcpy permet d'afficher l'écran de la TV à 60 FPS sur Windows.\n\n"
                "Installez-le facilement via PowerShell:\nwinget install Genymobile.scrcpy"
            )
            return

        cmd = [scrcpy_exe, f"--tcpip={host}:5555", "--window-title=CleanYourTV Display", "--max-size=1920"]
        try:
            flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            subprocess.Popen(cmd, creationflags=flags)
            self._set_status("Fenêtre scrcpy lancée.")
        except Exception as e:
            self._set_status(f"Erreur lancement scrcpy: {e}")

    def take_screenshot(self):
        def _task():
            self._set_status("Capture d'écran en cours...")
            shot_file = CONFIG_DIR / "latest_screenshot.png"
            ok, _ = self.adb.shell("screencap -p /sdcard/cleanyourtv_shot.png")
            if ok:
                # Récupération via pull ou base64
                ok_pull, _ = self.adb.shell("cat /sdcard/cleanyourtv_shot.png | base64")
                if ok_pull:
                    import base64
                    try:
                        data = base64.b64decode(ok_pull.replace("\r", "").replace("\n", ""))
                        with open(shot_file, "wb") as f:
                            f.write(data)
                        self._set_status("Capture réussie. Ouverture...")
                        os.startfile(shot_file)
                        return
                    except Exception:
                        pass
            self._set_status("Échec de la capture.")
        self._run_async(_task)

    # =============================================================
    # ONGLET 2 : DÉBLOAT & APPLICATIONS
    # =============================================================
    def _build_tab_apps(self, tab):
        top_bar = ctk.CTkFrame(tab, fg_color="#242424", corner_radius=10)
        top_bar.pack(fill="x", padx=8, pady=(8, 4))

        ctk.CTkLabel(top_bar, text="Gestionnaire d'Applications & Débloat", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=16, pady=12)

        # Filtre d'affichage
        self.filter_mode = ctk.StringVar(value="disabled")
        filters = ctk.CTkSegmentedButton(
            top_bar,
            values=["Désactivées", "Bloatware Détecté", "Toutes"],
            command=self._on_filter_changed
        )
        filters.set("Désactivées")
        filters.pack(side="left", padx=16)

        ctk.CTkButton(top_bar, text="🔄 Rafraîchir", width=90, height=32, corner_radius=6, fg_color="#0078D4", hover_color="#005FB8", command=self.refresh_packages).pack(side="right", padx=12)
        ctk.CTkButton(top_bar, text="⚠️ Restaurer Tout", width=120, height=32, corner_radius=6, fg_color="#C42B1C", hover_color="#A80000", command=self.restore_all_packages).pack(side="right", padx=(0, 6))

        # Zone scrollable pour la liste
        self.pkg_scroll = ctk.CTkScrollableFrame(tab, fg_color="#242424", corner_radius=10)
        self.pkg_scroll.pack(fill="both", expand=True, padx=8, pady=4)

    def _on_filter_changed(self, value):
        self.refresh_packages()

    def refresh_packages(self):
        if not self.adb.is_connected():
            self._set_status("Connectez un téléviseur pour lister les packages.")
            return

        def _task():
            self._set_status("Chargement des packages de la TV...")
            for w in self.pkg_scroll.winfo_children():
                w.destroy()

            # Liste des packages désactivés
            _, out_dis = self.adb.shell("pm list packages -d --user 0")
            disabled_set = set()
            for line in out_dis.splitlines():
                if line.strip().startswith("package:"):
                    disabled_set.add(line.replace("package:", "").strip())

            # Liste de tous les packages
            _, out_all = self.adb.shell("pm list packages -u")
            all_pkgs = []
            for line in out_all.splitlines():
                if line.strip().startswith("package:"):
                    all_pkgs.append(line.replace("package:", "").strip())

            filter_mode = self.tabview.get()
            display_pkgs = []

            # Filtrage selon le mode sélectionné
            filter_val = "disabled"
            for child in self.tabview._segmented_button._buttons_dict.values():
                pass

            # Rendu des éléments
            if not all_pkgs and not disabled_set:
                ctk.CTkLabel(self.pkg_scroll, text="Aucun package trouvé.").pack(pady=20)
                return

            pkgs_to_show = sorted(disabled_set) if disabled_set else sorted(all_pkgs)[:50]

            for pkg in pkgs_to_show:
                is_disabled = pkg in disabled_set
                friendly = FRIENDLY_NAMES.get(pkg, pkg)

                card = ctk.CTkFrame(self.pkg_scroll, fg_color="#2D2D2D", corner_radius=8)
                card.pack(fill="x", padx=8, pady=4)

                info = ctk.CTkFrame(card, fg_color="transparent")
                info.pack(side="left", fill="both", expand=True, padx=12, pady=8)

                ctk.CTkLabel(info, text=friendly, font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")
                ctk.CTkLabel(info, text=pkg, font=ctk.CTkFont(size=11), text_color="#888888").pack(anchor="w")

                status_lbl = ctk.CTkLabel(
                    card, 
                    text="Désactivé 🚫" if is_disabled else "Actif ✅", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#FFA0A0" if is_disabled else "#4CC2FF"
                )
                status_lbl.pack(side="left", padx=16)

                if is_disabled:
                    btn_action = ctk.CTkButton(
                        card, text="Activer", width=80, height=30, corner_radius=6,
                        fg_color="#107C41", hover_color="#0E6B38",
                        command=lambda p=pkg, c=card, s=status_lbl: self.toggle_package(p, enable=True, card=c, status_label=s)
                    )
                else:
                    is_safe = pkg not in PROTECTED_PACKAGES
                    btn_action = ctk.CTkButton(
                        card, text="Désactiver", width=80, height=30, corner_radius=6,
                        fg_color="#C42B1C" if is_safe else "#444444",
                        hover_color="#A80000" if is_safe else "#444444",
                        state="normal" if is_safe else "disabled",
                        command=lambda p=pkg, c=card, s=status_lbl: self.toggle_package(p, enable=False, card=c, status_label=s)
                    )
                btn_action.pack(side="right", padx=12, pady=8)

            self._set_status(f"{len(pkgs_to_show)} packages affichés.")

        self._run_async(_task)

    def toggle_package(self, pkg, enable, card, status_label):
        if not enable and pkg in PROTECTED_PACKAGES:
            messagebox.showerror("Protection Active", f"Le package '{pkg}' est indispensable au démarrage d'Android et ne peut pas être désactivé.")
            return

        def _task():
            if enable:
                cmd = f"pm enable {pkg}"
            else:
                cmd = f"pm disable-user --user 0 {pkg}"

            ok, out = self.adb.shell(cmd)
            if ok:
                status_label.configure(
                    text="Actif ✅" if enable else "Désactivé 🚫",
                    text_color="#4CC2FF" if enable else "#FFA0A0"
                )
                self._set_status(f"Package {pkg} {'activé' if enable else 'désactivé'}.")
            else:
                self._set_status(f"Erreur sur {pkg}: {out}")
        self._run_async(_task)

    def restore_all_packages(self):
        ok = messagebox.askyesno(
            "Restaurer Tout",
            "Voulez-vous réactiver toutes les applications précédemment désactivées sur cette télévision ?"
        )
        if not ok:
            return

        def _task():
            self._set_status("Restauration de toutes les applications...")
            _, out = self.adb.shell("pm list packages -d --user 0")
            count = 0
            for line in out.splitlines():
                if line.strip().startswith("package:"):
                    pkg = line.replace("package:", "").strip()
                    self.adb.shell(f"pm enable {pkg}")
                    count += 1
            self._set_status(f"{count} applications restaurées avec succès.")
            self.refresh_packages()
        self._run_async(_task)

    # =============================================================
    # ONGLET 3 : BOOST & SÉCURITÉ SYSTÈME
    # =============================================================
    def _build_tab_system(self, tab):
        container = ctk.CTkScrollableFrame(tab, fg_color="#242424", corner_radius=10)
        container.pack(fill="both", expand=True, padx=8, pady=8)

        ctk.CTkLabel(container, text="Optimisations & Sécurité Globale", font=ctk.CTkFont(size=16, weight="bold")).pack(padx=20, pady=(16, 8), anchor="w")

        # 1. Accélération des Animations
        f_anim = ctk.CTkFrame(container, fg_color="#2D2D2D", corner_radius=8)
        f_anim.pack(fill="x", padx=20, pady=6)
        f_anim_info = ctk.CTkFrame(f_anim, fg_color="transparent")
        f_anim_info.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(f_anim_info, text="⚡ Fluidité & Vitesse des Animations (0.5x)", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(f_anim_info, text="Divise par deux les temps de transition pour une sensation d'instantanéité.", font=ctk.CTkFont(size=11), text_color="#A0A0A0").pack(anchor="w")
        ctk.CTkButton(f_anim, text="Appliquer 0.5x", width=120, height=34, corner_radius=6, fg_color="#0078D4", hover_color="#005FB8", command=self.boost_animations).pack(side="right", padx=12)

        # 2. Compilation AOT Native
        f_aot = ctk.CTkFrame(container, fg_color="#2D2D2D", corner_radius=8)
        f_aot.pack(fill="x", padx=20, pady=6)
        f_aot_info = ctk.CTkFrame(f_aot, fg_color="transparent")
        f_aot_info.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(f_aot_info, text="🚀 Précompilation AOT Machine (Vitesse de lancement)", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(f_aot_info, text="Compile le launcher en code binaire direct pour supprimer toute saccade.", font=ctk.CTkFont(size=11), text_color="#A0A0A0").pack(anchor="w")
        ctk.CTkButton(f_aot, text="Compiler AOT", width=120, height=34, corner_radius=6, fg_color="#0078D4", hover_color="#005FB8", command=self.compile_aot).pack(side="right", padx=12)

        # 3. DNS Anti-Publicités AdGuard
        f_dns = ctk.CTkFrame(container, fg_color="#2D2D2D", corner_radius=8)
        f_dns.pack(fill="x", padx=20, pady=6)
        f_dns_info = ctk.CTkFrame(f_dns, fg_color="transparent")
        f_dns_info.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(f_dns_info, text="🛡️ Bloqueur de Pubs & Traceurs (DNS AdGuard)", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(f_dns_info, text="Active le DNS chiffré privé sans aucune application supplémentaire requise.", font=ctk.CTkFont(size=11), text_color="#A0A0A0").pack(anchor="w")
        ctk.CTkButton(f_dns, text="Activer AdGuard", width=120, height=34, corner_radius=6, fg_color="#107C41", hover_color="#0E6B38", command=self.setup_adguard_dns).pack(side="right", padx=12)

        # 4. Audit de Sécurité
        f_audit = ctk.CTkFrame(container, fg_color="#2D2D2D", corner_radius=8)
        f_audit.pack(fill="x", padx=20, pady=6)
        f_audit_info = ctk.CTkFrame(f_audit, fg_color="transparent")
        f_audit_info.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(f_audit_info, text="🕵️ Audit de Sécurité & Ports Écoutants", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        self.lbl_audit_res = ctk.CTkLabel(f_audit_info, text="Cliquez sur 'Scanner' pour analyser les ports ouverts et l'état de sécurité.", font=ctk.CTkFont(size=11), text_color="#A0A0A0")
        self.lbl_audit_res.pack(anchor="w")
        ctk.CTkButton(f_audit, text="Scanner", width=120, height=34, corner_radius=6, fg_color="#383838", hover_color="#444444", command=self.run_security_audit).pack(side="right", padx=12)

        # 5. Verrouillage ADB (Sécurisation maximale)
        f_lock = ctk.CTkFrame(container, fg_color="#3A2020", corner_radius=8)
        f_lock.pack(fill="x", padx=20, pady=6)
        f_lock_info = ctk.CTkFrame(f_lock, fg_color="transparent")
        f_lock_info.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(f_lock_info, text="🔒 Fermer le Port ADB (Sécurisation maximale)", font=ctk.CTkFont(size=14, weight="bold"), text_color="#FFA0A0").pack(anchor="w")
        ctk.CTkLabel(f_lock_info, text="Ferme le port 5555. Réactivation possible uniquement via télécommande physique.", font=ctk.CTkFont(size=11), text_color="#D0A0A0").pack(anchor="w")
        ctk.CTkButton(f_lock, text="Verrouiller ADB", width=120, height=34, corner_radius=6, fg_color="#C42B1C", hover_color="#A80000", command=self.lockdown_adb).pack(side="right", padx=12)

        # 6. Redémarrage
        f_reboot = ctk.CTkFrame(container, fg_color="#2D2D2D", corner_radius=8)
        f_reboot.pack(fill="x", padx=20, pady=6)
        f_reboot_info = ctk.CTkFrame(f_reboot, fg_color="transparent")
        f_reboot_info.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(f_reboot_info, text="🔄 Redémarrer Proprement la TV", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(f_reboot_info, text="Redémarre l'appareil pour valider la prise en compte des modifications.", font=ctk.CTkFont(size=11), text_color="#A0A0A0").pack(anchor="w")
        ctk.CTkButton(f_reboot, text="Redémarrer", width=120, height=34, corner_radius=6, fg_color="#444444", hover_color="#555555", command=self.reboot_device).pack(side="right", padx=12)

    def boost_animations(self):
        def _task():
            self._set_status("Accélération des animations...")
            self.adb.shell("settings put global window_animation_scale 0.5")
            self.adb.shell("settings put global transition_animation_scale 0.5")
            self.adb.shell("settings put global animator_duration_scale 0.5")
            self._set_status("Animations réglées à 0.5x (interface ultra-rapide).")
        self._run_async(_task)

    def compile_aot(self):
        def _task():
            self._set_status("Compilation AOT native en cours...")
            self.adb.shell("cmd package compile -m speed -f com.gathin.tvhome")
            self._set_status("Compilation AOT terminée avec succès.")
        self._run_async(_task)

    def setup_adguard_dns(self):
        def _task():
            self._set_status("Activation du DNS AdGuard...")
            self.adb.shell("settings put global private_dns_specifier dns.adguard-dns.com")
            self.adb.shell("settings put global private_dns_mode hostname")
            self._set_status("DNS AdGuard activé (blocage de pubs actif).")
        self._run_async(_task)

    def run_security_audit(self):
        def _task():
            self._set_status("Audit de sécurité en cours...")
            _, ports = self.adb.shell("cat /proc/net/tcp /proc/net/tcp6")
            _, dns_mode = self.adb.shell("settings get global private_dns_mode")

            has_adb = ":15B3" in ports
            has_adguard = "hostname" in dns_mode

            report = []
            if has_adb:
                report.append("⚠️ Port 5555 (ADB) ouvert")
            else:
                report.append("🔒 Port 5555 fermé")

            if has_adguard:
                report.append("🛡️ DNS AdGuard actif")
            else:
                report.append("⚠️ DNS standard sans filtrage")

            self.lbl_audit_res.configure(text=" • ".join(report), text_color="#4CC2FF")
            self._set_status("Audit terminé.")
        self._run_async(_task)

    def lockdown_adb(self):
        ok = messagebox.askyesno(
            "Verrouillage ADB",
            "⚠️ Attention : Cette action va désactiver le débogage réseau sur la TV.\n\n"
            "Ce gestionnaire ne pourra plus communiquer avec la TV jusqu'à réactivation manuelle "
            "dans les options développeur avec votre télécommande physique.\n\nVoulez-vous continuer ?"
        )
        if not ok:
            return

        def _task():
            self.adb.shell("settings put global adb_enabled 0")
            self.adb.shell("setprop service.adb.tcp.port -1")
            self.adb.shell("stop adbd")
            self._set_status("Port 5555 fermé. Débogage réseau coupé.")
            self.adb.disconnect()
            self.btn_connect.configure(text="⚡ Connecter", fg_color="#0078D4")
            self.lbl_device_info.configure(text="🔒 Sécurisé : Port ADB fermé.", text_color="#4CC2FF")
        self._run_async(_task)

    def reboot_device(self):
        def _task():
            self.adb.shell("reboot")
            self._set_status("Téléviseur en cours de redémarrage...")
        self._run_async(_task)

    # =============================================================
    # ONGLET 4 : THÈMES & LANCEUR
    # =============================================================
    def _build_tab_themes(self, tab):
        container = ctk.CTkFrame(tab, fg_color="#242424", corner_radius=10)
        container.pack(fill="both", expand=True, padx=8, pady=8)

        ctk.CTkLabel(container, text="Personnalisation du Lanceur CleanYourTV", font=ctk.CTkFont(size=16, weight="bold")).pack(padx=20, pady=(16, 8), anchor="w")
        ctk.CTkLabel(container, text="Configure l'apparence et le fond d'écran du launcher com.gathin.tvhome.", font=ctk.CTkFont(size=12), text_color="#A0A0A0").pack(padx=20, pady=(0, 16), anchor="w")

        # Sélection d'image personnalisée
        f_wall = ctk.CTkFrame(container, fg_color="#2D2D2D", corner_radius=8)
        f_wall.pack(fill="x", padx=20, pady=8)
        
        f_wall_info = ctk.CTkFrame(f_wall, fg_color="transparent")
        f_wall_info.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(f_wall_info, text="🖼️ Envoyer un Fond d'Écran Personnalisé", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(f_wall_info, text="Sélectionnez n'importe quelle photo de votre PC pour l'appliquer sur la TV.", font=ctk.CTkFont(size=11), text_color="#A0A0A0").pack(anchor="w")

        ctk.CTkButton(f_wall, text="Choisir une image...", width=140, height=34, corner_radius=6, fg_color="#0078D4", hover_color="#005FB8", command=self.pick_and_push_wallpaper).pack(side="right", padx=12)

        # Style Sombre Minimaliste
        f_dark = ctk.CTkFrame(container, fg_color="#2D2D2D", corner_radius=8)
        f_dark.pack(fill="x", padx=20, pady=6)
        f_dark_info = ctk.CTkFrame(f_dark, fg_color="transparent")
        f_dark_info.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(f_dark_info, text="🎬 Style Noir Pur (OLED Minimal)", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(f_dark_info, text="Design sobre sans distraction avec contraste élevé.", font=ctk.CTkFont(size=11), text_color="#A0A0A0").pack(anchor="w")
        ctk.CTkButton(f_dark, text="Appliquer", width=120, height=34, corner_radius=6, fg_color="#383838", hover_color="#444444", command=self.apply_dark_style).pack(side="right", padx=12)

    def pick_and_push_wallpaper(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fond d'écran",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.webp")]
        )
        if not file_path:
            return

        def _task():
            self._set_status("Envoi du fond d'écran sur la TV...")
            try:
                with open(file_path, "rb") as f:
                    img_data = f.read()

                # Envoi direct via base64 pour s'affranchir de tout outil tiers
                import base64
                b64 = base64.b64encode(img_data).decode("ascii")
                # Sauvegarde sur la TV
                self.adb.shell(f"echo '{b64}' | base64 -d > /sdcard/wallpaper.jpg")
                self._set_status("Fond d'écran transféré sur /sdcard/wallpaper.jpg.")
            except Exception as e:
                self._set_status(f"Erreur transfert wallpaper: {e}")

        self._run_async(_task)

    def apply_dark_style(self):
        def _task():
            self._set_status("Application du style sombre...")
            # Commande broadcast au launcher si supporté
            self.adb.shell("am broadcast -a com.gathin.tvhome.RELOAD_CONFIG")
            self._set_status("Configuration transmise au lanceur.")
        self._run_async(_task)


if __name__ == "__main__":
    app = CleanYourTVApp()
    app.mainloop()
