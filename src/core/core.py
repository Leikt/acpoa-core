########################################################################################################################
# ACPOA - Core                                                                                                         #
# -------------------------------------------------------------------------------------------------------------------- #
# Author : Leikt                                                                                                       #
# Author email : leikt.solreihin@gmail.com                                                                             #
########################################################################################################################

import configparser
import os.path
import shutil

from .hookshandler import HooksHandler, CumulativeHooksHandler
from .singleton import Singleton


class Core(metaclass=Singleton):
    """Manage communication between the different plugins and provide essential application interface."""

    ACPOA_CFG_DEFAULT = "defaults/acpoa.cfg"
    PLUGINS_CFG_DEFAULT = "defaults/plugins.cfg"
    ACPOA_CFG = "cfg/acpoa.cfg"
    PLUGINS_CFG = "cfg/plugins.cfg"

    class Status:
        INITIALIZED = 1
        LOADED = 2
        RUNNING = 3
        QUTTING = 4

    def __init__(self):
        # Initialize configuration files if needed
        if not os.path.isfile(Core.ACPOA_CFG):
            Core._copy_default(self.ACPOA_CFG_DEFAULT, self.ACPOA_CFG)
        if not os.path.isfile(Core.PLUGINS_CFG):
            Core._copy_default(self.PLUGINS_CFG_DEFAULT, self.PLUGINS_CFG)
        # Read the configuration file
        self._config = configparser.ConfigParser()
        self._config.read(Core.ACPOA_CFG)
        # Initialize
        # self._plugin_manager = PluginManager(self.PLUGINS_CFG)
        self._handlers = {}
        self._init_handlers()
        self._status = Core.Status.INITIALIZED

    def load(self):
        """Manage the plugins according to configuration file acpoa.cfg then load the plugins from plugins.cfg."""
        self._status = Core.Status.LOADED

    def run(self, argv: list = []):
        """Start the application by calling the the 'run' handler.

        :raise Exception: if this method is called before load."""
        if self._status < Core.Status.LOADED:
            raise Exception("Core.run called before Core.load")
        self._status = Core.Status.RUNNING
        self.execute('run', *argv)

    def quit(self):
        """Start the exit sequence and close the application."""
        self._status = Core.Status.QUTTING
        self.execute('quit')

    def fetch(self, name: str, klass: callable = None) -> HooksHandler:
        """Get the handler with the given name. Create it if it does not exist.

        :param name: name of the handler
        :param klass: klass of the handler
        :raise TypeError: if the handler exists but with a difference class OR if
        the klass parameter is not a valid Handler subclass
        :return: the requested handler"""

        handler = self._handlers.get(name, None)
        if handler is not None and klass is not None and type(handler) != klass:
            raise TypeError(f"Existing handler named '{name}' <{type(self._handlers[name]).__name__}>, "
                            f"you are trying to get a <{klass.__name__}>")
        if handler is None and klass not in HooksHandler.__subclasses__():
            raise TypeError(f"Handler class {klass} doesn't exists. It must be one of {HooksHandler.__subclasses__()}")
        if handler is None: self._handlers[name] = klass(name)
        return self._handlers[name]

    def remove(self, name: str):
        """Remove handler if it exists

        :param name: name the handler to remove
        :raise KeyError: if the handler doesn't exists"""
        if name not in self._handlers:
            raise KeyError(f"No handler named '{name}'")
        del self._handlers[name]

    def execute(self, name: str, *args, **kwargs) -> any:
        """Execute the hooks

        :param name: name of the hook handler
        :raise KeyError: if the name matches no hook handler
        :return: execution result"""
        if name not in self._handlers:
            raise KeyError(f"There is no handler named '{name}'")
        return self._handlers[name].execute(*args, **kwargs)

    def register(self, hh_name: str, hook_name: str, method: callable, priority: int = 0, hh_class: callable = None):
        """Register a hook. It will attempt to create the hook handler if it doesn't exist.

        :param hh_name: name of the handler
        :param hook_name: name of the hook
        :param method: callable that the hook will call
        :param priority: priority of the hook
        :param hh_class: class of the hook handler"""
        hook_handler = self.fetch(hh_name, hh_class)
        hook_handler.register(hook_name, method, priority)

    def unregister(self, hh_name: str, hook_name: str):
        """Remove a hook.

        :param hh_name: name of the hook handler where to remove the hook.
        :param hook_name: name of hook to remove.
        :raise KeyError: if the handlers isn't registred"""
        if hh_name in self._handlers:
            self._handlers[hh_name].remove(hook_name)
        else:
            raise KeyError(f"There is no hook handler named '{hh_name}'")

    @property
    def status(self):
        return self._status

    @staticmethod
    def _copy_default(src, dst):
        print(f"No file found at '{dst}'.")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        default_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), src)
        shutil.copyfile(default_path, dst)
        print(f"File copied from default to '{dst}'.")

    def _init_handlers(self):
        self.fetch('run', CumulativeHooksHandler)
        self.fetch('quit', CumulativeHooksHandler)
