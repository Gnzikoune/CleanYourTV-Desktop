"""
System Performance & Security Management Domain Service
"""

from typing import List, Tuple
from src.infra.adb_client import AdbClient


class SystemService:
    """Manages speed scaling, AOT precompilation, private DNS, and lockdowns."""

    def __init__(self, adb: AdbClient) -> None:
        self.adb = adb

    def set_animation_scale(self, scale: float = 0.5) -> Tuple[bool, str]:
        """Adjust window/transition animation scales for snappier UI."""
        s = str(scale)
        self.adb.shell(f"settings put global window_animation_scale {s}")
        self.adb.shell(f"settings put global transition_animation_scale {s}")
        self.adb.shell(f"settings put global animator_duration_scale {s}")
        return True, f"Animations réglées à {s}x (fluidité instantanée)."

    def compile_aot(self, target_package: str = "com.gathin.tvhome") -> Tuple[bool, str]:
        """Force Ahead-Of-Time compilation to native machine code."""
        cmd = f"cmd package compile -m speed -f {target_package}"
        ok, out = self.adb.shell(cmd, timeout=30)
        if ok and ("success" in out.lower() or not out.strip()):
            return True, f"Compilation AOT machine réussie pour '{target_package}'."
        return False, f"Retour compilation: {out.strip()}"

    def configure_adguard_dns(self) -> Tuple[bool, str]:
        """Configure system-wide Private DNS over TLS with AdGuard."""
        self.adb.shell("settings put global private_dns_specifier dns.adguard-dns.com")
        self.adb.shell("settings put global private_dns_mode hostname")
        return True, "DNS AdGuard actif (filtrage publicitaire activé)."

    def disable_private_dns(self) -> Tuple[bool, str]:
        """Disable Private DNS and restore default network routing (YouTube / Play Store)."""
        self.adb.shell("settings put global private_dns_mode off")
        return True, "DNS Privé désactivé (accès direct rétabli pour YouTube/Google)."

    def is_adguard_active(self) -> bool:
        """Check if private DNS is actively routing through AdGuard."""
        _, mode = self.adb.shell("settings get global private_dns_mode")
        _, spec = self.adb.shell("settings get global private_dns_specifier")
        return "hostname" in mode and "adguard" in spec.lower()

    def audit_security(self) -> Tuple[bool, str, List[str]]:
        """Scan listening ports and verify DNS protection."""
        _, ports = self.adb.shell("cat /proc/net/tcp /proc/net/tcp6")
        _, dns_mode = self.adb.shell("settings get global private_dns_mode")

        findings: List[str] = []
        has_adb_open = ":15B3" in ports  # 5555 in hex
        has_adguard = "hostname" in dns_mode
        has_oneroom = ":8257" in ports   # 33367 in hex

        if has_adb_open:
            findings.append("⚠️ Port 5555 (ADB) ouvert sur le réseau")
        else:
            findings.append("🔒 Port 5555 fermé")

        if has_adguard:
            findings.append("🛡️ DNS AdGuard chiffré actif")
        else:
            findings.append("ℹ️ DNS par défaut (compatible YouTube/Store)")

        if not has_oneroom:
            findings.append("✅ Mouchard Transsion absent ou neutralisé")
        else:
            findings.append("⚠️ Mouchard Transsion actif (:33367)")

        summary = " • ".join(findings)
        return True, summary, findings

    def lockdown_adb(self) -> Tuple[bool, str]:
        """Disable remote ADB and shut down listening port 5555."""
        self.adb.shell("settings put global adb_enabled 0")
        self.adb.shell("setprop service.adb.tcp.port -1")
        self.adb.shell("stop adbd")
        self.adb.disconnect()
        return True, "Port 5555 fermé. Débogage réseau coupé avec succès."

    def reboot(self) -> Tuple[bool, str]:
        """Soft-reboot the device cleanly."""
        self.adb.shell("reboot")
        self.adb.disconnect()
        return True, "Téléviseur en cours de redémarrage..."
