import unittest

from helpers import assure, list_of, tuple_of, isa

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

class ListTypes(unittest.TestCase):
    def test_pass_through(self):
        @assure(list_of(str))
        def f(x):
            return x
        self.assertEquals(["bla", "blubb"], f(["bla", "blubb"]))

    def test_convert(self):
        @assure(list_of(int))
        def f(x):
            return x
        self.assertEquals([1,0], f(["1", "0"]))

    def test_value_error(self):
        @assure(list_of(int))
        def f(x):
            return x
        with self.assertRaises(ValueError):
            f(["bla"])

class TupleTypes(unittest.TestCase):
    def test_pass_through(self):
        @assure(tuple_of(str, int))
        def f(x):
            return x
        self.assertEquals(("bla", 1), f(("bla", 1)))

    def test_convert(self):
        @assure(tuple_of(str, int))
        def f(x):
            return x
        self.assertEquals(("1",0), f(("1", "0")))

    def test_value_error(self):
        @assure(tuple_of(int, int))
        def f(x):
            return x
        with self.assertRaises(ValueError):
            f(("bla", "bla"))
        with self.assertRaises(ValueError):
            f((1, "bla"))
        with self.assertRaises(ValueError):
            f(("bla", 2))

class IsATest(unittest.TestCase):
    def test_in_string(self):
        @assure(isa(str))
        def f(x):
            return x
        self.assertEquals("bla", f("bla"))
    def test_custom_class(self):
        class A: pass
        @assure(isa(A))
        def f(x):
            return x
        a = A()
        self.assertEquals(a, f(a))

    def test_value_error(self):
        class A: pass
        @assure(isa(A))
        def f(x):
            return x
        with self.assertRaises(ValueError):
            f(1)
