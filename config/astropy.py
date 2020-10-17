try:
    import astropy.units as u
except ImportError:
    raise ImportError(
        'You need ``astropy`` to uses the config items from this module'
    ) from None

from collections.abc import Mapping

from .items import SimpleItem


class QuantityItem(SimpleItem):

    def __init__(self, default=None, unit=None, allow_none=True):
        super().__init__(default, copy_default=True)
        self.allow_none = allow_none
        if self.default is None and not self.allow_none:
            raise ValueError('Default is None but allow_none=False')
        self.unit = unit

    def __set__(self, instance, value):
        if value is None:
            if not self.allow_none:
                raise ValueError(
                    f'{instance.__class__} config {self.name} must not be None'
                )
        else:
            value = u.Quantity(value, copy=False)

            # verify unit if one is required
            if self.unit is not None:
                value = value.to(self.unit)

        super().__set__(instance, value)

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
