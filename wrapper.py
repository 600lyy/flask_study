from werkzeug.wrappers import Request as RequestBase


class Request(RequestBase):
    """The request object used by default in Flask
    """
    