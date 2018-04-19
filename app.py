import os
import sys
from threading import Lock

from .config import ConfigAttribute, Config
from .helpers import Decorators

# a lock used for logger initialization
_logger_lock = Lock()

D = Decorators()


class Flask(object):
    """The flask object implements a WSGI application and acts as the central
    object.  It is passed the name of the module or package of the
    application.  Once it is created it will act as a central registry for
    the view functions, the URL rules, template configuration and much more.
    """
    def __init__(self, import_name):
        self.__name__ = import_name