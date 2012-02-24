import unittest

from helpers import assure

class TestAssure(unittest.TestCase):
    def test_pass_through(self):
        @assure(str)
        def f(x):
            return x
        self.assertEquals("bla", f("bla"))

    def test_convert(self):
        @assure(int)
        def f(x):
            return x
        self.assertEquals(1, f("1"))

    def test_value_error(self):
        @assure(int)
        def f(x):
            return x
        with self.assertRaises(ValueError):
            f("bla")
