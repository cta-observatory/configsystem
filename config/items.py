from copy import deepcopy

from .item import ConfigItem
from .configurable import Configurable


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

    def get_default_config(self):
        return self.default


class ConfigurableClassItem(ConfigItem):
    '''
    A config item that is itself configurable
    '''
    def __init__(self, cls, default_config=None):
        if not issubclass(cls, Configurable):
            raise TypeError('cls must be a subclass of ``Configurable``')

        self.cls = cls
        self.default_config = {} if default_config is None else default_config

    def __set__(self, instance, value):
        if not isinstance(value, self.cls):
            raise TypeError(f'value must be an instance of {self.cls}')

        super().__set__(instance, value)

    def from_config(self, config):
        # check if the type of a subclass is specified in the config
        if config.get('cls'):
            # to get config without type and not modify the original one
            config = config.copy()
            cls = config.pop('cls')

            if isinstance(cls, str):
                cls = self.cls.get_nonabstract_subclass(cls)

            if not issubclass(cls, self.cls):
                raise TypeError(
                    '``cls`` must be non-abstract sublass or the name of'
                    ' a non-abstract subclass of {self.cls!r}'
                )
        else:
            cls = self.cls

        return cls(config=config)

    def get_default(self):
        return self.from_config(self.default_config)

    def get_default_config(self):
        config = self.cls.get_default_config()
        # local default overrides cls defaults
        config.update(self.default_config)
        return config
