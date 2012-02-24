#!/usr/bin/python

# Filename: helpers.py
# Author:   Aaron Karper
# Created:  2011-07-21
# Description:
# 		Provides some helper functions, namely the @assure and
#			@logging decorators and a accessor definition shortcut.
#           
from functools import wraps
import logging
def _(x):
	"as in @assure(_, int, float)"
	return x
class assure:
    """Assures a certain type on function calls. Ought to raise
    an exception, if the respective argument does not satisfy its 
    precondition and return a fitting representation of the argument
    if it does. 

    Example:
        @assure(int)
        def f(x):
            return x+1

        >>> f(1)
        2
        >>> f("2")
        3
        >>> f("bla")
        ValueError: ...
        """
    def __init__(self, *types, **keys):
        self.__types = types
        self.__keys  = keys
    def __call__(self, func):
        @wraps(func)
        def modified(*args, **kwargs):
            casted_args = [t(x) for t,x in zip(self.__types, args)]
            casted_kwargs = dict([k, self.__keys[k](kwargs[k])] for k in kwargs)
            return func( *casted_args, **casted_kwargs )
        return modified

class Logging:
    def func_arg(self, argument_list, keyword_arguments):
        argument_strings = [repr(arg) for arg in argument_list]
        keyword_strings = ["{} = {!r}".format(k, v) for k, v in
                keyword_arguments.items()]

        return "({})".format(", ".join(argument_strings + keyword_strings))

    def __init__(self, logger = logging.getLogger('Python').debug):
        self.__logger = logger

    def __call__(self, func):
        @wraps(func)
        def modified(*args, **key):
            arguments = self.func_arg(args,key)
            self.__logger("%s%s" % (func.func_name, arguments))
            return func(*args, **key)
        return modified

class function_logging(Logging):
    pass

class method_logging(Logging):
    def func_arg(self, L, D):
        return Logging.func_arg(self,L[1:], D)

class logging(method_logging):
    pass

class func_name:
    def __init__(self,name):
        self.name = name
    def __call__(self, f):
        f.func_name = self.name
        return f

def accessor(string, logger = _, type = _):
    """Shortcut to define a property object with type checking and logging"""
    attrname = "_%s" %string
    getter = lambda self: getattr(self, attrname)
    @logging(logger)
    @assure(_,type)
    @func_name(string)
    def setter(self, val):
        setattr(self,attrname, val)
    return property(getter,setter)

def list_of(type):
    return lambda l: map(type, l)
def tuple_of(*types):
    return lambda l: tuple(t(v) for t,v in zip(types, l))
def isa(type):
    def f(x):
        if isinstance(x, type):
            return x
        else:
            raise ValueError("{!r} should be a {!r} but is not".format(x, type))
    return f
