"""
Debloat & Application Management Domain Service
"""

from typing import List, Set, Tuple
from src.infra.adb_client import AdbClient
from src.core.security_rules import is_safe_to_disable, get_friendly_name


class DebloatService:
    """Handles package queries, freezing, unfreezing, and safety guards."""

    def __init__(self, adb: AdbClient):
        self.adb = adb

    def get_disabled_packages(self) -> List[str]:
        """Return list of packages currently disabled on TV."""
        _, out = self.adb.shell("pm list packages -d --user 0")
        packages = []
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("package:"):
                packages.append(line.replace("package:", "").strip())
        return sorted(packages)

    def get_all_packages(self) -> List[str]:
        """Return all installed packages."""
        _, out = self.adb.shell("pm list packages -u")
        packages = []
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("package:"):
                packages.append(line.replace("package:", "").strip())
        return sorted(packages)

    def disable_package(self, package_name: str) -> Tuple[bool, str]:
        """Safely disable a package using pm disable-user --user 0."""
        pkg = package_name.strip()
        if not is_safe_to_disable(pkg):
            return False, f"Protection active : '{pkg}' est un composant système critique."

        ok, out = self.adb.shell(f"pm disable-user --user 0 {pkg}")
        friendly = get_friendly_name(pkg)
        if ok and "disabled" in out.lower() or ok and not out.strip():
            return True, f"'{friendly}' ({pkg}) a été désactivé."
        return False, f"Échec de la désactivation: {out.strip()}"

    def enable_package(self, package_name: str) -> Tuple[bool, str]:
        """Re-enable a previously disabled package."""
        pkg = package_name.strip()
        ok, out = self.adb.shell(f"pm enable {pkg}")
        friendly = get_friendly_name(pkg)
        if ok:
            return True, f"'{friendly}' ({pkg}) a été réactivé."
        return False, f"Échec de l'activation: {out.strip()}"

    def restore_all(self) -> Tuple[int, List[str]]:
        """Re-enable all currently disabled packages."""
        disabled = self.get_disabled_packages()
        restored_count = 0
        errors = []

        for pkg in disabled:
            ok, msg = self.enable_package(pkg)
            if ok:
                restored_count += 1
            else:
                errors.append(msg)

        return restored_count, errors
