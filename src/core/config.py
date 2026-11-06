"""
Core Configuration & Paths Module
"""

import os
import sys
import json
import ctypes
from pathlib import Path


def get_resource_path(relative_path: str) -> str:
    """Return absolute path to resource, compatible with PyInstaller bundles."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def setup_windows_appid(app_id: str = "cleanyourtv.desktop.manager.v1") -> None:
    """Register explicit Windows AppUserModelID for taskbar icon."""
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass


# Storage Paths
CONFIG_DIR = Path.home() / ".cleanyourtv_desktop"
CONFIG_FILE = CONFIG_DIR / "config.json"
KEYS_DIR = CONFIG_DIR / "keys"

# UI Constants (Fluent 2 Dark Tokens)
COLOR_BG_MAIN = "#1E1E1E"
COLOR_BG_CARD = "#242424"
COLOR_BG_SUB = "#2D2D2D"
COLOR_ACCENT = "#0078D4"
COLOR_ACCENT_HOVER = "#005FB8"
COLOR_SUCCESS = "#107C41"
COLOR_SUCCESS_HOVER = "#0E6B38"
COLOR_DANGER = "#C42B1C"
COLOR_DANGER_HOVER = "#A80000"
COLOR_TEXT_PRIMARY = "#FFFFFF"
COLOR_TEXT_MUTED = "#888888"


class ConfigManager:
    """Manages persistent user configuration."""

    @staticmethod
    def load() -> dict:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if not CONFIG_FILE.exists():
            return {}
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    @staticmethod
    def save(data: dict) -> bool:
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
