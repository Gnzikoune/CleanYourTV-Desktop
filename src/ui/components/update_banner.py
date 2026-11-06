"""
Fluent 2 Update Notification Banner Component
"""

from typing import TYPE_CHECKING, Any
import customtkinter as ctk
from src.services.update_checker import UpdateCheckerService

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow


class UpdateBanner(ctk.CTkFrame):
    """Subtle top notification banner prompting user to download new .exe."""

    def __init__(self, parent: Any, app: "MainWindow", latest_tag: str, download_url: str) -> None:
        super().__init__(parent, fg_color="#183B22", corner_radius=8, border_width=1, border_color="#107C41")
        self.app = app
        self.download_url = download_url

        lbl = ctk.CTkLabel(
            self,
            text=f"🚀 Nouvelle version {latest_tag} disponible !",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#6CCB5F"
        )
        lbl.pack(side="left", padx=14, pady=6)

        btn_dl = ctk.CTkButton(
            self, text="⚡ Télécharger l'exécutable (.exe)", width=170, height=28,
            font=ctk.CTkFont(size=11, weight="bold"), fg_color="#107C41", hover_color="#0E6B38",
            corner_radius=6, command=self._on_download
        )
        btn_dl.pack(side="left", padx=10, pady=6)

        btn_close = ctk.CTkButton(
            self, text="✕", width=26, height=26,
            font=ctk.CTkFont(size=11), fg_color="transparent", hover_color="#265030",
            corner_radius=6, command=self.destroy
        )
        btn_close.pack(side="right", padx=8, pady=6)

    def _on_download(self) -> None:
        UpdateCheckerService.open_download(self.download_url)
        self.app.set_status("Téléchargement de la mise à jour lancé dans votre navigateur.")

