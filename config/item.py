from abc import ABCMeta, abstractmethod
import weakref

from .exceptions import ConfigError


class Item(metaclass=ABCMeta):
    '''
    Base class for all configuration items.

    This is a descriptor for class members.
    Each Item describes one configurable member variable
    of the instances.
    '''
    def __init__(self, help='', allow_none=True):
        self.help = help
        self.allow_none = allow_none
        self.configurable = None
        self.name = None

    def __set_name__(self, owner, name):
        # avoid circular reference
        self.configurable = weakref.ref(owner)
        self.name = name

    def __set__(self, instance, value):
        value = self.validate(value)
        instance.__dict__[self.name] = value

    def validate(self, value):
        '''Validate value, raises ValueError for invalid values'''
        if value is None and self.allow_none is False:
            raise ConfigError(self, value, 'must not be None')
        return value

    @abstractmethod
    def from_config(self, config):
        '''Create the value from its config representation'''
        pass

    @abstractmethod
    def get_default(self):
        '''Return a new instance created from the default configuration'''
        pass

    @abstractmethod
    def get_default_config(self):
        '''Return the default configuration'''
        pass

    def __repr__(self):
        if self.configurable is None:
            part1 = f'{self.__class__.__name__}'
        else:
            part1 = f'{self.configurable()}.{self.name}[{self.__class__.__name__}]'

        return f'{part1}(default={self.get_default()}, allow_none={self.allow_none})'
