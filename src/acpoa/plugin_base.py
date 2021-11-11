class PluginBase:
    def __init__(self):
        pass

    def register_hooks(self) -> list[tuple]:
        """Register the hooks in the Core. Each child class must implement this method. The returns is a list of
        tuples (handler_name, hook_name, callable, handler_type) where :

        - handler_name is the name of the handler
        - hook_name is the name of the hook (it must be unique)
        - callable is the method/function called by the hook
        - handler_type is one of :

            - acpoa.CumulativeHookHandler
            - acpoa.UniqueHooksHandler
            - acpoa.DecorativeHooksHandler

        :return: list of tuple (handler, hook, function, handler_type)"""

        raise NotImplemented
