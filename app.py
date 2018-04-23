import os
import sys
from threading import Lock

from werkzeug.routing import Map, Rule

from .config import ConfigAttribute
from .config import Config
from .helpers import Decorators
from .helpers import get_root_path
from .helpers import _endpoint_from_view_func

# a lock used for logger initialization
_logger_lock = Lock()

D = Decorators()


class Flask(object):
    """The flask object implements a WSGI application and acts as the central
    object.  It is passed the name of the module or package of the
    application.  Once it is created it will act as a central registry for
    the view functions, the URL rules, template configuration and much more.
    """
    debug = ConfigAttribute('DEBUG')

    logger_name = ConfigAttribute('LOGGER_NAME')

    config_class = Config

    url_rule_class = Rule

    default_config = {
        'DEBUG':                False,
        'LOGGER_NAME':          None,
        'SERVER_NAME':          None,
        'MAX_CONTENT_LENGTH':   None,
    }

    def __init__(self, import_name, instance_relative_config, root_path=None):
        self.__name__ = import_name
        self.logger_name = import_name
        self._got_first_request = False
        if root_path is None:
            self.root_path = get_root_path(import_name)
        self.config = self.make_config(instance_relative_config)

        #: A dictionary of all view functions registered.  The keys will
        #: be function names which are also used to generate URLs and
        #: the values are the function objects themselves.
        #: To register a view function, use the :meth:`route` decorator.
        self.view_functions = {}

        self.url_map = Map()

    def make_config(self, instance_relative_config=False):
        """Used to create the config attribute by the Flask constructor.
        """
        root_path = self.root_path
        return self.config_class(root_path, self.default_config)

    @property
    def got_first_request(self):
        return self._got_first_request

    @D.setupmethod
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        """Connects a URL rule.  Works exactly like the :meth:`route`
        decorator.  If a view_func is provided it will be registered with the
        endpoint.

        If the view_func is not provided you will need to connect the endpoint
        to a view function like so::

            app.view_functions['index'] = index
        """
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        options['endpoint'] = endpoint

        methods = options.pop('methods', None)
        if methods is None:
            methods = getattr(view_func, 'methods', None) or ('Get')
        else:
            methods = set(item.upper() for item in methods)
        options['methods'] = methods

        rule = self.url_rule_class(rule, **options)
        self.url_map.add(rule)

        if  view_func is not None:
            old_func = self.view_functions[endpoint]
            if old_func is not None and old_func != view_func:
                raise AssertionError('view function for an endpoint should not be overrwirtten')
            self.view_functions[endpoint] = view_func

    def route(self, rule, **options):
        """A decorator that is used to register a view function for a
        given URL rule.
        """"
        def wrapper(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, endpoint, func)
            return f
        return wrapper

    @setupmethod
    def endpoint(self, endpoint):
        """A decorator to register a function as an endpoint.
        Example::

            @app.endpoint('example.endpoint')
            def example():
                return "example"
        """
        def wrapper(f):
            self.view_functions[endpoint] = f
            return f
        return wrapper

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


    def wsgi_app(self, environ, start_response):
        pass    
