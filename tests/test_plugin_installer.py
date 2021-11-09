import os.path
import shutil
import unittest

from src.core.plugin_installer import PluginInstaller


class TestPluginInstaller(unittest.TestCase):
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
        acpoa_cfg = os.path.join('test_plugin_installer', 'install_remove', 'acpoa.cfg')
        plugins_cfg = os.path.join('test_plugin_installer', 'install_remove', 'plugins.cfg')
        self.copy_files(acpoa_cfg, plugins_cfg)
        package = 'requests'
        non_existing_package = 'do_not_exist'
        pi = PluginInstaller(acpoa_cfg, plugins_cfg)

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
        acpoa_cfg = os.path.join('test_plugin_installer', 'update', 'acpoa.cfg')
        plugins_cfg = os.path.join('test_plugin_installer', 'update', 'plugins.cfg')
        self.copy_files(acpoa_cfg, plugins_cfg)
        package = 'requests'
        non_existing_package = 'do_not_exist'
        pi = PluginInstaller(acpoa_cfg, plugins_cfg)
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

    def test_repository_add_has_remove(self):
        # Initialize data and objects
        acpoa_cfg = os.path.join('test_plugin_installer', 'repo_add_remove', 'acpoa.cfg')
        plugins_cfg = os.path.join('test_plugin_installer', 'repo_add_remove', 'plugins.cfg')
        self.copy_files(acpoa_cfg, plugins_cfg)
        repo = 'new_repo'
        non_existing_package = 'do_not_exist'
        pi = PluginInstaller(acpoa_cfg, plugins_cfg)

        try:
            pi.remove_repository(repo)
            assert not pi.has_repository(repo)
            pi.add_repository(repo, 'https://dummy.com')
            assert pi.has_repository(repo)
            pi.remove_repository(repo)
            assert not pi.has_repository(repo)
            # Test the different ways of boolean editable
            pi.add_repository(repo, 'https://dummy2.com', editable='no')
            self.assertWarns(Warning, pi.add_repository, repo, 'https://dummy2.com')
            pi.remove_repository(repo)
            pi.add_repository(repo, 'https://dummy2.com', editable=True)
            pi.remove_repository(repo)
        except:
            raise
        finally:
            self.clean_files(acpoa_cfg, plugins_cfg)

    def test_remote_repository(self):
        # Initialize data and objects
        acpoa_cfg = os.path.join('test_plugin_installer', 'repo_add_remove', 'acpoa.cfg')
        plugins_cfg = os.path.join('test_plugin_installer', 'repo_add_remove', 'plugins.cfg')
        self.copy_files(acpoa_cfg, plugins_cfg)
        non_existing_package = 'do_not_exist'
        pi = PluginInstaller(acpoa_cfg, plugins_cfg)
        server = "http://localhost:8080"
        index = f"{server}/simple/"
        repo = 'localhost'
        pack = 'mystring'

        try:
            # Tests
            pi.add_repository(repo, index)
            pi.install(pack)
            assert pi.is_installed(pack)
            show = __import__(pack).show
            assert show('you', 'only', 'live', 'once') == 'you only live once'
            pi.remove(pack)
            pi.remove_repository(repo)
        except:
            print("Server may be down.")
            raise
        finally:
            self.clean_files(acpoa_cfg, plugins_cfg)

    def test_no_repo(self):
        # Initialize data and objects
        acpoa_cfg = os.path.join('test_plugin_installer', 'no_repo', 'acpoa.cfg')
        plugins_cfg = os.path.join('test_plugin_installer', 'no_repo', 'plugins.cfg')
        self.copy_files(acpoa_cfg, plugins_cfg)
        pi = PluginInstaller(acpoa_cfg, plugins_cfg)

        try:
            self.assertRaises(Exception, pi.install, 'something')
            self.assertRaises(Exception, pi.update, 'something')
        except:
            raise
        finally:
            self.clean_files(acpoa_cfg, plugins_cfg)
