from abc import ABCMeta, abstractmethod

from copy import deepcopy


class ConfigItem(metaclass=ABCMeta):

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__config__[self.name]

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        instance.__config__[self.name] = value

    def __delete__(self, instance):
        del instance.__delete__[self.name]

    @abstractmethod
    def from_config(self, config):
        pass

    @abstractmethod
    def get_default(self):
        pass


class SimpleItem(ConfigItem):
    '''
    A config item consisting of a simple python value.
    No nested configuration supported
    '''

    def __init__(self, default=None, copy_default=False):
        self.default = default
        self.copy_default = copy_default

    def get_default(self):
        if self.copy_default:
            return deepcopy(self.default)
        else:
            return self.default

    def from_config(self, config):
        return config


class ConfigurableItem(ConfigItem):
    '''
    A config item that is itself configurable
    '''
    def __init__(self, type, default_config=None):
        self.type = type
        self.default_config = {} if default_config is None else default_config

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError(f'value must be an instance of type {self.type}')

        super().__set__(instance, value)

    def from_config(self, config):
        if config.get('type'):
            type_ = config.pop('type')
            subclasses = self.type.get_nonabstract_subclasses()
            if type_ not in subclasses:
                raise TypeError(f'Unknown type {type_!r}, expected a subclass of {self._type!r}')

            cls = subclasses[type_]
        else:
            cls = self.type
        return cls(config=config)

    def get_default(self):
        return self.from_config(self.default_config)
