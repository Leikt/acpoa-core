import importlib.util
import os

from src.core.configuration import Configuration
from src.core.singleton import Singleton


class PluginInstaller(metaclass=Singleton):
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
        result = os.system(f"python3 -m pip -q install {package}")
        if result > 0: raise Exception(f"Package '{package}' can't be installed. Pip returned error core : {result}")

        if not self._plugins_config.has_section(package):
            self._plugins_config.add_section(package)
            self._plugins_config.set(package, 'enabled', self._plugin_eoi)
            self._plugins_config.save()

    def remove(self, package: str):
        result = os.system(f"python3 -m pip -q uninstall -y {package}")
        if result > 0: raise Exception(f"Package '{package}' can't be removed. Pip returned error core : {result}")

        if self._plugins_config.has_section(package):
            self._plugins_config.remove_section(package)
            self._plugins_config.save()

    def update(self, package: str):
        if importlib.util.find_spec(package) is None:
            raise Exception(f"Package '{package}' is not installed therefore it can't be freshened.")

        result = os.system(f"python3 -m pip -q install --upgrade {package}")
        if result > 0: raise Exception(f"Package '{package}' can't be updated. Pip returned error core : {result}")

    def add_repository(self, name: str, index: str, editable: bool = False):
        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        if self._config.has_section(section):
            raise Exception(f"Repository {name} already is registered. Use modify_repository to update its data.")

        self._config.add_section(section)
        self._config.set(section, 'enabled', self._repo_eoi)
        self._config.set(section, 'index', index)
        self._config.setboolean(section, 'editable', editable)

    def remove_repository(self, name: str):
        pass

    def search(self, exp: str):
        pass

    class Repository:
        def __init__(self, index: str):
            self._index = index
