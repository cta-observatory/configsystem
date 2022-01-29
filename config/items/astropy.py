try:
    import astropy.units as u
except ImportError:
    raise ImportError(
        'You need ``astropy`` to uses the config items from this module'
    ) from None

from collections.abc import Mapping

from .basic import Object
from ..exceptions import ConfigError


class QuantityItem(Object):

    def __init__(self, unit=None, **kwargs):
        self.unit = unit
        # validate needs unit to be already set
        super().__init__(**kwargs)

    def validate(self, value):
        value = super().validate(value)
        if value is None:
            return

        try:
            value = u.Quantity(value, copy=False)
        except ValueError:
            raise ConfigError(self, value, "must be a valid input to Quantity")

        # verify unit if one is required
        if self.unit is not None:
            try:
                value = value.to(self.unit, copy=False)
            except ValueError:
                raise ConfigError(self, value, f"must be convertible to {self.unit}")

        return value

    def from_config(self, config_value):
        try:
            if isinstance(config_value, Mapping):
                config_value = u.Quantity(**config_value, copy=False)
            return self.validate(config_value)
        except Exception:
            raise ConfigError(
                self,
                config_value,
                'Config value for QuantityItem must be a Quantity, dict or valid input to u.Quantity'
            )

    def from_string(self, string):
        if string == 'None':
            return self.validate(None)
        return self.validate(string)
