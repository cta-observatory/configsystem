import pathlib
from ..item import Item
from ..exceptions import ConfigError


class Path(Item):
    '''
    A `~pathlib.Path` item, that can optionally validate the given path.

    Attributes
    ----------
    exists: bool or None
        if True, path must exist, if False, path must not exist,
        if None, no check is performed.
    file_okay: bool
        If False and path exists, the path must not be a file
    dir_okay: bool
        If False and path exists, the path must not be a directory
    '''

    def __init__(self, default=None, exists=None, file_okay=True, dir_okay=True, **kwargs):
        super().__init__(**kwargs)

        self.exists = exists
        self.file_okay = file_okay
        self.dir_okay = dir_okay
        self.default = default

    def validate(self, value):
        value = super().validate(value)
        if value is None:
            return None

        try:
            value = pathlib.Path(value).expanduser().resolve().absolute()
        except ValueError:
            raise ConfigError(self, value, "must be a valid input for pathlib.Path")

        exists = value.exists()
        if exists and self.exists is False:
            raise ConfigError(self, value, "must not exist")

        if not exists and self.exists is True:
            raise ConfigError(self, value, "must exist")

        if exists:
            if self.file_okay is False and value.is_file():
                raise ConfigError(self, value, "must not be a file")

            if self.dir_okay is False and value.is_dir():
                raise ConfigError(self, value, "must not be a directory")

        return value

    def get_default_config(self):
        return self.default

    def from_config(self, config):
        return config

    def get_default(self):
        return self.default
