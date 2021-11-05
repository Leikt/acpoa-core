import importlib.util
import os.path
import unittest

from src.core.plugin_installer import PluginInstaller


class TestPluginInstaller(unittest.TestCase):
    ACPO_TEST_CONF = os.path.join('test_plugin_installer', 'acpoa.cfg')
    PLUGIN_TEST_CONF = os.path.join('test_plugin_installer', 'plugins.cfg')

    def test_install_remove(self):
        pi = PluginInstaller(self.ACPO_TEST_CONF, self.PLUGIN_TEST_CONF)
        package = 'requests'
        pi.remove(package)
        assert importlib.util.find_spec(package) is None
        pi.install(package)
        assert importlib.util.find_spec(package) is not None
        pi.remove(package)
        assert importlib.util.find_spec(package) is None
        package = 'package_does_not_exist'
        self.assertRaises(Exception, pi.install, package)

    def test_update(self):
        pi = PluginInstaller(self.ACPO_TEST_CONF, self.PLUGIN_TEST_CONF)
        package = 'requests'
        pi.install(package)
        pi.update(package)
        # Test exception
        pi.remove(package)
        self.assertRaises(Exception, pi.update, package)
        self.assertRaises(Exception, pi.update, 'package_does_not_exist')

    def test_repository_add_has_remove(self):
        pi = PluginInstaller(self.ACPO_TEST_CONF, self.PLUGIN_TEST_CONF)
        repo = 'new_repo'
        pi.remove_repository(repo)
        assert not pi.has_repository(repo)
        pi.add_repository(repo, 'https://dummy.com')
        assert pi.has_repository(repo)
        pi.remove_repository(repo)
        assert not pi.has_repository(repo)
        # Test the different ways of boolean editable
        pi.add_repository(repo, 'https://dummy2.com', editable='no')
        pi.remove_repository(repo)
        pi.add_repository(repo, 'https://dummy2.com', editable=True)
        pi.remove_repository(repo)
