"""
Tab 1: Virtual Remote, Live Mirroring & PC-to-TV Typing
"""

import os
from typing import TYPE_CHECKING, Any
import customtkinter as ctk
from src.core.config import COLOR_BG_CARD, COLOR_BG_SUB, COLOR_ACCENT, COLOR_ACCENT_HOVER

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow


class RemoteTab:
    """Component for Virtual Remote, scrcpy, and PC->TV typing."""

    def __init__(self, parent: Any, app: "MainWindow") -> None:
        self.parent = parent
        self.app = app
        self._build_ui()

    def _build_ui(self) -> None:
        col_left = ctk.CTkFrame(self.parent, fg_color=COLOR_BG_CARD, corner_radius=10)
        col_left.pack(side="left", fill="both", expand=True, padx=(8, 4), pady=8)

        col_right = ctk.CTkFrame(self.parent, fg_color=COLOR_BG_CARD, corner_radius=10)
        col_right.pack(side="right", fill="both", expand=True, padx=(4, 8), pady=8)

        # Left Column: Screen & Typing
        ctk.CTkLabel(
            col_left, text="Écran & Interaction",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=16, pady=(16, 8), anchor="w")

        btn_scrcpy = ctk.CTkButton(
            col_left, text="📺 Miroir Écran en Direct (scrcpy)", height=40,
            font=ctk.CTkFont(size=13, weight="bold"), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
            corner_radius=8, command=self._on_launch_mirror
        )
        btn_scrcpy.pack(fill="x", padx=16, pady=(6, 2))

        self.switch_low_power = ctk.CTkSwitch(
            col_left, text="Profil Fluide TV (720p 30 FPS anti-saccades)",
            font=ctk.CTkFont(size=11), onvalue=True, offvalue=False
        )
        self.switch_low_power.select()
        self.switch_low_power.pack(fill="x", padx=18, pady=(0, 4))

        btn_shot = ctk.CTkButton(
            col_left, text="📸 Prendre une Capture d'Écran", height=32,
            font=ctk.CTkFont(size=12), fg_color="#333333", hover_color="#444444",
            corner_radius=8, command=self._on_take_screenshot
        )
        btn_shot.pack(fill="x", padx=16, pady=4)

        # Audio Streaming Box (Simultaneous TV + PC playback over LAN & Tailscale)
        audio_box = ctk.CTkFrame(col_left, fg_color=COLOR_BG_SUB, corner_radius=8)
        audio_box.pack(fill="x", padx=16, pady=(6, 6))
        ctk.CTkLabel(
            audio_box, text="🔊 Audio TV ➔ PC (Local & Tailscale)",
            font=ctk.CTkFont(size=11, weight="bold")
        ).pack(anchor="w", padx=10, pady=(6, 2))

        a_row = ctk.CTkFrame(audio_box, fg_color="transparent")
        a_row.pack(fill="x", padx=10, pady=(2, 6))
        ctk.CTkButton(
            a_row, text="▶ Écouter sur PC", height=28, corner_radius=6,
            fg_color="#005FB8", hover_color="#004A94", font=ctk.CTkFont(size=11),
            command=self._on_listen_audio
        ).pack(side="left", fill="x", expand=True, padx=(0, 3))
        ctk.CTkButton(
            a_row, text="📱 Ouvrir sur TV", height=28, corner_radius=6,
            fg_color="#383838", hover_color="#444444", font=ctk.CTkFont(size=11),
            command=self._on_setup_tv_audio
        ).pack(side="right", fill="x", expand=True, padx=(3, 0))

        # Clipboard Box
        clip_box = ctk.CTkFrame(col_left, fg_color=COLOR_BG_SUB, corner_radius=8)
        clip_box.pack(fill="x", padx=16, pady=(14, 8))
        ctk.CTkLabel(
            clip_box, text="⌨️ Clavier PC → TV",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=10, pady=(8, 4))

        self.entry_text = ctk.CTkEntry(
            clip_box, placeholder_text="Tapez ou collez un texte, mot de passe...", height=32
        )
        self.entry_text.pack(fill="x", padx=10, pady=(0, 6))

        c_row = ctk.CTkFrame(clip_box, fg_color="transparent")
        c_row.pack(fill="x", padx=10, pady=(0, 8))
        ctk.CTkButton(
            c_row, text="📋 Presse-papier", height=30, corner_radius=6,
            fg_color="#383838", hover_color="#444444", command=self._on_paste
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))
        ctk.CTkButton(
            c_row, text="Envoyer", height=30, corner_radius=6,
            fg_color="#107C41", hover_color="#0E6B38", command=self._on_send_text
        ).pack(side="right", fill="x", expand=True, padx=(4, 0))

        # Toast Message Box
        toast_box = ctk.CTkFrame(col_left, fg_color=COLOR_BG_SUB, corner_radius=8)
        toast_box.pack(fill="x", padx=16, pady=(4, 8))
        ctk.CTkLabel(
            toast_box, text="📢 Afficher un message sur l'écran TV",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=10, pady=(8, 4))

        t_row = ctk.CTkFrame(toast_box, fg_color="transparent")
        t_row.pack(fill="x", padx=10, pady=(0, 8))
        self.entry_toast = ctk.CTkEntry(t_row, placeholder_text="Ex: Le dîner est prêt !", height=32)
        self.entry_toast.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkButton(
            t_row, text="Afficher", width=70, height=32, corner_radius=6,
            fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, command=self._on_send_toast
        ).pack(side="right")

        # Right Column: Virtual D-Pad Remote
        ctk.CTkLabel(col_right, text="Télécommande Virtuelle", font=ctk.CTkFont(size=16, weight="bold")).pack(padx=16, pady=(16, 12))

        dpad = ctk.CTkFrame(col_right, fg_color="transparent")
        dpad.pack(pady=8)
        ctk.CTkButton(dpad, text="▲", width=64, height=44, corner_radius=8, fg_color="#333333", hover_color=COLOR_ACCENT, command=lambda: self._send_key("DPAD_UP")).grid(row=0, column=1, padx=4, pady=4)
        ctk.CTkButton(dpad, text="◀", width=64, height=44, corner_radius=8, fg_color="#333333", hover_color=COLOR_ACCENT, command=lambda: self._send_key("DPAD_LEFT")).grid(row=1, column=0, padx=4, pady=4)
        ctk.CTkButton(dpad, text="OK", width=64, height=44, corner_radius=8, font=ctk.CTkFont(weight="bold"), fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, command=lambda: self._send_key("DPAD_CENTER")).grid(row=1, column=1, padx=4, pady=4)
        ctk.CTkButton(dpad, text="▶", width=64, height=44, corner_radius=8, fg_color="#333333", hover_color=COLOR_ACCENT, command=lambda: self._send_key("DPAD_RIGHT")).grid(row=1, column=2, padx=4, pady=4)
        ctk.CTkButton(dpad, text="▼", width=64, height=44, corner_radius=8, fg_color="#333333", hover_color=COLOR_ACCENT, command=lambda: self._send_key("DPAD_DOWN")).grid(row=2, column=1, padx=4, pady=4)

        # Nav & Volume
        sys_f = ctk.CTkFrame(col_right, fg_color="transparent")
        sys_f.pack(fill="x", padx=16, pady=10)
        ctk.CTkButton(sys_f, text="🏠 Accueil", width=95, height=36, corner_radius=8, fg_color="#333333", hover_color="#444444", command=lambda: self._send_key("KEYCODE_HOME")).pack(side="left", padx=4, expand=True)
        ctk.CTkButton(sys_f, text="↩ Retour", width=95, height=36, corner_radius=8, fg_color="#333333", hover_color="#444444", command=lambda: self._send_key("KEYCODE_BACK")).pack(side="left", padx=4, expand=True)
        ctk.CTkButton(sys_f, text="☰ Menu", width=95, height=36, corner_radius=8, fg_color="#333333", hover_color="#444444", command=lambda: self._send_key("KEYCODE_MENU")).pack(side="left", padx=4, expand=True)

        vol_f = ctk.CTkFrame(col_right, fg_color="transparent")
        vol_f.pack(fill="x", padx=16, pady=4)
        ctk.CTkButton(vol_f, text="🔉 Vol -", width=95, height=34, corner_radius=8, fg_color="#333333", hover_color="#444444", command=lambda: self._send_key("VOLUME_DOWN")).pack(side="left", padx=4, expand=True)
        ctk.CTkButton(vol_f, text="🔊 Vol +", width=95, height=34, corner_radius=8, fg_color="#333333", hover_color="#444444", command=lambda: self._send_key("VOLUME_UP")).pack(side="left", padx=4, expand=True)
        ctk.CTkButton(vol_f, text="🔇 Muet", width=95, height=34, corner_radius=8, fg_color="#333333", hover_color="#444444", command=lambda: self._send_key("VOLUME_MUTE")).pack(side="left", padx=4, expand=True)

    def _send_key(self, keycode: str) -> None:
        self.app.run_async(lambda: self.app.adb.shell(f"input keyevent {keycode}"))

    def _on_paste(self) -> None:
        try:
            txt = self.app.clipboard_get()
            self.entry_text.delete(0, "end")
            self.entry_text.insert(0, txt)
        except Exception:
            pass

    def _on_send_text(self) -> None:
        txt = self.entry_text.get().strip()
        if not txt:
            return
        def _task() -> None:
            esc = txt.replace(" ", "%s").replace("&", r"\&").replace("'", r"\'").replace('"', r'\"')
            self.app.adb.shell(f"input text '{esc}'")
            self.app.set_status("Texte envoyé sur la TV.")
        self.app.run_async(_task)

    def _on_send_toast(self) -> None:
        msg = self.entry_toast.get().strip()
        if not msg:
            return
        def _task() -> None:
            safe = msg.replace("'", " ")
            self.app.adb.shell(f"cmd notification post -t 'CleanYourTV' pc_msg '{safe}'")
            self.app.set_status("Message affiché sur l'écran.")
            self.app.after(0, lambda: self.entry_toast.delete(0, "end"))
        self.app.run_async(_task)

    def _on_launch_mirror(self) -> None:
        host = self.app.connected_host or self.app.entry_ip.get().strip()
        low_p = bool(self.switch_low_power.get())
        ok, msg = self.app.screen_service.start_mirroring(host, low_power=low_p)
        self.app.set_status(msg)

    def _on_listen_audio(self) -> None:
        host = self.app.connected_host or self.app.entry_ip.get().strip()
        ok, msg = self.app.audio_service.launch_pc_client(host)
        self.app.set_status(msg)

    def _on_setup_tv_audio(self) -> None:
        def _task() -> None:
            installed, _ = self.app.audio_service.is_tv_agent_installed()
            ok, msg = self.app.audio_service.start_tv_agent() if installed else self.app.audio_service.open_playstore_on_tv()
            self.app.set_status(msg)
        self.app.run_async(_task)

    def _on_take_screenshot(self) -> None:
        def _task() -> None:
            self.app.set_status("Capture d'écran en cours...")
            ok, msg, path = self.app.screen_service.capture_screenshot()
            self.app.set_status(msg)
            if ok and path and hasattr(os, "startfile"):
                getattr(os, "startfile")(path)
        self.app.run_async(_task)
