from ..item import Item
from ..configurable import Configurable
from ..exceptions import ConfigError


class ConfigurableInstance(Item):
    '''
    A config item that is itself configurable
    '''
    def __init__(self, cls, default_config=None, allow_subclasses=True, **kwargs):
        if not issubclass(cls, Configurable):
            raise TypeError('cls must be a subclass of ``Configurable``')

        super().__init__(**kwargs)
        self.cls = cls
        self.default_config = {} if default_config is None else default_config
        self.allow_subclasses = allow_subclasses

    def validate(self, value):
        if not isinstance(value, self.cls):
            raise ConfigError(self, value, f"must be an instance of {self.cls}")
        
        if self.allow_subclasses is False and type(value) is not self.cls:
            raise ConfigError(self, value, "must not be a subclass instance")
        return value

    def from_config(self, config):
        if 'cls' not in config:
            return self.cls(config=config)

        # we don't want to modify the config object, but we need it without cls
        config = config.copy()
        cls = config.pop('cls')

        if isinstance(cls, str):
            try:
                cls = self.cls.get_nonabstract_subclass(cls)
            except TypeError:
                raise ConfigError(self, cls, f"must be a subclass of {self.cls}")

        if not issubclass(cls, self.cls):
            raise ConfigError(self, cls, f"must be a subclass of {self.cls}")

        return cls(config=config)

    def get_default(self):
        return self.from_config(self.get_default_config())

    def get_default_config(self):
        config = self.cls.get_default_config()
        # local default overrides cls defaults
        config.update(self.default_config)
        return config
