########################################################################################################################
# ACPOA - HooksHandler                                                                                                 #
# -------------------------------------------------------------------------------------------------------------------- #
# Author : Leikt                                                                                                       #
# Author email : leikt.solreihin@gmail.com                                                                             #
########################################################################################################################
import warnings


class HooksHandler:
    """Handle a collection of hooks."""

    def __init__(self, name: str):
        self._hooks = []
        self._name = name

    @property
    def name(self) -> str:
        """Name of the handler.

        :return: the name of the handler"""

        return self._name

    def register(self, name: str, method: callable, priority: int = 0):
        """Add a hook to the manager, will call *method* when its triggered

        :param name: name the hook, will be used to identify hooks
        :param method: callable called when the handler is triggered
        :param priority: used to sort hooks execution order
        :raises NameError: when the hook already exists"""

        if any(hook.name == name for hook in self._hooks):
            raise NameError(f"Trying to add an new hook named '{name}' but it already exists.")
        hook = Hook(name, method, priority)
        self._hooks.append(hook)
        self._hooks.sort(key=lambda h: h.priority, reverse=True)  # higher priority, higher in the list

    def remove(self, name: str):
        """Remove a hook from the handler. Its method won't be called next execution.

        :param name: name of the hook
        :raise KeyError: if the hook doesn't exists"""

        hook = next(filter(lambda h: h.name == name, self._hooks), None)
        if hook is None:
            raise KeyError("No hook named '{name}'.")
        self._hooks.remove(hook)

    def execute(self, *args, **kwargs) -> any:
        raise NotImplementedError()


class DecorativeHooksHandler(HooksHandler):
    def execute(self, *args, **kwargs) -> any:
        if len(kwargs) > 0:
            raise Exception(f"{self.__class__.__name__} does not take key arguments.")
        multiple_args = len(args) > 1
        for hook in self._hooks:
            args = hook(*args)
            if not multiple_args: args = [args]
        if not multiple_args: args = args[0]
        return args


class CumulativeHooksHandler(HooksHandler):
    def execute(self, *args, **kwargs) -> any:
        return [hook(*args, **kwargs) for hook in self._hooks]


class UniqueHooksHandler(HooksHandler):
    def register(self, name: str, method: callable, priority: int = 0):
        if len(self._hooks) > 0:
            if self._hooks[0].priority >= priority:
                warnings.warn(f"Other(s) hook in this UniqueHooksHandler. Hook '{name}' "
                              f"added won't be executed.", Warning)
            else:
                warnings.warn(f"Other(s) hook in this UniqueHooksHandler. Hook '{name}' "
                              f"has higher priority, it will shadow others.", )
        super().register(name, method, priority)

    def execute(self, *args, **kwargs) -> any:
        return self._hooks[0](*args, **kwargs)


class Hook:
    def __init__(self, name: str, method: callable, priority: int):
        self._name = name
        self._method = method
        self._priority = priority

    @property
    def name(self):
        return self._name

    @property
    def priority(self):
        return self._priority

    def __call__(self, *args, **kwargs) -> any:
        return self._method(*args, **kwargs)
