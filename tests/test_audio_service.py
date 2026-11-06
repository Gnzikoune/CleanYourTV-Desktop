"""
Unit tests for AudioService (Clean Architecture & GEF Standards)
"""

import unittest
from unittest.mock import MagicMock, patch
from src.services.audio_service import AudioService


class TestAudioService(unittest.TestCase):
    def setUp(self):
        self.mock_adb = MagicMock()
        self.service = AudioService(self.mock_adb)

    def test_is_tv_agent_installed_true(self):
        self.mock_adb.shell.return_value = (True, "package:com.android.settings\npackage:com.azefsw.audioconnect\n")
        installed, pkg = self.service.is_tv_agent_installed()
        self.assertTrue(installed)
        self.assertEqual(pkg, "com.azefsw.audioconnect")

    def test_is_tv_agent_installed_false(self):
        self.mock_adb.shell.return_value = (True, "package:com.android.settings\npackage:com.google.android.youtube\n")
        installed, pkg = self.service.is_tv_agent_installed()
        self.assertFalse(installed)
        self.assertIsNone(pkg)

    def test_start_tv_agent_success(self):
        self.mock_adb.shell.side_effect = [
            (True, "package:com.azefsw.audioconnect"),
            (True, "Events injected: 1\n## Network stats: elapsed time=12ms")
        ]
        ok, msg = self.service.start_tv_agent()
        self.assertTrue(ok)
        self.assertIn("Agent audio lancé", msg)

    def test_start_tv_agent_not_installed(self):
        self.mock_adb.shell.return_value = (True, "")
        ok, msg = self.service.start_tv_agent()
        self.assertFalse(ok)
        self.assertIn("n'est pas encore installé", msg)

    def test_open_playstore_on_tv(self):
        self.mock_adb.shell.return_value = (True, "Starting: Intent...")
        ok, msg = self.service.open_playstore_on_tv()
        self.assertTrue(ok)
        self.assertIn("Play Store", msg)

    @patch("os.path.exists")
    def test_locate_pc_client_found(self, mock_exists):
        mock_exists.side_effect = lambda p: "Program Files" in p
        path = self.service.locate_pc_client()
        self.assertIsNotNone(path)
        self.assertIn("AudioRelay.exe", path)


if __name__ == "__main__":
    unittest.main()

