from copy import deepcopy
from operator import index

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


class String(Object):
    type = str


class Int(Object):
    type = int

    def validate(self, value):

        # special case for to allow integer floats like 1.0
        if isinstance(value, float):
            if value.is_integer():
                value = int(value)

        # '__index__' means "I am losslessly convertible to an int"
        if hasattr(value, '__index__'):
            value = index(value)

        return super().validate(value)


class Float(Object):
    type = float

    def validate(self, value):
        # special casing for things explicitly advertising convertible to float
        if hasattr(value, '__float__'):
            value = float(value)

        return super().validate(value)
