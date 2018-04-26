import os
import sys
from functools import update_wrapper, wraps
from types import MethodType
from types import FunctionType

from .config import Property

__all__ = ['Decorators']


class Decorators(object):
    """A collection of user-defined decorators
    """
    def setupmethod(self, f):
        """Wraps a method so that it performs a check in debug mode if the
        first request was already handled.
         """
        #  assert isinstance(f, MethodType), "func to wrap must be a instancemethod"

        def wrapper_func(obj, *args, **kwargs):
            if obj.debug and obj._got_first_request:
                raise AssertionError(
                    'A setup function was called after the '
                    'first request was handled.  This usually indicates a bug'
                )
            return f(obj, *args, **kwargs)
        return update_wrapper(wrapper_func, f)

    class Funcwrap(object):
        """Wraps a method and return an callable object
        """
        def __init__(self, f):
            if isinstance(f, FunctionType):
                self.f = f
            else:
                raise AssertionError('{} is not a function'.format(f.__class__))
        
        def __call__(self, *args, **kwargs):
            return self.f(*args, **kwargs)

    class Cached_Property(Property):
        """A decorator that converts a function into a lazy property
        so the function will be only called once and the returned
        value is saved in objs.__dict__ which is to be red directly
        next time
        """
        def __init__(self, fget, name=None, doc=None):
            if not isinstance(fget, (FunctionType, MethodType)):
                _type = str(type(fget))
                raise AttributeError('Expected a function, get {} instead'.format(_type))
            self.__name__ = name or fget.__name__
            self.fget = fget
            self.__doc__ = doc or fget.__doc__

        def __get__(self, obj, type=None):
            if obj is None:
                return self
            value = obj.__dict__.get(self.__name__, None)
            if value is None:
                value = self.fget(obj)
                obj.__dict__[self.__name__] = value
            return value

        def __set__(self, obj, value):
            obj.__dict__[self.__name__] = value


@Decorators.Funcwrap
def get_root_path(import_name):
    """Returns the path to a package. this returns the path of a package or
    the folder that contains a module
    """
    mod = sys.modules.get(import_name)
    if mod is not None and hasattr(mod, '__file__'):
        return os.path.dirname(os.path.abspath(mod.__file__))


def _endpoint_from_view_func(view_func):
    """Returns the default endpoint for a given function.
    """
    assert isinstance(view_func, FunctionType), 'view_func must be a function' \
                                                'but {} got'.format(type(view_func))
    return view_func.__name__
