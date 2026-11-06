"""
Screen Streaming & Media Management Domain Service
"""

import os
import base64
import subprocess
from pathlib import Path
from typing import Tuple, Optional
from src.infra.adb_client import AdbClient
from src.core.config import CONFIG_DIR


class ScreenService:
    """Manages scrcpy video streaming, screenshots, and wallpaper pushing."""

    def __init__(self, adb: AdbClient):
        self.adb = adb

    @staticmethod
    def locate_scrcpy() -> Optional[str]:
        """Auto-detect scrcpy executable in standard locations."""
        candidates = [
            "scrcpy",
            r"C:\Users\hp\AppData\Local\Microsoft\WinGet\Packages\Genymobile.scrcpy_Microsoft.Winget.Source_8wekyb3d8bbwe\scrcpy-win64-v5.0.1\scrcpy.exe",
            r"C:\Program Files\scrcpy\scrcpy.exe",
            r"C:\tools\scrcpy\scrcpy.exe"
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
            if subprocess.run(["where", path], capture_output=True).returncode == 0:
                return path
        return None

    def start_mirroring(
        self, host: str, port: int = 5555, low_power: bool = True
    ) -> Tuple[bool, str]:
        """Launch scrcpy live streaming window with hardware-adapted profile."""
        scrcpy_path = self.locate_scrcpy()
        if not scrcpy_path:
            return False, "scrcpy n'a pas été trouvé (installez-le avec : winget install Genymobile.scrcpy)."

        cmd = [
            scrcpy_path,
            f"--tcpip={host}:{port}",
            "--window-title=CleanYourTV Live Display",
        ]

        if low_power:
            # Profil Haute Fluidité pour Smart TV (720p, 30 FPS, 3 Mbps, no-audio pour CPU TV)
            cmd.extend([
                "--max-size=1280",
                "--video-bit-rate=3M",
                "--max-fps=30",
                "--video-buffer=50",
                "--no-audio"
            ])
            profile_name = "Fluide 720p 30 FPS (Anti-saccades)"
        else:
            cmd.extend(["--max-size=1920", "--video-bit-rate=8M"])
            profile_name = "Full HD 1080p"

        try:
            flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            scrcpy_dir = os.path.dirname(scrcpy_path)
            subprocess.Popen(cmd, cwd=scrcpy_dir if scrcpy_dir else None, creationflags=flags)
            return True, f"Miroir {profile_name} lancé avec succès."
        except Exception as e:
            return False, f"Erreur de lancement scrcpy: {e}"

    def capture_screenshot(self) -> Tuple[bool, str, Optional[str]]:
        """Grab a live screenshot over ADB and save it locally."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        out_path = CONFIG_DIR / "latest_screenshot.png"
        ok, _ = self.adb.shell("screencap -p /sdcard/cleanyourtv_shot.png")
        if not ok:
            return False, "Échec de screencap sur la TV.", None

        ok_base64, out_b64 = self.adb.shell("cat /sdcard/cleanyourtv_shot.png | base64")
        if not ok_base64 or not out_b64.strip():
            return False, "Échec de lecture base64 de la capture.", None

        try:
            raw = base64.b64decode(out_b64.replace("\r", "").replace("\n", ""))
            with open(out_path, "wb") as f:
                f.write(raw)
            return True, "Capture enregistrée.", str(out_path)
        except Exception as e:
            return False, f"Erreur décodage image: {e}", None

    def push_wallpaper(self, local_image_path: str) -> Tuple[bool, str]:
        """Stream an image file directly to /sdcard/wallpaper.jpg."""
        if not os.path.exists(local_image_path):
            return False, "Fichier image introuvable."

        try:
            with open(local_image_path, "rb") as f:
                raw = f.read()
            b64_str = base64.b64encode(raw).decode("ascii")
            self.adb.shell(f"echo '{b64_str}' | base64 -d > /sdcard/wallpaper.jpg")
            return True, "Fond d'écran 4K transféré avec succès sur /sdcard/wallpaper.jpg."
        except Exception as e:
            return False, f"Erreur de transfert: {e}"
