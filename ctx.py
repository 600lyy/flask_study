import sys
from functools import update_wrapper


class RequestContext(object):
    """The request context contains all request relevant information.
    """
    def __init__(self, app, environ, request=None):
        self.app = app
        if request is None:
            request = app.request_class(environ)