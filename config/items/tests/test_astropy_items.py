import pytest
from config.exceptions import ConfigError


def test_quantity_simple():
    u = pytest.importorskip('astropy.units')

    from config import Configurable
    from config.items.astropy import QuantityItem

    class Test(Configurable):
        q = QuantityItem()

    t = Test()
    t.q = 5
    assert isinstance(t.q, u.Quantity)

    # test quantity in config
    t = Test(config={'q': u.Quantity(5, u.m)})
    assert t.q == 5 * u.m

    # test dict base config
    t = Test(config={'q': {'value': 10, 'unit': 'm'}})
    assert t.q == 10 * u.m

    # test array
    t = Test(config={'q': {'value': [1, 2, 3], 'unit': 'm'}})
    assert all(t.q == [1, 2, 3] * u.m)


def test_quantity_unit():
    u = pytest.importorskip('astropy.units')

    from config import Configurable
    from config.items.astropy import QuantityItem

    class Test(Configurable):
        q = QuantityItem(unit=u.m)

    t = Test()
    with pytest.raises(ConfigError):
        t.q = 5


def test_quantity_allow_none():
    u = pytest.importorskip('astropy.units')

    from config import Configurable
    from config.items.astropy import QuantityItem

    class Test(Configurable):
        q = QuantityItem(default=1 * u.m, unit=u.m, allow_none=False)

    t = Test()
    with pytest.raises(ConfigError):
        t.q = None
