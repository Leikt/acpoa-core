import unittest

from src.core import Core, CumulativeHandler
from src.core import DecorativeHandler

class NonExistant:
    pass

class TestCore(unittest.TestCase):
    def test_core_singleton(self):
        a = Core()
        b = Core()
        assert id(a) == id(b)

    def test_core_exceptions(self):
        core = Core()
        self.assertRaises(Exception, core.run)

    def test_core_status(self):
        core = Core()
        assert core.status == core.Status.INITIALIZED
        core.load()
        assert core.status == core.Status.LOADED
        core.run()
        assert core.status == core.Status.RUNNING
        core.quit()
        assert core.status == core.Status.TERMINATED

    def test_core_fetch(self):
        core = Core()
        assert type(core.fetch('test', DecorativeHandler)) == DecorativeHandler  # Create
        assert type(core.fetch('test', DecorativeHandler)) == DecorativeHandler  # Get
        self.assertRaises(TypeError, core.fetch, 'test', CumulativeHandler)  # Get the wrong type
        self.assertRaises(TypeError, core.fetch, 'wrong', NonExistant) # Not a handler class
