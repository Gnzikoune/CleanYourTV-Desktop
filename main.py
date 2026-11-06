"""
CleanYourTV Desktop Manager — Entry Point
"""

import customtkinter as ctk
from src.core.config import setup_windows_appid
from src.ui.main_window import MainWindow

# Fluent 2 Theme Initialization
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main():
    setup_windows_appid("cleanyourtv.desktop.manager.v1")
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
