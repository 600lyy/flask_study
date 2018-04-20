import os
import sys
from threading import Lock

<<<<<<< HEAD
from .config import ConfigAttribute
from .config import Config as config_class
from .helpers import Decorators
from .helpers import 
=======
from .config import ConfigAttribute, Config
from .helpers import Decorators
>>>>>>> edb62659621eb1f5efb1325a82f973743356f27b

# a lock used for logger initialization
_logger_lock = Lock()

D = Decorators()


class Flask(object):
    """The flask object implements a WSGI application and acts as the central
    object.  It is passed the name of the module or package of the
    application.  Once it is created it will act as a central registry for
    the view functions, the URL rules, template configuration and much more.
    """
<<<<<<< HEAD
    debug = ConfigAttribute('DEBUG')

    logger_name = ConfigAttribute('LOGGER_NAME')

    default_config = {
        'DEBUG':                False,
        'LOGGER_NAME':          None,
        'SERVER_NAME':          None,
        'MAX_CONTENT_LENGTH':   None,
    }

    def __init__(self, import_name, root_path=None):
        self.__name__ = import_name
        if root_path is None:
            pass
=======
    def __init__(self, import_name):
        self.__name__ = import_name
>>>>>>> edb62659621eb1f5efb1325a82f973743356f27b
