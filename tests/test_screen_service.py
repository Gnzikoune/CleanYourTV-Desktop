"""
Unit tests for ScreenService (Clean Architecture & GEF Standards)
"""

import unittest
from unittest.mock import MagicMock, patch
from src.services.screen_service import ScreenService


class TestScreenService(unittest.TestCase):
    def setUp(self):
        self.mock_adb = MagicMock()
        self.service = ScreenService(self.mock_adb)

    @patch("subprocess.Popen")
    @patch.object(ScreenService, "locate_scrcpy", return_value="C:\\fake\\scrcpy.exe")
    def test_start_mirroring_low_power(self, mock_locate, mock_popen):
        ok, msg = self.service.start_mirroring("192.168.1.50", low_power=True)
        self.assertTrue(ok)
        self.assertIn("Fluide 720p", msg)

        # Vérifie que les paramètres anti-saccades ont bien été passés
        cmd = mock_popen.call_args[0][0]
        self.assertIn("--max-size=1280", cmd)
        self.assertIn("--video-bit-rate=3M", cmd)
        self.assertIn("--max-fps=30", cmd)
        self.assertIn("--no-audio", cmd)

    @patch("subprocess.Popen")
    @patch.object(ScreenService, "locate_scrcpy", return_value="C:\\fake\\scrcpy.exe")
    def test_start_mirroring_full_hd(self, mock_locate, mock_popen):
        ok, msg = self.service.start_mirroring("192.168.1.50", low_power=False)
        self.assertTrue(ok)
        self.assertIn("Full HD", msg)

        cmd = mock_popen.call_args[0][0]
        self.assertIn("--max-size=1920", cmd)
        self.assertIn("--video-bit-rate=8M", cmd)

    @patch.object(ScreenService, "locate_scrcpy", return_value=None)
    def test_start_mirroring_missing_scrcpy(self, mock_locate):
        ok, msg = self.service.start_mirroring("192.168.1.50")
        self.assertFalse(ok)
        self.assertIn("scrcpy n'a pas été trouvé", msg)


if __name__ == "__main__":
    unittest.main()

