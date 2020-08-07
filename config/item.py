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
