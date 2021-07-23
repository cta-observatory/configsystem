from copy import deepcopy
from operator import index

from .item import Item
from .configurable import Configurable
from .exceptions import ConfigError


class Object(Item):
    '''
    A config item consisting of a single python object.
    No nested configuration supported
    '''

    def __init__(self, default=None, allow_none=True, copy_default=False, **kwargs):
        super().__init__(**kwargs)
        self.default = default
        self.allow_none = allow_none
        self.copy_default = copy_default

    def validate(self, value):
        if value is None and not self.allow_none:
            raise ConfigError(self.configurable(), self, value, "must not be None")
        return value

    def get_default(self):
        if self.copy_default:
            return deepcopy(self.default)
        else:
            return self.default

    def from_config(self, config):
        return config

    def get_default_config(self):
        return self.get_default()


class Int(Object):
    def validate(self, value):
        value = super().validate(value)
        if value is None:
            return value

        try:
            return index(value)
        except TypeError:
            raise ConfigError(self.configurable(), self, value, "must be interpretable as an integer")

    def from_string(self, string):
        return int(string)

class ConfigurableInstance(Item):
    '''
    A config item that is itself configurable
    '''
    def __init__(self, cls, default_config=None, **kwargs):
        if not issubclass(cls, Configurable):
            raise TypeError('cls must be a subclass of ``Configurable``')

        super().__init__(**kwargs)
        self.cls = cls
        self.default_config = {} if default_config is None else default_config

    def validate(self, value):
        if not isinstance(value, self.cls):
            raise ConfigError(self.configurable(), self, value, f"must be an instance of {self.cls}")
        return value

    def from_config(self, config):
        # check if the type of a subclass is specified in the config
        if config.get('cls'):
            # to get config without type and not modify the original one
            config = config.copy()
            cls = config.pop('cls')

            if isinstance(cls, str):
                try:
                    cls = self.cls.get_nonabstract_subclass(cls)
                except TypeError:
                    raise ConfigError(self.configurable(), self, cls, f"must be a subclass of {self.cls}")

            if not issubclass(cls, self.cls):
                raise ConfigError(self.configurable(), self, cls, f"must be a subclass of {self.cls}")
        else:
            cls = self.cls

        return cls(config=config)

    def from_string(self):
        raise NotImplementedError('Creating Whole Configurable Objects from String is not supported')

    def get_default(self):
        return self.from_config(self.default_config)

    def get_default_config(self):
        config = self.cls.get_default_config()
        # local default overrides cls defaults
        config.update(self.default_config)
        return config
