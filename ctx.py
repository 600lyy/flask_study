import sys
from functools import update_wrapper
from werkzeug.exceptions import HTTPException


class RequestContext(object):
    """The request context contains all request relevant information.
    """
    def __init__(self, app, environ, request=None):
        self.app = app
        if request is None:
            request = app.request_class(environ)
        self.request = request
        self.url_adapter = app.create_url_adapter(self.request)
        self.match_request()

    def match_request(self):
        """call match request to find endpoint
        """
        try:
            self.request.url_rule, self.request.view_args = \
                self.url_adapter.match(return_rule=True)
        except HTTPException as e:
            self.request.routing_exception = e

    def __repr__(self):
        return "<{0} \'{1}\' [{2}] of {3}>".format(
            self.__class__.__name__,
            self.request.url,
            self.request.method,
            self.app.name,
        )

    def __enter__(self):
        #  self.pop()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        pass

    def copy(self):
        """returns a copy of itself
        """
        return self.__class__(
            self.app, self.request.environ, self.request
            )

    __str__ = __repr__