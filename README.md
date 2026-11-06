# CleanYourTV Desktop Manager 📺✨

> A native Windows control center (Microsoft Fluent 2 design) to manage, debloat, optimize, and customize any Android TV or Google TV over Wi-Fi / ADB.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D4.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](#)

---

## 🌟 Highlights

- **Universal Compatibility:** Works with any brand running Android TV / Google TV (Sony, TCL, Xiaomi, Panasonic, Philips, Hisense, Chromecast, Nvidia Shield, etc.).
- **Zero-Install Portable `.exe`:** No Python or manual ADB installation needed for end users.
- **Built-in Pure-Python ADB Engine:** Persistent socket connection offering ~20ms response times for snappy remote control.
- **Safe Debloat Manager:** One-click disable/enable for OEM bloatware & telemetry with built-in protection against disabling core system packages.
- **Remote & Live Mirroring:** Virtual D-pad, media keys, PC-to-TV clipboard pasting, toast message broadcasting, and optional 60 FPS live screen streaming via `scrcpy`.
- **System Speed Boost & Security:** 
  - Animation speed scaler (0.5x instant responsiveness).
  - AOT machine code precompilation.
  - One-click Encrypted AdGuard Private DNS setup (system-wide adblocking without third-party apps).
  - Security audit & ADB lockdown switch (closes port 5555 once done).

---

## 🚀 Quick Start

### Option 1: Run the Precompiled Standalone Executable
1. Download the latest `CleanYourTV-Manager.exe` from [Releases](../../releases).
2. Ensure your Android TV is on the same local network (or reachable via VPN/Tailscale) with **Network / Wireless Debugging** enabled in *Developer Options*.
3. Launch `CleanYourTV-Manager.exe`, type your TV's IP address, and click **⚡ Connecter**.

### Option 2: Run from Source
```powershell
# Clone the repository
git clone https://github.com/Gnzikoune/CleanYourTV-Desktop.git
cd CleanYourTV-Desktop

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the manager
python app.py
```

---

## 🛠️ Building the Standalone `.exe`

To package the application into a single portable binary with PyInstaller:

```powershell
pyinstaller --noconfirm --onedir --windowed `
  --icon="assets/icon.ico" `
  --add-data "assets;assets" `
  --name="CleanYourTV-Manager" `
  app.py
```

The resulting folder will be available inside `dist/CleanYourTV-Manager/`.

---

## 🔒 Safety & Architecture

CleanYourTV Desktop Manager strictly complies with the non-destructive debloating philosophy:
- **No uninstallations (`pm uninstall`)**: All freezes use `pm disable-user --user 0`, allowing instant 100% restoration at any time.
- **Core system blacklist**: Critical components (`com.android.systemui`, `com.android.settings`, package installers, keyboard services) cannot be disabled through the UI.
- **Private & Local**: Zero telemetry or third-party tracking. All communication stays strictly between your PC and your local TV.

---

## 🤝 Contributing & Community

Built as an open-source companion project to [CleanYourTV](https://github.com/Gathin23/cleanyourtv).

Contributions, bug reports, and pull requests are warmly welcome!

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
