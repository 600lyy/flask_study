import os
import types
import errno
import json


class My_property(object):
    def __init__(self, name):
        self.__name__ = name
    
    def __get__(self, obj, type=None):
        print("__get__ {}, {}".format(obj, type))
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, None)
        if value is None:
            return self.__name__
        return value

    def __set__(self, obj, value):
        obj.__dict__[self.__name__] = value
        

class ConfigAttribute(object):
    """An implementation of property
    """
    def __init__(self, name):
        self.__name__ = name

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.config[self.__name__]
        
    def __set__(self, obj, value):
        obj.config[self.__name__] = value


class Config(dict):
    def __init__(self, root_path, defaults=None):
        dict.__init__(self, defaults or {})
        #  super().__init__(defaults or {})
        self.root_path = root_path

    def from_envvar(self, variable_name, silent=False):
        rv = os.environ.get(variable_name)
        if not rv:
            if silent:
                return False
            raise RuntimeError("The environment varible {} is not set".format(variable_name))
        return self.from_pyfile(rv, silent=silent)
    
    def from_pyfile(self, filename, silent=False):
        filename = os.path.join(self.root_path, filename)
        d = types.ModuleType(filename, "dynamically created module")
        d.__file__ = filename
        try:
            with open(filename, mode='rb') as config_file:
                exec(compile(config_file.read(), filename, mode='exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self._from_object(d)
        return True

    def _from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                self.update({key: getattr(obj, key)})

    def from_mapping(self, *mapping, **kwargs):
        """Updates the config like :meth:`update` ignoring items with non-upper
        keys.
        """
        mappings = []
        if len(mapping) == 1:
            if hasattr(mapping[0], 'items'):
                mappings.append(mapping[0].items())
            elif len(mapping) > 1:
                raise TypeError(
                    "Expected at most 1 positional arguement"
                )
            mappings.append(kwargs.items())
            for mapping in mappings:
                for key, value in mapping:
                    if key.isupper():
                        self[key] = value
            return True

    def from_json(self, filename, silent=False):
        filename = os.path.join(self.root_path, filename)
        try:
            with open(filename, 'r') as json_file:
                obj = json.load(json_file)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        return self.from_mapping(obj)

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, dict.__repr__(self))


class Property(object):
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        print("{}.setter is called".format(self.__class__))
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

    
