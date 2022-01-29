import pytest
from config.exceptions import ConfigError


def test_int_validate():
    from config import Int

    item = Int()
    assert item.validate(5) == 5
    assert item.validate(None) is None

    with pytest.raises(ConfigError):
        item.validate(5.0)

    with pytest.raises(ConfigError):
        item.validate('5.0')

    item = Int(default=1, allow_none=False)
    with pytest.raises(ConfigError):
        item.validate(None)


def test_int_get_default():
    from config import Int

    item = Int()
    assert item.get_default() is None

    item = Int(default=1)
    assert item.get_default() == 1


def test_int_get_default_config():
    from config import Int

    item = Int()
    assert item.get_default_config() is None

    item = Int(default=1)
    assert item.get_default_config() == 1


def test_float_validate():
    from config import Float

    item = Float()
    assert item.validate(5.0) == 5.0
    assert item.validate(None) is None

    with pytest.raises(ConfigError):
        item.validate('5.0')

    with pytest.raises(ConfigError):
        item.validate(5)

    item = Float(default=1.0, allow_none=False)
    with pytest.raises(ConfigError):
        item.validate(None)


def test_float_get_default():
    from config import Float

    item = Float()
    assert item.get_default() is None

    item = Float(default=1.0)
    assert isinstance(item.get_default(), float)
    assert item.get_default() == 1.0


def test_float_get_default_config():
    from config import Float

    item = Float()
    assert item.get_default_config() is None

    item = Float(default=1.0)
    assert item.get_default_config() == 1.0


def test_string_validate():
    from config import String

    item = String()
    assert item.validate("foo") == "foo"
    assert item.validate(None) is None

    with pytest.raises(ConfigError):
        item.validate(5.0)

    with pytest.raises(ConfigError):
        item.validate(5)

    item = String(default="foo", allow_none=False)
    with pytest.raises(ConfigError):
        item.validate(None)


def test_string_default_config():
    from config import String

    item = String()
    assert item.get_default_config() is None

    item = String(default='foo')
    assert item.get_default_config() == 'foo'
