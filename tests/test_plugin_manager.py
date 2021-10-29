import os.path
import unittest

from src.core.plugin_manager import PluginManager


class TestPluginManager(unittest.TestCase):
    def test_set(self):
        cfg_dir = os.path.join(os.path.dirname(__file__), 'cfg')
        pm = PluginManager(os.path.join(cfg_dir, 'acpoa.cfg'), os.path.join(cfg_dir, 'preset_plugins.cfg'))

        for i in range(1, 3):
            name = f"plugin{i}"
            pm.enable(name)
            assert pm.is_enabled(name)
            pm.disable(name)
            assert not pm.is_enabled(name)

        self.assertRaises(KeyError, pm.enable, 'not_installed_package')
        self.assertRaises(KeyError, pm.disable, 'not_installed_package')
        self.assertRaises(KeyError, pm.is_enabled, 'not_installed_package')

    def test_install(self):
        cfg_dir = os.path.join(os.path.dirname(__file__), 'cfg')
        pm = PluginManager(os.path.join(cfg_dir, 'acpoa.cfg'), os.path.join(cfg_dir, 'plugins.cfg'))

        name = 'plugin10'
        pm.install(name)
        assert pm.is_installed(name)
        self.assertWarns(Warning, pm.install, name)  # Already installed warning
        pm.remove(name)
        assert not pm.is_installed(name)

        # self.assertRaises(NameError, pm.install, 'does_not_exist')
        self.assertWarns(Warning, pm.remove, 'does_not_exist')
