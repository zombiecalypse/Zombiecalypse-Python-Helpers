from helpers import function_logging, method_logging
import unittest


class LoggingTest(unittest.TestCase):
    def assertLogged(self, str):
        self.assertNotEqual([], self._log)
        self.assertRegexpMatches(self._log[-1], str)
    def setUp(self):
        self._log = []

class TestFunctionLogging(LoggingTest):
    def test_log_function_name(self):
        @function_logging(self._log.append)
        def go_fishing():
            return None
        go_fishing()
        self.assertLogged('go_fishing')

    def test_wrapped_function_return(self):
        @function_logging(self._log.append)
        def go_fishing():
            return "fish"
        self.assertEquals("fish", go_fishing())

    def test_log_function_arguments(self):
        @function_logging(self._log.append)
        def go_fishing_with_net(net):
            return None
        go_fishing_with_net("my net")
        self.assertLogged('[\'"]my net[\'"]')

    def test_log_function_keyword_arguments(self):
        @function_logging(self._log.append)
        def go_fishing_with_net(**kwargs):
            return kwargs
        self.assertEquals(dict(net = "my net"), go_fishing_with_net(net = "my net"))
        self.assertLogged('net\\s*=\\s*["\']my net["\']')

class TestMethodLogging(LoggingTest):
    def setUp(self):
        LoggingTest.setUp(self)
        class Cat:
            @method_logging(self._log.append)
            def miao(self, *args, **kwargs):
                return 10
        self.cat_class = Cat
        self.cat = self.cat_class()

    def test_wrapped_method(self):
        self.assertEquals(10, self.cat.miao())

    def test_method_name_logged(self):
        self.cat.miao()
        self.assertLogged("miao")

    def test_method_argument_logged(self):
        self.cat.miao("OHAI")
        self.assertLogged("['\"]OHAI['\"]")

    def test_method_keyword_argument_logged(self):
        self.cat.miao(greeting = "OHAI")
        self.assertLogged(r"greeting\s*=\s*['\"]OHAI['\"]")
