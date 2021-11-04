import importlib.util
import os

from src.core.configuration import Configuration
from src.core.singleton import Singleton


class PluginInstaller(metaclass=Singleton):
    def __init__(self, config_fname: str, plugin_config_fname: str):
        self._config = Configuration.open(config_fname)
        self._plugins_config = Configuration.open(plugin_config_fname)
        self._repositories = []
        self._enable_on_installation = self._config.get('plugins', 'enable-on-installation')

    def install(self, package: str):
        result = os.system(f"python3 -m pip -q install {package}")
        if result > 0: raise Exception(f"Package '{package}' can't be installed. Pip returned error core : {result}")

        if not self._plugins_config.has_section(package):
            self._plugins_config.add_section(package)
            self._plugins_config.set(package, 'enabled', self._enable_on_installation)
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

    def add_repository(self, name: str, index: str = None):
        pass

    def remove_repository(self, name: str):
        pass

    def search(self, exp: str):
        pass

    class Repository:
        def __init__(self, index: str):
            self._index = index
