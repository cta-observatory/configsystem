from inspect import isabstract

from .item import ConfigItem, ConfigurableItem


class Configurable:
    def __init_subclass__(cls):
        '''
        Called when a new subclass of Configurable is created

        Sets up the ``__config_items__`` dict as a class member
        and inherits the config items from the base classes.
        '''
        cls.__config_items__ = {}

        # inherit config items
        for b in cls.__bases__:
            if hasattr(b, '__config_items__'):
                for k, v in b.__config_items__.items():
                    cls.__config_items__[k] = v

        # but local ones override those of the base classes
        for k, v in cls.__dict__.items():
            if isinstance(v, ConfigItem):
                cls.__config_items__[k] = v

    def __init__(self, config=None, **kwargs):
        '''
        Initialize a new configurable instance.

        All configurable items can be passed also as kwargs
        and then take precedence over the values specified in ``config``.

        All config items not specified in config or kwargs are instantiated
        from their defaults.
        '''
        self.__config__ = {}

        # first set all attributes handed in via kwargs
        for k, v in kwargs.items():
            if k in self.__config_items__:
                setattr(self, k, v)
            else:
                raise TypeError(
                    f'__init__ got an unexpected keyword argument {k}'
                )

        already_set = set(kwargs)

        # now the remaining stuff via the config
        if config is not None:
            for k in set(config.keys()).difference(already_set):
                if k not in self.__config_items__:
                    raise ValueError(f'Unknown config key "{k}"')

                val = self.__config_items__[k].from_config(config[k])
                setattr(self, k, val)
                already_set.add(k)

        # instantiate any unset things via the defaults
        for k in set(self.__config_items__).difference(already_set):
            setattr(self, k, self.__config_items__[k].get_default())

    def get_config(self):
        '''
        Get the current config of an instance as dict.
        '''
        config = {}
        for k, v in self.__config__.items():
            if isinstance(v, Configurable):
                config[k] = v.get_config()
            else:
                config[k] = v

        return config

    @classmethod
    def get_default_config(cls):
        '''
        Returns the default config of this class as dict.
        '''
        config = {}
        for k, v in cls.__config_items__.items():
            if isinstance(v, ConfigurableItem):
                # the default might be a subclass, so
                # we instantiate the default and get its config and type
                default = v.get_default()
                config[k] = default.get_config()
                config[k]['type'] = default.__class__.__name__
            else:
                config[k] = v.get_default()

        return config

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
