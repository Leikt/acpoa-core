import warnings

from .configuration import Configuration
from .plugin_base import PluginBase


class PluginManager:
    """Manage plugins"""

    def __init__(self, config_fname: str, plugin_config_fname: str):
        self._config = Configuration.open(config_fname)
        self._plugins_config = Configuration.open(plugin_config_fname)

    def load(self) -> list[PluginBase]:
        """:todo: create sample plugins, install them, then put them inside plugin.cfg"""
        pass

    def install(self, package: str):
        """Install the given package in the project

        :param package: name of the package to install
        :raise NameError: if the package doesn't exists inside the repositories"""
        if self._plugins_config.has_section(package):
            warnings.warn(f"The package {package} is already installed, if you want to update it, call the update "
                          f"method.")
            return
        # Call the clients to install the package
        # Update the plugin configuration
        self._plugins_config.add_section(package)
        self.disable(package)

    def remove(self, package: str):
        """Remove the given package from the project

        :param package: name of the package to remove"""
        if not self._plugins_config.has_section(package):
            warnings.warn(f"The package {package} is not installed method.")
            return
        # Remove package with pip
        # os.system(f"python3 -m pip uninstall {package}")
        # Update the plugin configuration
        self._plugins_config.remove_section(package)
        self._plugins_config.save()

    def update(self):
        """:todo: needs acpo client"""
        pass

    def is_installed(self, package: '') -> bool:
        """Test if a package is installed.

        :param package: name of the package to test
        :return: whether or not the package is installed"""
        return self._plugins_config.has_section(package)

    def enable(self, package: str):
        """Activate a plugin, it will be loaded when the method load is called.

        :param package: package to enable
        :raise FileNotFoundError: the plugin is not in the plugins.cfg file"""
        self._set(package, True)

    def disable(self, package: str):
        """Activate a plugin, it will be loaded when the method load is called.

        :param package: name of the package to enable
        :raise FileNotFoundError: the plugin is not in the plugins.cfg file"""
        self._set(package, False)

    def is_enabled(self, package: str) -> bool:
        """Test if a plugin is enabled.

        :param package: name of the plugin to test
        :return: whether or not the plugin is enabled
        :raise KeyError: the plugin is not in the plugins.cfg file"""
        if not self._plugins_config.has_section(package):
            raise KeyError(f"The plugin {package} is not inside plugins.cfg\n"
                           f"Possible causes: bad spelling, not installed, deleted by hand.")
        return self._plugins_config.getboolean(package, 'enabled')

    def _set(self, package: str, state: bool):
        """Change the enabled state of the given plugin.

        :param package: package to enable
        :raise KeyError: the plugin is not in the plugins.cfg file"""
        if not self._plugins_config.has_section(package):
            raise KeyError(f"The plugin {package} is not inside plugins.cfg\n"
                           f"Possible causes: bad spelling, not installed, deleted by hand.")
        value = 'yes' if state else 'no'
        self._plugins_config.set(package, 'enabled', value)
        self._plugins_config.save()
