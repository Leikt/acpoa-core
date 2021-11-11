import os.path
import shutil
import unittest

from src.acpoa import RepositoryManager


class TestPluginInstaller(unittest.TestCase):
    _DIR = 'test_repository_manager'

    @staticmethod
    def copy_files(*files):
        for fname in files:
            shutil.copy(fname + '.def', fname)

    @staticmethod
    def clean_files(*files):
        for fname in files:
            os.remove(fname)

    def test_installation(self):
        # Initialize data and objects
        acpoa_cfg = os.path.join(self._DIR, 'installation', 'acpoa.cfg')
        plugins_cfg = os.path.join(self._DIR, 'installation', 'plugins.cfg')
        self.copy_files(acpoa_cfg, plugins_cfg)
        repo = 'new_repo'
        non_existing_package = 'do_not_exist'
        rm = RepositoryManager(acpoa_cfg)

        try:
            rm.remove(repo)
            assert not rm.is_installed(repo)
            rm.add(repo, 'https://dummy.com')
            assert rm.is_installed(repo)
            rm.remove(repo)
            assert not rm.is_installed(repo)
            # Test the different ways of boolean editable
            rm.add(repo, 'https://dummy2.com', editable='no')
            self.assertWarns(Warning, rm.add, repo, 'https://dummy2.com')
            rm.remove(repo)
            rm.add(repo, 'https://dummy2.com', editable=True)
            rm.remove(repo)
        except:
            raise
        finally:
            self.clean_files(acpoa_cfg, plugins_cfg)

    def test_remote(self):
        # Initialize data and objects
        acpoa_cfg = os.path.join(self._DIR, 'remote', 'acpoa.cfg')
        plugins_cfg = os.path.join(self._DIR, 'remote', 'plugins.cfg')
        self.copy_files(acpoa_cfg, plugins_cfg)
        rm = RepositoryManager(acpoa_cfg)

        try:
            for repo in rm.each():
                assert repo.is_reachable()
            rm.add('not_reachable', 'not_reachable')
            repo = [r for r in rm.each()][-1]
            assert not repo.is_reachable()
        except:
            print("Server may be down.")
            raise
        finally:
            self.clean_files(acpoa_cfg, plugins_cfg)

    def test_activation(self):
        # Initialize data and objects
        acpoa_cfg = os.path.join(self._DIR, 'activation', 'acpoa.cfg')
        plugins_cfg = os.path.join(self._DIR, 'activation', 'plugins.cfg')
        self.copy_files(acpoa_cfg, plugins_cfg)
        rm = RepositoryManager(acpoa_cfg)

        try:
            assert rm.is_installed('localhost')
            assert rm.is_installed('pypi')
            assert not rm.is_installed('no_repo')
            assert rm.is_enabled('localhost')
            assert not rm.is_enabled('pypi')
            assert not rm.is_enabled('no_repo')

            # Disable a repo
            rm.disable('localhost')
            assert rm.is_installed('localhost')
            assert not rm.is_enabled('localhost')
            rm.enable('pypi')
            assert rm.is_installed('pypi')
            assert rm.is_enabled('pypi')
        except:
            raise
        finally:
            self.clean_files(acpoa_cfg, plugins_cfg)
