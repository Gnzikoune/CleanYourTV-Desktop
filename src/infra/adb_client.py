"""
Persistent ADB TCP Client with pure-Python socket & RSA keys
"""

import subprocess
import threading
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from src.core.config import KEYS_DIR

try:
    from adb_shell.adb_device import AdbDeviceTcp
    from adb_shell.auth.sign_pythonrsa import PythonRSASigner
    ADB_SHELL_AVAILABLE = True
except ImportError:
    ADB_SHELL_AVAILABLE = False
    AdbDeviceTcp = None  # type: ignore
    PythonRSASigner = None  # type: ignore


class AdbClient:
    """Manages low-latency persistent ADB connection via TCP sockets."""

    def __init__(self) -> None:
        self.device: Optional[Any] = None
        self.host: str = ""
        self.port: int = 5555
        self.signer: Optional[Any] = None
        self.lock = threading.Lock()
        self._setup_keys()

    # ------------------------------------------------------------------
    # Key management
    # ------------------------------------------------------------------

    def _setup_keys(self) -> None:
        """Initialize or generate RSA keypair for ADB authentication."""
        KEYS_DIR.mkdir(parents=True, exist_ok=True)
        priv_key = KEYS_DIR / "adbkey"
        pub_key = KEYS_DIR / "adbkey.pub"

        if not priv_key.exists():
            self._generate_rsa_key(str(priv_key))

        if priv_key.exists() and ADB_SHELL_AVAILABLE:
            self._load_signer(priv_key, pub_key)

    def _generate_rsa_key(self, priv_path: str) -> None:
        """Generate ADB RSA keypair using adb_shell.auth.keygen or CLI fallback."""
        try:
            from adb_shell.auth.keygen import keygen
            keygen(priv_path)
            return
        except Exception:
            pass
        try:
            subprocess.run(["adb", "keygen", priv_path], capture_output=True)
        except Exception:
            pass

    def _load_signer(self, priv_key: Path, pub_key: Path) -> None:
        """Load RSA signer from key files on disk."""
        try:
            with open(priv_key, "rb") as f:
                priv_data = f.read()
            with open(pub_key, "rb") as f:
                pub_data = f.read()
            if PythonRSASigner is not None:
                self.signer = PythonRSASigner(pub_data, priv_data)
        except Exception:
            self.signer = None

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    def connect(self, host: str, port: int = 5555, timeout: int = 5) -> Tuple[bool, str]:
        """Establish persistent connection to TV."""
        with self.lock:
            self._disconnect_unlocked()
            self.host = host
            self.port = port

            if ADB_SHELL_AVAILABLE and self.signer and AdbDeviceTcp is not None:
                try:
                    dev = AdbDeviceTcp(
                        self.host, self.port,
                        default_transport_timeout_s=timeout
                    )
                    dev.connect(rsa_keys=[self.signer], auth_timeout_s=timeout)
                    self.device = dev
                    return True, "Connecté avec succès via adb_shell (latence ~20ms)."
                except Exception:
                    self.device = None

            # Fallback: system adb CLI
            try:
                res = subprocess.run(
                    ["adb", "connect", f"{host}:{port}"],
                    capture_output=True, text=True, timeout=timeout
                )
                if "connected" in res.stdout.lower():
                    return True, f"Connecté via CLI adb: {res.stdout.strip()}"
                return False, f"Connexion refusée: {res.stdout or res.stderr}"
            except Exception as e:
                return False, f"Impossible d'établir la connexion: {e}"

    def disconnect(self) -> None:
        """Close active ADB connection and release socket."""
        with self.lock:
            self._disconnect_unlocked()

    def _disconnect_unlocked(self) -> None:
        """Internal disconnect — must be called while lock is already held."""
        if self.device:
            try:
                self.device.close()
            except Exception:
                pass
            self.device = None

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def is_connected(self) -> bool:
        """Check if currently connected."""
        if self.device is not None:
            return True
        try:
            res = subprocess.run(
                ["adb", "devices"],
                capture_output=True, text=True, timeout=2
            )
            for line in res.stdout.splitlines():
                if f"{self.host}:{self.port}" in line and "device" in line:
                    return True
        except Exception:
            pass
        return False

    # ------------------------------------------------------------------
    # Shell
    # ------------------------------------------------------------------

    def shell(self, command: str, timeout: int = 10) -> Tuple[bool, str]:
        """Execute a shell command over persistent connection."""
        with self.lock:
            if self.device:
                try:
                    out = self.device.shell(command)
                    return True, out if out is not None else ""
                except Exception:
                    self.device = None

            try:
                cmd = ["adb", "-s", f"{self.host}:{self.port}", "shell", command]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                return (res.returncode == 0), (res.stdout if res.returncode == 0 else res.stderr)
            except Exception as e:
                return False, str(e)

    # ------------------------------------------------------------------
    # Device info
    # ------------------------------------------------------------------

    def get_device_props(self) -> Dict[str, str]:
        """Read standard Android hardware properties."""
        _, model = self.shell("getprop ro.product.model")
        _, brand = self.shell("getprop ro.product.brand")
        _, version = self.shell("getprop ro.build.version.release")
        _, sdk = self.shell("getprop ro.build.version.sdk")
        return {
            "model": model.strip(),
            "brand": brand.strip().capitalize(),
            "version": version.strip(),
            "sdk": sdk.strip(),
        }
