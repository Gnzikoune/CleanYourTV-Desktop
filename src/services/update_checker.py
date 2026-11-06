"""
Asynchronous GitHub Release Checker and Direct Executable Downloader
"""

import json
import urllib.request
import webbrowser
from typing import Optional, Tuple

CURRENT_VERSION = "v1.1.0"
REPO_API_URL = "https://api.github.com/repos/Gnzikoune/CleanYourTV-Desktop/releases/latest"


class UpdateCheckerService:
    """Checks for latest GitHub release and direct .exe download assets."""

    @staticmethod
    def _parse_version(v_str: str) -> Tuple[int, ...]:
        """Convert 'v1.0.1' into numeric tuple (1, 0, 1) for reliable comparison."""
        clean = v_str.lstrip("v").strip()
        parts = []
        for p in clean.split("."):
            try:
                parts.append(int(p))
            except ValueError:
                parts.append(0)
        return tuple(parts)

    @classmethod
    def check_for_updates(cls) -> Tuple[bool, str, str, str]:
        """
        Check GitHub API for newer release.
        Returns:
            (has_update, latest_version_tag, direct_exe_url, release_html_url)
        """
        try:
            req = urllib.request.Request(
                REPO_API_URL,
                headers={"User-Agent": f"CleanYourTV-Manager/{CURRENT_VERSION}"}
            )
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status != 200:
                    return False, CURRENT_VERSION, "", ""
                data = json.loads(response.read().decode("utf-8"))

            latest_tag = data.get("tag_name", CURRENT_VERSION)
            release_url = data.get("html_url", "")
            assets = data.get("assets", [])

            # Locate direct standalone .exe asset
            direct_exe_url = ""
            for a in assets:
                name = a.get("name", "").lower()
                if name.endswith(".exe"):
                    direct_exe_url = a.get("browser_download_url", "")
                    break

            if not direct_exe_url and release_url:
                direct_exe_url = release_url

            has_update = cls._parse_version(latest_tag) > cls._parse_version(CURRENT_VERSION)
            return has_update, latest_tag, direct_exe_url, release_url

        except Exception:
            return False, CURRENT_VERSION, "", ""

    @staticmethod
    def open_download(url: str) -> None:
        """Open web browser to trigger direct executable download."""
        if url:
            webbrowser.open(url)

