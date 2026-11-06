"""
High-Speed Asynchronous Local Network Scanner for Android TV Devices
"""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple


class NetworkScannerService:
    """Discovers ADB-enabled Android TV devices on the local subnet."""

    @staticmethod
    def get_local_ip() -> str:
        """Retrieve local host IP address connected to default gateway."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "192.168.1.1"

    @classmethod
    def scan_subnet(cls, port: int = 5555, timeout: float = 0.4, max_workers: int = 60) -> List[Tuple[str, int]]:
        """
        Scan /24 local subnet in parallel for open ADB ports.
        Returns list of (ip_address, port) pairs.
        """
        local_ip = cls.get_local_ip()
        parts = local_ip.split(".")
        if len(parts) != 4:
            return []

        base_ip = f"{parts[0]}.{parts[1]}.{parts[2]}"
        active_devices: List[Tuple[str, int]] = []

        def _probe_ip(ip_str: str) -> Tuple[bool, str]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                res = sock.connect_ex((ip_str, port))
                sock.close()
                return (res == 0, ip_str)
            except Exception:
                return (False, ip_str)

        all_ips = [f"{base_ip}.{i}" for i in range(1, 255)]

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(_probe_ip, ip) for ip in all_ips]
            for fut in as_completed(futures):
                is_open, ip = fut.result()
                if is_open:
                    active_devices.append((ip, port))

        return sorted(active_devices)
