try:
    # performance improvement for python >= 3.9
    from functools import cache
except ImportError:
    from functools import lru_cache
    def cache(f):
        return lru_cache(maxsize=None)(f)

from ..item import Item
from ..exceptions import ConfigError


__all__ = ['LookupDatabase', 'Lookup']


class LookupDatabase:

    def __init__(self, item, hierarchy, default=None, configuration=None):
        self.hierarchy = tuple(hierarchy)
        self._indexed_hierarchy = list(enumerate(hierarchy))[::-1]
        self._expected = '(' + ', '.join(f'<{key} value>' for key in self.hierarchy) + ')'

        self.item = item
        # allow overriding the default of the item
        self.default = default if default is not None else self.item.get_default()

        self.configuration = []

        if configuration is None:
            return

        for lookup_config in configuration:
            lookup_config = tuple(lookup_config)

            if len(lookup_config) != 3:
                raise ValueError(f'Lookup definition must be (key, value of key, value), got {lookup_config}')

            key, key_value, value = lookup_config
            if key not in self.hierarchy:
                raise ValueError(f'Key {key} not in hierarchy: {self.hierarchy}')


            value = item.validate(value)
            self.configuration.append((key, key_value, value))

    @cache
    def __getitem__(self, lookup):
        # support a single value for len(hierarchy) == 1
        if not isinstance(lookup, tuple):
            lookup = (lookup, )

        if len(lookup) != len(self.hierarchy):
            raise IndexError(f"Lookup must be a tuple of form {self._expected}")

        for index, key in self._indexed_hierarchy:

            for (lookup_key, key_value, value) in self.configuration:
                if key != lookup_key:
                    continue

                if key_value == lookup[index]:
                    return value

        return self.default

    def __repr__(self):
        return f'{self.__class__.__name__}(hierarchy={self.hierarchy}, item={self.item})'


class Lookup(Item):
    def __init__(self, item, hierarchy, default_config=None, **kwargs):
        super().__init__(**kwargs)
        self.item = item
        self.hierarchy = hierarchy
        self.default_config = default_config


    def from_config(self, config):
        try:
            return LookupDatabase(
                item=self.item,
                hierarchy=self.hierarchy,
                **config
            )
        except:
            raise ConfigError(self, config, 'is an invalid config')


    def get_default(self):
        if self.default_config is None:
            return LookupDatabase(self.item, self.hierarchy)
        return self.from_config(self.default_config)

    def get_default_config(self):
        if self.default_config is None:
            return {}
        return self.default_config

    def validate(self, value):
        if not isinstance(value, LookupDatabase):
            # see if it's a single value matching our item

            try:
                value = self.item.validate(value)
            except ConfigError:
                raise ConfigError(self, value, f'Single value must be valid for {self.item}')

            return LookupDatabase(item=self.item, hierarchy=self.hierarchy, default=value)

        if value.hierarchy != self.hierarchy:
            raise ConfigError(
                self, 
                value,
                'HierarchicalLookup must have same hierarchy.'
                f' Expected {self.hierarchy}, got {value.hierarchy}'
            )

        if type(value.item) is not type(self.item):
            raise ConfigError(
                self, 
                value,
                'HierarchicalLookup must have same item type.'
                f' Expected {type(self.item)}, got {type(value)}'
            )

        return value
