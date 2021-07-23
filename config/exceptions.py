class ConfigError(ValueError):
    def __init__(self, configurable, item, value, msg):
        super().__init__(
            f'Config error for item {item.name}={item} of {configurable!r}: {msg}, got {value!r}'
        )
