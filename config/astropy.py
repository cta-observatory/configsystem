try:
    import astropy.units as u
except ImportError:
    raise ImportError(
        'You need ``astropy`` to uses the config items from this module'
    ) from None

from collections.abc import Mapping

from .items import Object, ConfigError


class QuantityItem(Object):

    def __init__(self, unit=None, **kwargs):
        super().__init__(**kwargs)
        self.unit = unit

    def validate(self, value):
        value = super().validate(value)
        if value is None:
            return

        try:
            value = u.Quantity(value, copy=False)
        except ValueError:
            raise ConfigError(self.configurable(), self, value, f"must be a valid input to Quantity")

        # verify unit if one is required
        if self.unit is not None:
            try:
                value = value.to(self.unit)
            except ValueError:
                raise ConfigError(self.configurable(), self, value, f"must be convertible to {self.unit}")

        return value

    def from_config(self, config_value):
        if isinstance(config_value, u.Quantity):
            return config_value
        elif isinstance(config_value, Mapping):
            return u.Quantity(**config_value)
        else:
            raise TypeError(
                'Config value for QuantityItem must be a Quantity or dict'
                f', got {config_value}'
            )

    def from_string(self, string):
        if string == 'None':
            return self.validate(None)
        return self.validate(string)
