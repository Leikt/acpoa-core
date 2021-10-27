import os.path
import unittest

from src.core.plugin_manager import PluginManager


class TestPluginManager(unittest.TestCase):
    def setUp(self) -> None:
        cfg_dir = os.path.join(os.path.dirname(__file__), 'cfg')
        self.pm = PluginManager(os.path.join(cfg_dir, 'acpoa.cfg'), os.path.join(cfg_dir, 'plugins.cfg'))

    def test_install(self):
        self.pm.install("requests")
        self.assertRaises(Exception, self.pm.install, "oeijgzrhtp6hd45hdthrf6rsdb13fv1db56489db4")
