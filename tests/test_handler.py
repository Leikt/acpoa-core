import unittest

from src.core import HooksHandler


class TestHandler(unittest.TestCase):

    def test_handler_name(self):
        handler = HooksHandler('test_handler')
        assert handler.name == 'test_handler'

    def test_handler_registration(self):
        handler = HooksHandler('test_handler')
        count = len(handler._hooks)
        handler.register('test', lambda: print())
        assert len(handler._hooks) == count + 1
        self.assertRaises(NameError, handler.register, 'test', lambda: print())
