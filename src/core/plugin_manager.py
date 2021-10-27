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
        """:todo: create acpoa client to install package"""
        pass

    def update(self):
        """:todo: needs acpo client"""
        pass

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
        :return: whether or not the plugin is enabled"""

    def _set(self, package: str, state: bool):
        """Change the enabled state of the given plugin.

        :param package: package to enable
        :raise FileNotFoundError: the plugin is not in the plugins.cfg file"""
        if not self._plugins_config.has_section(package):
            raise FileNotFoundError(f"The plugin {package} is not inside plugins.cfg\n"
                                    f"Possible causes: bad spelling, not installed, deleted by hand.")
        self._plugins_config.set(package, 'enabled', str(state))
        self._plugins_config.save()
