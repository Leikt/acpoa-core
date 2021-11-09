import os.path
import shutil
import unittest

from src.core.plugin_manager import PluginManager


class TestPluginManager(unittest.TestCase):
    @staticmethod
    def copy_files(*files):
        for fname in files:
            shutil.copy(fname + '.def', fname)

    @staticmethod
    def clean_files(*files):
        for fname in files:
            os.remove(fname)

    def test_install_remove(self):
        # Initialize data and objects
        acpoa_cfg = os.path.join('test_plugin_manager', 'install_remove', 'acpoa.cfg')
        plugins_cfg = os.path.join('test_plugin_manager', 'install_remove', 'plugins.cfg')
        self.copy_files(acpoa_cfg, plugins_cfg)
        package = 'dice'
        non_existing_package = 'do_not_exist'
        pi = PluginManager(acpoa_cfg, plugins_cfg)

        # Tests
        try:
            # Clean previous failed test
            if pi.is_installed(package):
                pi.remove(package)
            # Test normal installation
            pi.install(package)
            assert pi.is_installed(package)
            # Test install installed package
            self.assertWarns(Warning, pi.install, package)
            # Test normal remove
            pi.remove(package)
            assert not pi.is_installed(package)
            # Test remove uninstalled package
            self.assertRaises(ModuleNotFoundError, pi.remove, package)
            # Test install non existing package
            self.assertRaises(Exception, pi.install, non_existing_package)
        except:
            raise
        finally:
            self.clean_files(acpoa_cfg, plugins_cfg)

    def test_update(self):
        # Initialize data and objects
        acpoa_cfg = os.path.join('test_plugin_manager', 'update', 'acpoa.cfg')
        plugins_cfg = os.path.join('test_plugin_manager', 'update', 'plugins.cfg')
        self.copy_files(acpoa_cfg, plugins_cfg)
        package = 'dice'
        non_existing_package = 'do_not_exist'
        pi = PluginManager(acpoa_cfg, plugins_cfg)
        if pi.is_installed(package): pi.remove(package)
        os.system(f"pip install {package}==2.0.0")

        # Tests
        try:
            # Test normal update
            pi.update(package)
            # Cannot test if update works because python need to be restart in order to take update into account
            # Test update not existing package
            self.assertRaises(Exception, pi.update, non_existing_package)
            # Test update not installed package
            pi.remove(package)
            pi.update(package)
            assert pi.is_installed(package)
        except:
            raise
        finally:
            self.clean_files(acpoa_cfg, plugins_cfg)

    def test_no_repo(self):
        # Initialize data and objects
        acpoa_cfg = os.path.join('test_plugin_manager', 'no_repo', 'acpoa.cfg')
        plugins_cfg = os.path.join('test_plugin_manager', 'no_repo', 'plugins.cfg')
        self.copy_files(acpoa_cfg, plugins_cfg)
        pi = PluginManager(acpoa_cfg, plugins_cfg)

        try:
            self.assertRaises(Exception, pi.install, 'something')
            self.assertRaises(Exception, pi.update, 'something')
        except:
            raise
        finally:
            self.clean_files(acpoa_cfg, plugins_cfg)
