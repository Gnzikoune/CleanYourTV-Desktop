# CleanYourTV Desktop Manager 📺✨

<p align="center">
  <strong>A native Windows control center (Microsoft Fluent 2 design) to manage, debloat, optimize, and customize any Android TV or Google TV over Wi-Fi / ADB.</strong>
</p>

<p align="center">
  <a href="README.fr.md">🇫🇷 <strong>Lire en Français</strong></a> ·
  <a href="README.md">🇬🇧 <strong>Read in English</strong></a>
</p>

<p align="center">
  <a href="https://github.com/Gnzikoune/CleanYourTV-Desktop/releases/latest"><img src="https://img.shields.io/github/v/release/Gnzikoune/CleanYourTV-Desktop?color=0078D4&label=Latest%20Release&logo=windows" alt="Release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
  <a href="#"><img src="https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011%20(x64)-0078D4?logo=windows" alt="Platform"></a>
  <a href="#"><img src="https://img.shields.io/badge/Design-Microsoft%20Fluent%202-005FB8" alt="Fluent 2"></a>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python"></a>
  <a href="https://github.com/Gathin23/cleanyourtv"><img src="https://img.shields.io/badge/Companion%20to-CleanYourTV-orange" alt="CleanYourTV"></a>
</p>

---

## 📑 Table of Contents

