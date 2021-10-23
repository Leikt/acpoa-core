import configparser
import os.path
import shutil

from .singleton import Singleton
from .handler import Handler, CumulativeHandler


class Core(metaclass=Singleton):
    """Manage communication between the different plugins and provide essentials application interface."""

    ACPOA_CFG_DEFAULT = "defaults/acpoa.cfg"
    PLUGINS_CFG_DEFAULT = "defaults/plugins.cfg"
    ACPOA_CFG = "cfg/acpoa.cfg"
    PLUGINS_CFG = "cfg/plugins.cfg"

    class Status:
        INITIALIZED = 1
        LOADED = 2
        RUNNING = 3
        TERMINATED = 4

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

    def run(self):
        """Start the application by calling the the 'run' handler.

        :raise Exception: if this method is called before load."""
        if self._status < Core.Status.LOADED:
            raise Exception("Core.run called before Core.load.")
        self._status = Core.Status.RUNNING

    def quit(self):
        self._status = Core.Status.TERMINATED

    def fetch(self, name: str, klass: object) -> Handler:
        """Get the handler with the given name.

        :param name: name of the handler
        :param klass: klass of the handler
        :raise TypeError: if the handler exists but with a difference class OR if
        the klass parameter is not a valid Handler subclass
        :return: the requested handler"""

        handler = self._handlers.get(name, None)
        # Attempt to get
        if handler is not None:
            if type(handler) == klass:
                return handler
            raise TypeError(f"Existing handler named '{name}' <{type(self._handlers[name]).__name__}>, "
                            f"you are trying to get a <{klass.__name__}> handler")
        # Attempt to create
        allowed_handlers = Handler.__subclasses__()
        if klass in allowed_handlers:
            self._handlers[name] = klass(name)
            return self._handlers[name]
        raise TypeError(f"Handler class {klass} doesn't exists. It must be one of {allowed_handlers}")

    def remove(self):
        pass

    def execute(self):
        pass

    def register(self):
        pass

    def unregister(self):
        pass

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
        self.fetch('run', CumulativeHandler)
        self.fetch('quit', CumulativeHandler)
