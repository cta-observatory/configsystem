from inspect import isabstract

from .item import ConfigItem


class Configurable:
    def __init_subclass__(cls):
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
        config = {}
        for k, v in self.__config__.items():
            if isinstance(v, Configurable):
                config[k] = v.get_config()
            else:
                config[k] = v

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
