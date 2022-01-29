from copy import deepcopy

from ..item import Item
from ..exceptions import ConfigError


class Object(Item):
    '''
    A config item consisting of a single python object.

    No nested configuration supported.
    '''
    type = object

    def __init__(self, default=None, allow_none=True, copy_default=False, **kwargs):
        super().__init__(**kwargs)

        self.allow_none = allow_none
        self.copy_default = copy_default
        self.default = default
        self.default = self.validate(default)

    def validate(self, value):
        value = super().validate(value)
        if value is None:
            return None

        if not isinstance(value, self.type):
            raise ConfigError(self, value, f"must be an instance of {self.type}")

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
    type = int


class Float(Object):
    type = float


class String(Object):
    type = str
