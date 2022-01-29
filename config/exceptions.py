class ConfigError(ValueError):
    def __init__(self, item, value, msg):
        super().__init__(
            f'Item {item!r}: {msg}, got {value!r}'
        )
