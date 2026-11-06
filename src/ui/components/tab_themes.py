"""
Tab 4: Launcher Customization & Wallpapers
"""

from tkinter import filedialog
from typing import TYPE_CHECKING, Any
import customtkinter as ctk
from src.core.config import COLOR_BG_CARD, COLOR_BG_SUB, COLOR_ACCENT, COLOR_ACCENT_HOVER

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow


class ThemesTab:
    """Component for wallpaper streaming and visual styling."""

    def __init__(self, parent: Any, app: "MainWindow") -> None:
        self.parent = parent
        self.app = app
        self._build_ui()

    def _build_ui(self) -> None:
        container = ctk.CTkFrame(self.parent, fg_color=COLOR_BG_CARD, corner_radius=10)
        container.pack(fill="both", expand=True, padx=8, pady=8)

        ctk.CTkLabel(
            container, text="Personnalisation du Lanceur CleanYourTV",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=20, pady=(16, 8), anchor="w")
        ctk.CTkLabel(
            container,
            text="Configure l'apparence et le fond d'écran du launcher com.gathin.tvhome.",
            font=ctk.CTkFont(size=12), text_color="#A0A0A0"
        ).pack(padx=20, pady=(0, 16), anchor="w")

        # Custom Wallpaper
        f_wall = ctk.CTkFrame(container, fg_color=COLOR_BG_SUB, corner_radius=8)
        f_wall.pack(fill="x", padx=20, pady=8)
        info_wall = ctk.CTkFrame(f_wall, fg_color="transparent")
        info_wall.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(
            info_wall, text="🖼️ Envoyer un Fond d'Écran Personnalisé",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        ctk.CTkLabel(
            info_wall,
            text="Sélectionnez n'importe quelle photo de votre PC pour l'appliquer sur la TV.",
            font=ctk.CTkFont(size=11), text_color="#A0A0A0"
        ).pack(anchor="w")
        ctk.CTkButton(
            f_wall, text="Choisir une image...", width=140, height=34, corner_radius=6,
            fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, command=self._on_pick_wallpaper
        ).pack(side="right", padx=12)

        # OLED Dark Minimal
        f_dark = ctk.CTkFrame(container, fg_color=COLOR_BG_SUB, corner_radius=8)
        f_dark.pack(fill="x", padx=20, pady=6)
        info_dark = ctk.CTkFrame(f_dark, fg_color="transparent")
        info_dark.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(
            info_dark, text="🎬 Style Noir Pur (OLED Minimal)",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        ctk.CTkLabel(
            info_dark, text="Design sobre sans distraction avec contraste élevé.",
            font=ctk.CTkFont(size=11), text_color="#A0A0A0"
        ).pack(anchor="w")
        ctk.CTkButton(
            f_dark, text="Appliquer", width=120, height=34, corner_radius=6,
            fg_color="#383838", hover_color="#444444", command=self._on_apply_dark
        ).pack(side="right", padx=12)

    def _on_pick_wallpaper(self) -> None:
        path = filedialog.askopenfilename(
            title="Sélectionner un fond d'écran",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.webp")]
        )
        if not path:
            return

        def _task() -> None:
            self.app.set_status("Envoi du fond d'écran sur la TV...")
            ok, msg = self.app.screen_service.push_wallpaper(path)
            self.app.set_status(msg)
        self.app.run_async(_task)

    def _on_apply_dark(self) -> None:
        def _task() -> None:
            self.app.set_status("Application du style sombre...")
            self.app.adb.shell("am broadcast -a com.gathin.tvhome.RELOAD_CONFIG")
            self.app.set_status("Signal de rechargement envoyé au lanceur.")
        self.app.run_async(_task)
