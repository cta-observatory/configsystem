from .item import ConfigItem


class ConfigurableMeta(type):
    def __new__(cls, name, bases, dct):

        dct['__config_items__'] = {}
        for k, v in dct.items():
            if isinstance(dct[k], ConfigItem):
                dct['__config_items__'][k] = v

        new_cls = super().__new__(cls, name, bases, dct)
        return new_cls


class Configurable(metaclass=ConfigurableMeta):

    def __init__(self, config=None, **kwargs):
        self.__config__ = {}

        # first set all attributes handed in via kwargs
        for k, v in kwargs.items():
            if k in self.__config_items__:
                setattr(self, k, v)
            else:
                raise TypeError(f'__int__ got an unexpected keyword argument {k}')

        already_set = set(kwargs)

        # now the remaining stuff via the config
        if config is not None:
            for k in set(config.keys()).difference(already_set):
                setattr(self, k, config[k])
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
