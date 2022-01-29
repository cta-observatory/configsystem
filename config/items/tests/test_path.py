import pathlib
import pytest
from config.exceptions import ConfigError


def test_path_validate(tmp_path):
    from config import Path

    not_existing_path = tmp_path / 'nope'
    existing_dir = tmp_path

    existing_file = tmp_path / 'yes'
    with existing_file.open('w'):
        pass

    item = Path()
    assert item.validate(None) is None
    assert item.validate(not_existing_path) == not_existing_path
    assert item.validate(existing_dir) == existing_dir
    assert item.validate(existing_file) == existing_file

    item = Path(dir_okay=False)
    assert item.validate(None) is None
    assert item.validate(not_existing_path) == not_existing_path
    assert item.validate(existing_file) == existing_file
    with pytest.raises(ConfigError):
        item.validate(existing_dir)


    item = Path(file_okay=False)
    assert item.validate(None) is None
    assert item.validate(not_existing_path) == not_existing_path
    assert item.validate(existing_dir) == existing_dir
    with pytest.raises(ConfigError):
        item.validate(existing_file)

    item = Path(exists=False)
    assert item.validate(None) is None
    assert item.validate(not_existing_path) == not_existing_path
    with pytest.raises(ConfigError):
        item.validate(existing_file)
    with pytest.raises(ConfigError):
        item.validate(existing_dir)


    item = Path(allow_none=False)
    with pytest.raises(ConfigError):
        item.validate(None)



def test_path_configurable():
    from config import Configurable, Path

    class Foo(Configurable):
        path = Path(allow_none=False)

    foo = Foo(path="test.csv")
    assert foo.path == pathlib.Path("test.csv").absolute()

    foo = Foo(config=dict(path="test.csv"))
    assert foo.path == pathlib.Path("test.csv").absolute()

    with pytest.raises(ConfigError):
        foo.path = None

    with pytest.raises(ConfigError):
        foo = Foo()
