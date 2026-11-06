"""
Tab 2: Safe Debloat & Package Management
"""

from tkinter import messagebox
from typing import TYPE_CHECKING, Any, List, Set
import customtkinter as ctk
from src.core.config import (
    COLOR_BG_CARD, COLOR_BG_SUB, COLOR_ACCENT,
    COLOR_ACCENT_HOVER, COLOR_DANGER, COLOR_DANGER_HOVER
)
from src.core.security_rules import is_safe_to_disable, get_friendly_name

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow


class DebloatTab:
    """Component for browsing, freezing, and restoring packages."""

    def __init__(self, parent: Any, app: "MainWindow") -> None:
        self.parent = parent
        self.app = app
        self.active_filter: str = "disabled"
        self._build_ui()

    def _build_ui(self) -> None:
        top_bar = ctk.CTkFrame(self.parent, fg_color=COLOR_BG_CARD, corner_radius=10)
        top_bar.pack(fill="x", padx=8, pady=(8, 4))

        ctk.CTkLabel(
            top_bar, text="Gestionnaire d'Applications & Débloat",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=16, pady=12)

        self.seg_filter = ctk.CTkSegmentedButton(
            top_bar, values=["Désactivées", "Toutes les applications"],
            command=self._on_filter_changed
        )
        self.seg_filter.set("Désactivées")
        self.seg_filter.pack(side="left", padx=16)

        ctk.CTkButton(
            top_bar, text="🔄 Rafraîchir", width=90, height=32, corner_radius=6,
            fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
            command=self.refresh_list
        ).pack(side="right", padx=12)

        ctk.CTkButton(
            top_bar, text="⚠️ Restaurer Tout", width=120, height=32, corner_radius=6,
            fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER,
            command=self._on_restore_all
        ).pack(side="right", padx=(0, 6))

        self.scroll = ctk.CTkScrollableFrame(self.parent, fg_color=COLOR_BG_CARD, corner_radius=10)
        self.scroll.pack(fill="both", expand=True, padx=8, pady=4)

    def _on_filter_changed(self, val: str) -> None:
        self.active_filter = "disabled" if val == "Désactivées" else "all"
        self.refresh_list()

    def refresh_list(self) -> None:
        if not self.app.adb.is_connected():
            self.app.set_status("Connectez un téléviseur pour lister les packages.")
            return

        def _task() -> None:
            self.app.set_status("Chargement des applications sur la TV...")
            disabled_set: Set[str] = set(self.app.debloat_service.get_disabled_packages())
            all_pkgs: List[str] = (
                self.app.debloat_service.get_all_packages()
                if self.active_filter == "all"
                else sorted(disabled_set)
            )

            def _populate_ui() -> None:
                for w in self.scroll.winfo_children():
                    w.destroy()

                if not all_pkgs:
                    ctk.CTkLabel(
                        self.scroll, text="Aucune application trouvée.",
                        font=ctk.CTkFont(size=14)
                    ).pack(pady=30)
                    self.app.set_status("Liste vide.")
                    return

                for pkg in all_pkgs[:100]:
                    self._render_card(pkg, pkg in disabled_set)

                self.app.set_status(f"{len(all_pkgs)} applications trouvées.")

            self.app.after(0, _populate_ui)

        self.app.run_async(_task)

    def _render_card(self, pkg: str, is_disabled: bool) -> None:
        friendly = get_friendly_name(pkg)
        card = ctk.CTkFrame(self.scroll, fg_color=COLOR_BG_SUB, corner_radius=8)
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

        is_safe = is_safe_to_disable(pkg)
        btn_action = ctk.CTkButton(
            card,
            text="Activer" if is_disabled else "Désactiver",
            width=80, height=30, corner_radius=6,
            fg_color="#107C41" if is_disabled else (COLOR_DANGER if is_safe else "#444444"),
            hover_color="#0E6B38" if is_disabled else (COLOR_DANGER_HOVER if is_safe else "#444444"),
            state="normal" if (is_disabled or is_safe) else "disabled",
            command=lambda p=pkg, dis=is_disabled, s=status_lbl: self._toggle_package(p, dis, s)
        )
        btn_action.pack(side="right", padx=12, pady=8)

    def _toggle_package(self, pkg: str, is_currently_disabled: bool, status_lbl: ctk.CTkLabel) -> None:
        def _task() -> None:
            if is_currently_disabled:
                ok, msg = self.app.debloat_service.enable_package(pkg)
            else:
                ok, msg = self.app.debloat_service.disable_package(pkg)

            if ok:
                new_state = not is_currently_disabled
                def _update() -> None:
                    status_lbl.configure(
                        text="Désactivé 🚫" if new_state else "Actif ✅",
                        text_color="#FFA0A0" if new_state else "#4CC2FF"
                    )
                self.app.after(0, _update)
            self.app.set_status(msg)

        self.app.run_async(_task)

    def _on_restore_all(self) -> None:
        ok = messagebox.askyesno(
            "Restaurer Tout",
            "Voulez-vous réactiver toutes les applications précédemment désactivées sur cette télévision ?"
        )
        if not ok:
            return

        def _task() -> None:
            self.app.set_status("Restauration de toutes les applications en cours...")
            count, _ = self.app.debloat_service.restore_all()
            self.app.set_status(f"{count} applications restaurées avec succès.")
            self.app.after(0, self.refresh_list)

        self.app.run_async(_task)
