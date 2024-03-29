from inspect import isabstract
from collections.abc import Mapping

from .item import Item


class Configurable:
    __config__ = {}


    def __init_subclass__(cls):
        '''
        Called when a new subclass of Configurable is created

        Sets up the ``__config__`` dict as a class member
        and inherits the config items from the base classes.
        '''
        # make sure each class gets it's own config dict
        cls.__config__ = {}

        # inherit config items
        for b in cls.__bases__:
            config = getattr(b, '__config__', {})
            for k, v in config.items():
                cls.__config__[k] = v

        # but local ones override those of the base classes
        for k, v in cls.__dict__.items():
            if isinstance(v, Item):
                cls.__config__[k] = v

    def __init__(self, config=None, **kwargs):
        '''
        Initialize a new configurable instance.

        All configurable items can be passed also as kwargs
        and then take precedence over the values specified in ``config``.

        All config items not specified in config or kwargs are instantiated
        from their defaults.
        '''
        # keep track of which config items we already set
        already_set = set()

        # first set / validate all attributes handed in via kwargs
        for k, v in kwargs.items():
            if k in self.__config__:
                setattr(self, k, v)
                already_set.add(k)
            else:
                raise TypeError(
                    f'__init__ got an unexpected keyword argument {k}'
                )

        # now the config
        if config is not None:
            if not isinstance(config, Mapping):
                raise TypeError(f"config must be a mapping, got {config}")

            for k in set(config).difference(already_set):
                if k not in self.__config__:
                    raise ValueError(f'Unknown config key "{k}"')

                val = self.__config__[k].from_config(config[k])
                setattr(self, k, val)
                already_set.add(k)

        # set all remaining to their defaults
        for k in set(self.__config__).difference(already_set):
            setattr(self, k, self.__config__[k].get_default())

    def get_config(self):
        '''
        Get the current config of an instance as dict.
        '''
        # to avoid circular import
        from .items import ConfigurableInstance

        config = {}
        for k, item in self.__config__.items():
            v = getattr(self, k)
            if isinstance(item, ConfigurableInstance):
                config[k] = v.get_config()
                # if the value is actually a subclass, we need include the name
                if v.__class__ is not item.cls:
                    config[k]['cls'] = v.__class__.__name__
            else:
                config[k] = v

        return config

    @classmethod
    def get_config_tree(cls):
        '''
        Return a tree of all configurable items with this class at the root
        '''
        # to avoid circular import
        from .items import ConfigurableInstance

        tree = {}
        for name, item in cls.__config__.items():
            if isinstance(item, ConfigurableInstance):
                tree[name] = [
                    {'cls': name, 'config': cls.get_config_tree()}
                    for name, cls in item.cls.get_nonabstract_subclasses().items()
                ]
            else:
                tree[name] = item

        return tree

    @classmethod
    def get_default_config(cls):
        '''
        Returns the default config of this class as dict.
        '''
        return {
            k: item.get_default_config()
            for k, item in cls.__config__.items()
        }

    @classmethod
    def get_nonabstract_subclasses(cls):
        '''
        Get all non-abstract children of this class

        Returns
        -------
        subclasses: dict
            mapping of name to subclass
        '''
        subclasses = {}
        if not isabstract(cls):
            subclasses[cls.__name__] = cls

        for subcls in cls.__subclasses__():
            subclasses.update(subcls.get_nonabstract_subclasses())

        return subclasses

    @classmethod
    def get_nonabstract_subclass(cls, name):
        '''
        Get all non-abstract children of this class
        '''
        subclasses = cls.get_nonabstract_subclasses()

        if name not in subclasses:
            raise TypeError(
                f'Unknown subclass {name!r} for class {cls}'
                f', possible values are {list(subclasses)}'
            )

        return subclasses[name]

    def __repr__(self):
        configs = ', '.join(f'{k}={getattr(self, k)!r}' for k in self.__config__.keys())
        return f'{self.__class__.__name__}({configs})'
