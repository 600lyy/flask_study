from werkzeug.wrappers import Request as RequestBase


class Request(RequestBase):
    """The request object used by default in Flask
    It supports the handling of 
    AcceptMixin, ETagRequestMixin,
    UserAgentMixin, AuthorizationMixin,
    CommonRequestDescriptorsMixin
    """
    #  def __init__(self, environ):
    #    super().__init__(environ)
    
    