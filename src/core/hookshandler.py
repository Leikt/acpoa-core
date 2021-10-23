class HooksHandler:
    def __init__(self, name: str):
        self._hooks = []
        self._name = name

    @property
    def name(self) -> str:
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


class DecorativeHooksHandler(HooksHandler):
    pass


class CumulativeHooksHandler(HooksHandler):
    pass


class UniqueHooksHandler(HooksHandler):
    # Should raise error / warning if trying to add hook but there is one
    pass


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
