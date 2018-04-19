import os
from functools import update_wrapper
from types import MethodType


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


def get_root_path(import_name):
    """Returns the path to a package. this returns the path of a package or
    the folder that contains a module
    """
    