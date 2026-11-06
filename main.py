"""
CleanYourTV Desktop Manager — Entry Point
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path for robust imports across all environments & IDEs
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import customtkinter as ctk
from src.core.config import setup_windows_appid
from src.ui.main_window import MainWindow

# Fluent 2 Theme Initialization
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main() -> None:
    setup_windows_appid("cleanyourtv.desktop.manager.v1")
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
