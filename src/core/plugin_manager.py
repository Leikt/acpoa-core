import importlib.util
import warnings

from src.core.configuration import Configuration
from src.core.repository_manager import RepositoryManager, Repository


class PluginManager:
    """Help the installation of plugins and repositories."""

    _ACPOA_CFG_SECTION_PLUGINS = 'plugins'

    def __init__(self, config_fname: str, plugin_config_fname: str):
        self._config = Configuration.open(config_fname)
        self._plugins_config = Configuration.open(plugin_config_fname)
        self._plugin_eoi = self._config.get(self._ACPOA_CFG_SECTION_PLUGINS, 'enable-on-installation')
        self._repository_manager = RepositoryManager(config_fname)

    def install(self, package: str):
        """Install the given plugin from the repositories

        :param package: name of the plugin to install
        :raise Exception: if the package couldn't be installed. Provides pip error code."""

        if self._repository_manager.count == 0:
            raise Exception("There is no repository registered or enabled.")
        if self.is_installed(package):
            warnings.warn(Warning(f"Package '{package}' is already installed."))
            return

        for repo in self._repository_manager.each():
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

        result = Repository.remove(package)
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
        if self._repository_manager.count == 0:
            raise Exception("There is no repository registered or enabled.")

        for repo in self._repository_manager.each():
            result = repo.upgrade(package)
            if result == 0: break
        if result > 0: raise Exception(f"Package '{package}' can't be updated. Pip returned error core : {result}")

    def is_installed(self, package: str) -> bool:
        """Test if the given plugin is installed

        :param package: name of the plugin to test
        :return: whether or not the plugin is installed"""

        res = importlib.util.find_spec(package)
        return res is not None

    def is_enabled(self, package: str) -> bool:
        pass

    def load(self) -> list:
        return []
