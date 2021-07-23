from abc import ABCMeta, abstractmethod
import weakref


class Item(metaclass=ABCMeta):
    '''
    Base class for all configuration items.

    This is a descriptor for class members.
    Each Item describes one configurable member variable
    of the instances.
    '''
    def __init__(self, help):
        self.help = help

    def __set_name__(self, owner, name):
        # avoid circular reference
        self.configurable = weakref.ref(owner)
        self.name = name

    def __set__(self, instance, value):
        value = self.validate(value)
        instance.__dict__[self.name] = value

    @abstractmethod
    def validate(self, value):
        '''Validate value, raises ValueError for invalid values'''
        pass

    @abstractmethod
    def from_config(self, config):
        '''Create the value from its config representation'''
        pass

    @abstractmethod
    def from_string(self, string):
        '''Create the value from a string representation'''
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
        return (
            f'{self.__class__.__name__}('
            f'name={self.name}'
            f', default={self.get_default()}'
            ')'
        )