- [The Problem](#-the-problem)
- [Key Features](#-key-features)
  - [1. Universal & Persistent Connection](#1-universal--persistent-connection)
  - [2. Virtual Remote & Direct Typing](#2-virtual-remote--direct-typing)
  - [3. Low-Latency Screen Mirroring (scrcpy)](#3-low-latency-screen-mirroring-scrcpy)
  - [4. Safe & Intelligent Debloat Manager](#4-safe--intelligent-debloat-manager)
  - [5. System Boost & Hardware Acceleration](#5-system-boost--hardware-acceleration)
  - [6. Privacy, Security & ADB Lockdown](#6-privacy-security--adb-lockdown)
  - [7. Themes & Wallpapers](#7-themes--wallpapers)
- [How to Enable Developer Options on your TV](#-how-to-enable-developer-options-on-your-tv)
- [Quick Start](#-quick-start)
  - [Option A: Portable Binary (No Installation Required)](#option-a-portable-binary-no-installation-required)
  - [Option B: Run from Source Code](#option-b-run-from-source-code)
- [Building the Executable (.exe)](#-building-the-executable-exe)
- [Safety & Anti-Bricking Philosophy](#-safety--anti-bricking-philosophy)
- [Device Compatibility Matrix](#-device-compatibility-matrix)
- [Troubleshooting & FAQ](#-troubleshooting--faq)
- [Contributing](#-contributing)
- [License & Acknowledgments](#-license--acknowledgments)

---

## 🧐 The Problem

Modern Smart TVs (Android TV, Google TV, OEM variants) ship overloaded with:
- **Sponsored ads, trailers, and recommended junk** running continuously on the home screen.
- **Background telemetry and metrics collectors** consuming RAM, CPU cycles, and network bandwidth.
- **Sluggish interfaces** that stutter during simple navigation because low-tier TV processors (MediaTek, Realtek, Amlogic) are starved of resources.
- **Tedious text entry** using a physical remote to type complex passwords or search queries.

**CleanYourTV Desktop Manager** gives you back full control over your TV right from your Windows desktop—safely, visually, and without requiring any command-line experience.

---

## 🌟 Key Features

### 1. Universal & Persistent Connection
- **Zero-Configuration Discovery:** Enter your TV's local IP address (or remote VPN/Tailscale IP) and connect with one click.
- **Embedded Pure-Python ADB Engine:** Communicates over pure TCP sockets without requiring `adb.exe` to be installed on your computer.
- **Persistent Connection Pool:** Holds open ADB sessions for near-instant execution (~20ms latency), completely eliminating the 2-second reconnect lag typical of standard scripts.
- **Hardware Probing:** Automatically detects and displays your TV's brand, model, Android version, and SDK level upon connection.

### 2. Virtual Remote & Direct Typing
- **D-Pad & Navigation:** Full direction pad (Up, Down, Left, Right, OK/Center), Home, Back, Menu, Volume + / -, and Mute.
- **PC-to-TV Clipboard & Typing:** Copy any text, password, or URL on Windows and paste it instantly into the active text field on your TV.
- **On-Screen Toast Notifications:** Send instant HUD pop-up messages to the TV screen (e.g., *"Dinner is ready!"*).

### 3. Low-Latency Screen Mirroring (scrcpy)
- **60 FPS Live Stream:** Detects and launches `scrcpy` in an ultra-low latency borderless window to view and control your TV directly with your mouse and keyboard.
- **Native Screenshot Grabber:** Captures the current TV screen over ADB and displays/saves it locally on your PC.

### 4. Safe & Intelligent Debloat Manager
- **Human-Readable Package Directory:** Translates obscure package IDs (such as `com.smartdevice.acr.recommendation` or `com.google.android.katniss`) into plain descriptions.
- **One-Click Freeze / Unfreeze:** Uses `pm disable-user --user 0` instead of dangerous uninstalls.
- **Strict Anti-Brick Blacklist:** Built-in safeguards make it impossible to disable core Android services (SystemUI, Settings, PackageInstaller, Keyboards).
- **Emergency "Restore All" Switch:** Restore every disabled app to its factory state with a single confirmation.

### 5. System Boost & Hardware Acceleration
- **Animation Speed Scaler (0.5x):** Cuts window and transition animations in half for an immediate, snappier UI response.
- **Ahead-Of-Time (AOT) Native Compilation:** Forces Android ART (`cmd package compile -m speed`) to precompile the launcher into native machine code, eliminating app launch stutter.

### 6. Privacy, Security & ADB Lockdown
- **Encrypted AdGuard Private DNS:** Activates system-wide DNS-over-TLS (`dns.adguard-dns.com`) with one click to block ad servers and trackers across all apps without installing any extra software.
- **Network Security Audit:** Inspects `/proc/net/tcp` to detect open ports (5555, OEM background push daemons, rogue services).
- **Secure ADB Lockdown Switch:** Closes port 5555 and cuts off wireless debugging once you finish configuring your TV, ensuring complete protection from unauthorized network access.

### 7. Themes & Wallpapers
- Seamless compatibility with the official [CleanYourTV Launcher](https://github.com/Gathin23/cleanyourtv) (`com.gathin.tvhome`).
- Push custom 4K wallpapers from your PC to the TV via pure base64 streaming.
- Switch between Minimalist OLED Dark and custom styles in real time.

---

## 📺 How to Enable Developer Options on your TV

Before connecting, you need to turn on **USB / Network Debugging** on your TV once:

1. On your TV, navigate to **Settings** (`⚙️`) → **Device Preferences** (or **System**) → **About**.
2. Scroll down to **Android TV OS build** (or **Build number**).
3. Press the **OK** button on your physical remote **7 times**. A toast message will announce: *"You are now a developer!"*.
4. Return to **Settings** → **Device Preferences** (or **System**) → **Developer options**.
5. Enable **USB debugging** and **Network debugging** (or **Wireless debugging**).
6. Note the TV's IP address in **Settings** → **Network & Internet** (e.g., `192.168.1.50`).
7. When connecting for the first time, check *"Always allow from this computer"* on your TV screen.

---

## 🚀 Quick Start

### Option A: Portable Binary (No Installation Required)

> Ideal for everyday users. No Python, no terminal, and no dependencies needed.

1. Head to the **[Releases Page](https://github.com/Gnzikoune/CleanYourTV-Desktop/releases/latest)**.
2. Download **`CleanYourTV-Manager-v1.0.0-windows-x64.zip`**.
3. Extract the archive into any folder on your PC.
4. Launch **`CleanYourTV-Manager.exe`**.
5. Enter your TV's IP and click **⚡ Connecter**.

---

### Option B: Run from Source Code

```powershell
# 1. Clone the repository
git clone https://github.com/Gnzikoune/CleanYourTV-Desktop.git
cd CleanYourTV-Desktop

# 2. Create and activate a Python virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the application
python app.py
```

---

## 🛠️ Building the Executable (.exe)

You can package your own standalone `.exe` using PyInstaller:

```powershell
pip install pyinstaller
pyinstaller --noconfirm --onedir --windowed `
  --icon="assets/icon.ico" `
  --add-data "assets;assets" `
  --name="CleanYourTV-Manager" `
  app.py
```

The compiled output will be generated inside `dist/CleanYourTV-Manager/`.

---

## 🛡️ Safety & Anti-Bricking Philosophy

CleanYourTV Desktop Manager strictly complies with the non-destructive debloating philosophy of the parent [CleanYourTV](https://github.com/Gathin23/cleanyourtv) community:

| Principle | How It Is Enforced |
|---|---|
| **Never Uninstall** | Uses `pm disable-user --user 0`. Packages remain in system partition and can be re-enabled instantly. |
| **Protected Core Packages** | Blacklisted packages (`android`, `SystemUI`, `Settings`, `PackageInstaller`, keyboards) are locked and cannot be disabled through the UI. |
| **No Root or Flashing** | Works strictly within authorized Android user space over standard ADB. |
| **Total Privacy** | Operates strictly locally between your PC and your TV. Zero telemetry, zero analytics, zero external servers. |

---

## 📱 Device Compatibility Matrix

CleanYourTV Desktop Manager works with **any hardware running Android TV 8.0 (API 26) through Android 14+ / Google TV**:

| Brand | System | Status | Notes |
|---|---|:---:|---|
| **Sony Bravia** | Google TV / Android TV | ✅ Verified | Excellent response, handles AOT compilation smoothly. |
| **TCL** | Google TV / Android TV | ✅ Verified | Works on all G-series boards (G03, G05, G08, G10). |
| **Xiaomi / Redmi** | PatchWall / Android TV | ✅ Verified | Cleans telemetry and ad services cleanly. |
| **Panasonic** | Android TV 10/11 | ✅ Verified | Tested on Skyworth OEM SW4H boards. |
| **Philips** | Android TV / Google TV | ✅ Verified | Safe disable of OEM shop demos and telemetry. |
| **Chromecast with Google TV** | Google TV (HD & 4K) | ✅ Verified | Setupwraith warning respected. |
| **Nvidia Shield TV** | Android TV | ✅ Verified | Snappy low-latency execution. |
| **Hisense / Changhong / Coocaa** | Android TV OEM | ✅ Verified | Cleans retail demo loops and background trackers. |

---

## ❓ Troubleshooting & FAQ

<details>
<summary><b>1. The application says "Connection refused" or hangs when clicking Connect.</b></summary>
Ensure that:
- Your TV and PC are connected to the same Wi-Fi / LAN network (or reachable via VPN/Tailscale).
- **Network / USB debugging** is enabled in *Developer options* on the TV.
- You typed the correct IP address (verify in *Settings > Network* on the TV).
</details>

<details>
<summary><b>2. The TV screen asks for authorization.</b></summary>
When connecting for the first time, Android TV displays a security prompt: *"Allow USB debugging?"*. Check **"Always allow from this computer"** and select **OK** with your remote.
</details>

<details>
<summary><b>3. scrcpy doesn't open when clicking "Live Screen".</b></summary>
scrcpy is an optional dependency for live video streaming. You can install it on Windows via PowerShell:
```powershell
winget install Genymobile.scrcpy
```
CleanYourTV Desktop Manager will automatically locate it.
</details>

<details>
<summary><b>4. How do I turn ADB off completely once I'm done?</b></summary>
Go to the **Boost & Sécurité Système** tab and click **Verrouiller ADB**. This executes `stop adbd` and closes port 5555. To re-enable it later, turn it back on with your physical remote in Developer options.
</details>

---

## 🤝 Contributing

Contributions, feature requests, and bug reports are warmly welcome!

1. Fork the repository (`https://github.com/Gnzikoune/CleanYourTV-Desktop/fork`).
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License & Acknowledgments

- **License:** Released under the permissive **[MIT License](LICENSE)**.
- **Community:** Developed as a standalone companion for the worldwide **[CleanYourTV](https://github.com/Gathin23/cleanyourtv)** initiative.
