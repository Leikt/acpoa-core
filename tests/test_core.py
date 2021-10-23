import unittest

import src.core.singleton
from src.core import Core, CumulativeHooksHandler, DecorativeHooksHandler, HooksHandler


class NonExistant:
    pass


class CustomHooksHandler(HooksHandler):
    pass


class TestCore(unittest.TestCase):
    def setUp(self) -> None:
        self.core = Core()

    def tearDown(self) -> None:
        Core.delete()

    def test_singleton(self):
        a = Core()
        b = Core()
        assert id(a) == id(b)
        Core.delete()   # Delete existing core
        assert id(a) != id(Core()) # Create a new core

    def test_status_exceptions(self):
        self.assertRaises(Exception, self.core.run)

    def test_status(self):
        core = self.core
        assert core.status == core.Status.INITIALIZED
        core.load()
        assert core.status == core.Status.LOADED
        core.run()
        assert core.status == core.Status.RUNNING
        core.quit()
        assert core.status == core.Status.TERMINATED

    def test_fetch(self):
        core = self.core
        assert type(core.fetch('test', DecorativeHooksHandler)) == DecorativeHooksHandler  # Create
        assert type(core.fetch('test', DecorativeHooksHandler)) == DecorativeHooksHandler  # Get
        self.assertRaises(TypeError, core.fetch, 'test', CumulativeHooksHandler)  # Get the wrong type
        self.assertRaises(TypeError, core.fetch, 'wrong', NonExistant)  # Not a handler class
        assert type(core.fetch('with_custom_handler', CustomHooksHandler)) == CustomHooksHandler
        assert type(core.fetch('with_custom_handler')) == CustomHooksHandler # Whatever the class is
        self.assertRaises(TypeError, core.fetch, 'no_class')

    def test_remove(self):
        core = self.core
        count = len(core._handlers.items())
        core.fetch('test', DecorativeHooksHandler)
        assert len(core._handlers.items()) == (count + 1)
        core.remove('test')
        assert len(core._handlers) == count
