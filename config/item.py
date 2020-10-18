from abc import ABCMeta, abstractmethod


class ConfigItem(metaclass=ABCMeta):
    '''
    Base class for all configuration items.

    This is a descriptor for class members.
    Each ConfigItem describes one configurable member variable
    of the instances.
    '''
    def __init__(self, help):
        self.help = help

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__config__[self.name]

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        instance.__config__[self.name] = value

    @abstractmethod
    def from_config(self, config):
        pass

    @abstractmethod
    def get_default(self):
        pass

    @abstractmethod
    def get_default_config(self):
        pass

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'name={self.name}'
            f', default={self.get_default()}'
            ')'
        )
