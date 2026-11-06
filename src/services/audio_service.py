"""
Audio Streaming Domain Service (Clean Architecture)
Manages simultaneous TV audio broadcasting over LAN & Tailscale VPN.
"""

import os
import subprocess
from typing import Tuple, Optional
from src.infra.adb_client import AdbClient


class AudioService:
    """Manages AudioRelay streaming between Android TV and Windows PC."""

    KNOWN_PACKAGES = [
        "com.azefsw.audioconnect",
        "com.asphalifa.audiorelay"
    ]

    PC_EXECUTABLE_PATHS = [
        r"C:\Program Files\AudioRelay\AudioRelay.exe",
        r"C:\Program Files (x86)\AudioRelay\AudioRelay.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\AudioRelay\AudioRelay.exe")
    ]

    def __init__(self, adb: AdbClient):
        self.adb = adb

    def is_tv_agent_installed(self) -> Tuple[bool, Optional[str]]:
        """Check if AudioRelay or an audio agent is installed on the TV."""
        ok, out = self.adb.shell("pm list packages")
        if not ok or not out:
            return False, None

        for pkg in self.KNOWN_PACKAGES:
            if f"package:{pkg}" in out:
                return True, pkg
        return False, None

    def start_tv_agent(self) -> Tuple[bool, str]:
        """Launch the audio streaming agent on the Android TV."""
        installed, pkg = self.is_tv_agent_installed()
        if not installed or not pkg:
            return False, "AudioRelay n'est pas encore installé sur la TV."

        # Lance l'activité principale de l'agent audio
        cmd = f"monkey -p {pkg} -c android.intent.category.LAUNCHER 1"
        ok, out = self.adb.shell(cmd)
        if ok and "Events injected: 1" in out:
            return True, "Agent audio lancé en arrière-plan sur la TV."
        return False, f"Impossible de lancer l'agent audio: {out.strip()}"

    def locate_pc_client(self) -> Optional[str]:
        """Auto-detect AudioRelay Windows executable."""
        for path in self.PC_EXECUTABLE_PATHS:
            if os.path.exists(path):
                return path
        # Check in PATH
        check = subprocess.run(["where", "AudioRelay.exe"], capture_output=True, text=True)
        if check.returncode == 0 and check.stdout.strip():
            return check.stdout.strip().splitlines()[0]
        return None

    def launch_pc_client(self, target_ip: str) -> Tuple[bool, str]:
        """Launch the Windows AudioRelay receiver."""
        client_path = self.locate_pc_client()
        if not client_path:
            return False, "AudioRelay n'est pas installé sur le PC. Installez-le avec : winget install AsaphaHalifa.AudioRelay"

        try:
            flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            subprocess.Popen([client_path], creationflags=flags)
            return True, f"AudioRelay ouvert sur PC. Connectez-vous à l'IP {target_ip}."
        except Exception as e:
            return False, f"Erreur lors du lancement d'AudioRelay sur PC: {e}"

    def open_playstore_on_tv(self) -> Tuple[bool, str]:
        """Open AudioRelay page directly on Google Play Store on the TV."""
        cmd = "am start -a android.intent.action.VIEW -d 'market://details?id=com.azefsw.audioconnect'"
        ok, _ = self.adb.shell(cmd)
        if ok:
            return True, "Page AudioRelay ouverte sur le Play Store de la TV."
        return False, "Échec de l'ouverture du Play Store sur la TV."

