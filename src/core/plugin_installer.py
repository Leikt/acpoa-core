import importlib.util
import os
import warnings

from src.core.configuration import Configuration
from src.core.singleton import Singleton


class PluginInstaller(metaclass=Singleton):
    """Help the installation of plugins and repositories."""

    _ACPOA_CFG_SECTION_REPO = 'repo'
    _ACPOA_CFG_SECTION_PLUGINS = 'plugins'
    _ACPOA_CFG_SECTION_REPOSITORIES = 'repositories'

    def __init__(self, config_fname: str, plugin_config_fname: str):
        self._config = Configuration.open(config_fname)
        self._plugins_config = Configuration.open(plugin_config_fname)
        self._repositories = self._load_repositories()
        self._plugin_eoi = self._config.get(self._ACPOA_CFG_SECTION_PLUGINS, 'enable-on-installation')
        self._repo_eoi = self._config.get(self._ACPOA_CFG_SECTION_REPOSITORIES, 'enable-on-installation')

    def install(self, package: str):
        """Install the given plugin from the repositories

        :param package: name of the plugin to install
        :raise Exception: if the package couldn't be installed. Provides pip error code."""

        if len(self._repositories) == 0:
            raise Exception("There is no repository registered or enabled.")
        if self.is_installed(package):
            warnings.warn(Warning(f"Package '{package}' already installed."))
            return

        for repo in self._repositories:
            result = repo.install(package)
            if result == 0: break
        if result > 0: raise Exception(f"Package '{package}' can't be installed. Pip returned error core : {result}")

        if not self._plugins_config.has_section(package):
            self._plugins_config.add_section(package)
            self._plugins_config.set(package, 'enabled', self._plugin_eoi)
            self._plugins_config.save()

    def remove(self, package: str):
        """Uninstall the given package.

        :param package: name of the plugin to install
        :raise ModuleNotFoundError: if the package isn't installed.
        :raise Exception: if the package couldn't be uninstalled. Provides pip error code."""

        if not self.is_installed(package):
            raise ModuleNotFoundError(f"Package '{package}' is not installed.")

        result = self.Repository.remove(package)
        if result > 0: raise Exception(f"Package '{package}' can't be removed. Pip returned error core : {result}")

        if self._plugins_config.has_section(package):
            self._plugins_config.remove_section(package)
            self._plugins_config.save()

    def update(self, package: str):
        """Update the plugin. It needs to be installed to be updated. It needs to be restarted to
        take upgrade into account.

        :param package: name of the package to update
        :raise Exception: if package couldn't be updated."""

        # if importlib.util.find_spec(package) is None:
        #     raise Exception(f"Package '{package}' is not installed therefore it can't be updated.")
        if len(self._repositories) == 0:
            raise Exception("There is no repository registered or enabled.")

        for repo in self._repositories:
            result = repo.upgrade(package)
        if result > 0: raise Exception(f"Package '{package}' can't be updated. Pip returned error core : {result}")

    def is_installed(self, package: str) -> bool:
        """Test if the given plugin is installed

        :param package: name of the plugin to test
        :return: whether or not the plugin is installed"""

        res = importlib.util.find_spec(package)
        return res is not None

    def is_enabled(self, package: str) -> bool:
        pass

    def add_repository(self, name: str, index: str, editable: [bool, str] = False):
        """Add the repository to the list where to search plugins.

        :param name: custom name of the repository
        :param index: url, path to the repository
        :param editable: do the plugins need to be dynamically updated (development usage)
        :raise Exception: if the repository is already registered"""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        if self._config.has_section(section):
            warnings.warn(Warning(f"Repository {name} already is registered."))
            return

        self._config.add_section(section)
        self._config.set(section, 'enabled', self._repo_eoi)
        self._config.set(section, 'index', index)
        self._config.setboolean(section, 'editable', editable)
        self._config.save()

        self._repositories = self._load_repositories()

    def remove_repository(self, name: str):
        """Remove the repository from the list.

        :param name: name of the repository to remove"""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        self._config.remove_section(section)
        self._config.save()

        self._repositories = self._load_repositories()

    def has_repository(self, name) -> bool:
        """Test if the given repository is installed.

        :param name: name of the repository in the config file.
        :return: whether or not the repository is installed."""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        return self._config.has_section(section)

    def has_enabled_repository(self, name) -> bool:
        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        if not self._config.has_section(section): return False
        return self._config.getboolean(section, 'enabled')

    def enable_repository(self, name: str):
        """Enable a repository

        :param name: name of the repository"""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        self._config.setboolean(section, 'enabled', True)
        self._config.save()

        self._repositories = self._load_repositories()

    def disable_repository(self, name: str):
        """Disable a repository.

        :param name: name of the repository"""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        self._config.setboolean(section, 'enabled', False)
        self._config.save()

        self._repositories = self._load_repositories()

    def _load_repositories(self):
        repos = []
        for section in self._config.subsections_of(self._ACPOA_CFG_SECTION_REPO):
            if not self._config.getboolean(section, 'enabled'): continue

            index = self._config.get(section, 'index')
            editable = self._config.getboolean(section, 'editable', fallback=False)
            repos.append(self.Repository(index, editable))
        return repos

    class Repository:
        def __init__(self, index: str, editable: bool):
            self._index = index
            self._editable = editable
            self._editable_opt = '-e' if editable else ''

        def install(self, package, upgrade: bool = False) -> int:
            command = f"pip -q install {self._editable_opt} " \
                      f"{'--upgrade' if upgrade else ''} " \
                      f"--no-cache-dir " \
                      f"--index-url {self._index} " \
                      f"{package} "
            return os.system(command)

        def upgrade(self, package):
            return self.install(package, upgrade=True)

        @staticmethod
        def remove(package) -> int:
            result = int(os.system(f"pip -q uninstall -y {package}"))
            os.system('pip -q cache purge')
            return result
