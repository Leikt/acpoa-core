import importlib.util
import os

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
        self._repositories = []
        self._plugin_eoi = self._config.get(self._ACPOA_CFG_SECTION_PLUGINS, 'enable-on-installation')
        self._repo_eoi = self._config.get(self._ACPOA_CFG_SECTION_REPOSITORIES, 'enable-on-installation')

    def install(self, package: str):
        """Install the given plugin from the repositories

        :param package: name of the plugin to install
        :raise Exception: if the package couldn't be installed. Provides pip error code."""

        result = os.system(f"python3 -m pip -q install {package}")
        if result > 0: raise Exception(f"Package '{package}' can't be installed. Pip returned error core : {result}")

        if not self._plugins_config.has_section(package):
            self._plugins_config.add_section(package)
            self._plugins_config.set(package, 'enabled', self._plugin_eoi)
            self._plugins_config.save()

    def remove(self, package: str):
        """Uninstall the given package.

        :param package: name of the plugin to install
        :raise Exception: if the package couldn't be uninstalled. Provides pip error code."""

        result = os.system(f"python3 -m pip -q uninstall -y {package}")
        if result > 0: raise Exception(f"Package '{package}' can't be removed. Pip returned error core : {result}")

        if self._plugins_config.has_section(package):
            self._plugins_config.remove_section(package)
            self._plugins_config.save()

    def update(self, package: str):
        """Update the plugin. It needs to be installed to be updated.

        :param package: name of the package to update
        :raise Exception: if package couldn't be updated or if the package isn't installed."""

        if importlib.util.find_spec(package) is None:
            raise Exception(f"Package '{package}' is not installed therefore it can't be freshened.")

        result = os.system(f"python3 -m pip -q install --upgrade {package}")
        if result > 0: raise Exception(f"Package '{package}' can't be updated. Pip returned error core : {result}")

    def add_repository(self, name: str, index: str, editable: [bool, str] = False):
        """Add the repository to the list where to search plugins.

        :param name: custom name of the repository
        :param index: url, path to the repository
        :param editable: do the plugins need to be dynamically updated (development usage)
        :raise Exception: if the repository is already registered"""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        if self._config.has_section(section):
            raise Exception(f"Repository {name} already is registered. Use modify_repository to update its data.")

        self._config.add_section(section)
        self._config.set(section, 'enabled', self._repo_eoi)
        self._config.set(section, 'index', index)
        self._config.setboolean(section, 'editable', editable)
        self._config.save()

    def has_repository(self, name) -> bool:
        """Test if the given repository is installed.

        :param name: name of the repository in the config file.
        :return: whether or not the repository is installed."""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        return self._config.has_section(section)

    def remove_repository(self, name: str):
        """Remove the repository from the list.

        :param name: name of the repository to remove"""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        self._config.remove_section(section)
        self._config.save()

    class Repository:
        def __init__(self, index: str):
            self._index = index
