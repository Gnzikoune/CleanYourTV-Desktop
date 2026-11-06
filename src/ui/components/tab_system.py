"""
Tab 3: System Performance Tuning & Security Lockdown
"""

from tkinter import messagebox
from typing import TYPE_CHECKING, Any, Callable
import customtkinter as ctk
from src.core.config import (
    COLOR_BG_CARD, COLOR_BG_SUB, COLOR_ACCENT,
    COLOR_ACCENT_HOVER, COLOR_DANGER, COLOR_DANGER_HOVER
)

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow


class SystemTab:
    """Component for speed optimizations, AdGuard DNS, and ADB lockdown."""

    def __init__(self, parent: Any, app: "MainWindow") -> None:
        self.parent = parent
        self.app = app
        self._build_ui()

    def _build_ui(self) -> None:
        container = ctk.CTkScrollableFrame(self.parent, fg_color=COLOR_BG_CARD, corner_radius=10)
        container.pack(fill="both", expand=True, padx=8, pady=8)

        ctk.CTkLabel(
            container, text="Optimisations & Sécurité Globale",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=20, pady=(16, 8), anchor="w")

        # 1. Animation Speed (0.5x)
        self._create_row(
            container,
            title="⚡ Fluidité & Vitesse des Animations (0.5x)",
            desc="Divise par deux les temps de transition d'Android pour une sensation immédiate de rapidité.",
            btn_text="Appliquer 0.5x",
            btn_color=COLOR_ACCENT,
            btn_hover=COLOR_ACCENT_HOVER,
            command=self._on_boost_animations
        )

        # 2. AOT Compilation
        self._create_row(
            container,
            title="🚀 Précompilation AOT Machine (Vitesse de lancement)",
            desc="Compile le launcher en code binaire machine natif pour éliminer tout lag au démarrage.",
            btn_text="Compiler AOT",
            btn_color=COLOR_ACCENT,
            btn_hover=COLOR_ACCENT_HOVER,
            command=self._on_compile_aot
        )

        # 3. Encrypted AdGuard DNS
        self._create_row(
            container,
            title="🛡️ Bloqueur de Pubs & Traceurs (DNS AdGuard)",
            desc="Active le DNS privé chiffré TLS sans aucune application supplémentaire requise.",
            btn_text="Activer AdGuard",
            btn_color="#107C41",
            btn_hover="#0E6B38",
            command=self._on_setup_dns
        )

        # 4. Security Audit
        f_audit = ctk.CTkFrame(container, fg_color=COLOR_BG_SUB, corner_radius=8)
        f_audit.pack(fill="x", padx=20, pady=6)
        info_audit = ctk.CTkFrame(f_audit, fg_color="transparent")
        info_audit.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(
            info_audit, text="🕵️ Audit de Sécurité & Ports Écoutants",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")
        self.lbl_audit = ctk.CTkLabel(
            info_audit,
            text="Cliquez sur 'Scanner' pour analyser les ports ouverts et l'exposition réseau.",
            font=ctk.CTkFont(size=11), text_color="#A0A0A0"
        )
        self.lbl_audit.pack(anchor="w")
        ctk.CTkButton(
            f_audit, text="Scanner", width=120, height=34, corner_radius=6,
            fg_color="#383838", hover_color="#444444", command=self._on_audit
        ).pack(side="right", padx=12)

        # 5. ADB Lockdown
        f_lock = ctk.CTkFrame(container, fg_color="#3A2020", corner_radius=8)
        f_lock.pack(fill="x", padx=20, pady=6)
        info_lock = ctk.CTkFrame(f_lock, fg_color="transparent")
        info_lock.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(
            info_lock, text="🔒 Fermer le Port ADB (Sécurisation maximale)",
            font=ctk.CTkFont(size=14, weight="bold"), text_color="#FFA0A0"
        ).pack(anchor="w")
        ctk.CTkLabel(
            info_lock,
            text="Ferme le port 5555. Réactivation possible uniquement avec la télécommande physique.",
            font=ctk.CTkFont(size=11), text_color="#D0A0A0"
        ).pack(anchor="w")
        ctk.CTkButton(
            f_lock, text="Verrouiller ADB", width=120, height=34, corner_radius=6,
            fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, command=self._on_lockdown
        ).pack(side="right", padx=12)

        # 6. Reboot
        self._create_row(
            container,
            title="🔄 Redémarrer Proprement la TV",
            desc="Redémarre l'appareil pour valider la prise en compte complète des modifications.",
            btn_text="Redémarrer",
            btn_color="#444444",
            btn_hover="#555555",
            command=self._on_reboot
        )

    def _create_row(
        self, parent: Any, title: str, desc: str,
        btn_text: str, btn_color: str, btn_hover: str,
        command: Callable[[], None]
    ) -> None:
        frame = ctk.CTkFrame(parent, fg_color=COLOR_BG_SUB, corner_radius=8)
        frame.pack(fill="x", padx=20, pady=6)
        info = ctk.CTkFrame(frame, fg_color="transparent")
        info.pack(side="left", padx=12, pady=10, fill="both", expand=True)
        ctk.CTkLabel(info, text=title, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(info, text=desc, font=ctk.CTkFont(size=11), text_color="#A0A0A0").pack(anchor="w")
        ctk.CTkButton(
            frame, text=btn_text, width=120, height=34, corner_radius=6,
            fg_color=btn_color, hover_color=btn_hover, command=command
        ).pack(side="right", padx=12)

    def _on_boost_animations(self) -> None:
        def _task() -> None:
            ok, msg = self.app.system_service.set_animation_scale(0.5)
            self.app.set_status(msg)
        self.app.run_async(_task)

    def _on_compile_aot(self) -> None:
        def _task() -> None:
            self.app.set_status("Compilation AOT native en cours...")
            ok, msg = self.app.system_service.compile_aot()
            self.app.set_status(msg)
        self.app.run_async(_task)

    def _on_setup_dns(self) -> None:
        def _task() -> None:
            ok, msg = self.app.system_service.configure_adguard_dns()
            self.app.set_status(msg)
        self.app.run_async(_task)

    def _on_audit(self) -> None:
        def _task() -> None:
            self.app.set_status("Audit de sécurité en cours...")
            ok, msg, _ = self.app.system_service.audit_security()
            def _update() -> None:
                self.lbl_audit.configure(text=msg, text_color="#4CC2FF")
                self.app.set_status("Audit de sécurité terminé.")
            self.app.after(0, _update)
        self.app.run_async(_task)

    def _on_lockdown(self) -> None:
        ok = messagebox.askyesno(
            "Verrouillage ADB",
            "⚠️ Attention : Cette action va couper le débogage réseau et fermer le port 5555 sur la TV.\n\n"
            "Voulez-vous continuer ?"
        )
        if not ok:
            return
        def _task() -> None:
            ok, msg = self.app.system_service.lockdown_adb()
            self.app.set_status(msg)
            self.app.after(0, self.app.on_disconnected)
        self.app.run_async(_task)

    def _on_reboot(self) -> None:
        def _task() -> None:
            ok, msg = self.app.system_service.reboot()
            self.app.set_status(msg)
            self.app.after(0, self.app.on_disconnected)
        self.app.run_async(_task)
