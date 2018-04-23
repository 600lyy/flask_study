import os
import sys
from functools import update_wrapper
from types import MethodType
from types import FunctionType


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

    class _Funcwrap(object):
        """Wraps a method and return an callable object
        """
        def __init__(self, f):
            if isinstance(f, FunctionType):
                self.f = f
            else:
                raise AssertionError('{} is not a function'.format(f.__class__))
        
        def __call__(self, *args, **kwargs):
            return self.f(*args, **kwargs)


@Decorators._Funcwrap
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
