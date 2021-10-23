class Handler:
    def __init__(self, name):
        self._hooks = []


class DecorativeHandler(Handler):
    pass


class CumulativeHandler(Handler):
    pass


class UniqueHandler(Handler):
    pass
