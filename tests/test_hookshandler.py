import unittest

from src.core import HooksHandler, DecorativeHooksHandler, CumulativeHooksHandler, UniqueHooksHandler


class TestHandler(unittest.TestCase):
    DUMMY = lambda: print()

    def test_name(self):
        handler = HooksHandler('test_handler')
        assert handler.name == 'test_handler'

    def test_register(self):
        handler = HooksHandler('test_handler')
        count = len(handler._hooks)
        handler.register('test', self.DUMMY)
        assert len(handler._hooks) == count + 1
        self.assertRaises(NameError, handler.register, 'test', self.DUMMY)

    def test_remove(self):
        handler = HooksHandler('test_handler')
        count = len(handler._hooks)
        handler.register('test', self.DUMMY)
        handler.register('test2', self.DUMMY)
        assert len(handler._hooks) == count + 2
        handler.remove('test2')
        assert len(handler._hooks) == count + 1
        self.assertRaises(KeyError, handler.remove, 'test2')

    def test_execute(self):
        handler = HooksHandler('test_handler')
        handler.register('test', self.DUMMY)
        self.assertRaises(NotImplementedError, handler.execute)

    def test_execute_cumulative(self):
        handler = CumulativeHooksHandler('test_handler')
        handler.register('one', lambda x: x + 1)
        assert handler.execute(0) == [1]
        handler.register('two', lambda x: x + 2)
        handler.register('three', lambda x: x + 3)
        assert handler.execute(0) == [1, 2, 3]

    def test_register_unique(self):
        handler = UniqueHooksHandler('test_handler')
        count = len(handler._hooks)
        handler.register('dummy', self.DUMMY)
        assert len(handler._hooks) == count + 1
        self.assertWarns(Warning, handler.register, 'dummy2', self.DUMMY)
        self.assertWarns(Warning, handler.register, 'dummy3', self.DUMMY, 10)
        assert len(handler._hooks) == count + 3
        assert handler._hooks[0].name == 'dummy3'

    def test_execute_unique(self):
        handler = UniqueHooksHandler('test_handler')
        handler.register('one', lambda x: x + 1)
        assert handler.execute(0) == 1
        handler.register('two', lambda x: x + 2, 10)
        handler.register('three', lambda x: x + 3)
        assert handler.execute(0) == 2

    def test_execute_decorative(self):
        handler = DecorativeHooksHandler('test_handler')
        handler.register('one', lambda x: x + 1)
        handler.register('two', lambda x: x + 2)
        handler.register('three', lambda x: x + 3)
        assert handler.execute(0) == 6
        handler._hooks.clear()

        handler.register('a', lambda x, y: (x + 1, y + 2))
        handler.register('b', lambda x, y: (x * 2, y * 2))
        assert handler.execute(0, 1) == (2, 6)

        self.assertRaises(Exception, handler.execute, 0, 1, a=2)
