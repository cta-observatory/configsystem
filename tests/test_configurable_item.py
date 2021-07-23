import pytest
from config.exceptions import ConfigError


def test_simple():
    from config import Configurable, ConfigurableInstance, Int

    class Foo(Configurable):
        val = Int(default=1, help='')

    class Bar(Configurable):
        foo = ConfigurableInstance(cls=Foo, help='')

    bar = Bar()
    assert isinstance(bar.foo, Foo)
    assert bar.foo.val == 1

    with pytest.raises(ConfigError):
        bar.foo = 1


def test_default_config():
    from config import Configurable, ConfigurableInstance, Int

    class Foo(Configurable):
        val = Int(default=1, help='')

    class Bar(Configurable):
        foo = ConfigurableInstance(cls=Foo, default_config={'val': 2}, help='')

    bar = Bar()
    assert isinstance(bar.foo, Foo)
    assert bar.foo.val == 2


def test_default_nested():
    from config import Configurable, ConfigurableInstance, Int

    class Foo(Configurable):
        val = Int(default=1, help='')

    class Bar(Configurable):
        foo = ConfigurableInstance(cls=Foo, default_config={'val': 2}, help='')

    class Baz(Configurable):
        bar = ConfigurableInstance(cls=Bar, default_config={'foo': {'val': 3}}, help='')

    baz = Baz()
    assert isinstance(baz.bar.foo, Foo)
    assert baz.bar.foo.val == 3


def test_config_nested():
    from config import Configurable, Int, ConfigurableInstance

    class Foo(Configurable):
        val = Int(default=1, help='')

    class Bar(Configurable):
        val = Int(default=2, help='')
        foo = ConfigurableInstance(Foo, default_config={'val': 3}, help='')

    # test with empty config
    b = Bar(config={})
    assert b.val == 2
    assert b.foo.val == 3

    # only some things configured
    # TODO: which default_config should be used? This right now
    # overrides the config of Bar.foo.val with the Foo.val default.
    # which from a certain point of view makes sense.
    b = Bar(config={'foo': {}})
    assert b.val == 2
    assert b.foo.val == 1

    b = Bar(config={'val': 5})
    assert b.val == 5
    assert b.foo.val == 3


def test_deeply_nested():
    from config import Configurable, Int, ConfigurableInstance

    class Foo(Configurable):
        val = Int(default=1, help='')

    class Bar(Configurable):
        val = Int(default=2, help='')
        foo = ConfigurableInstance(Foo, help='')

    class Baz(Configurable):
        foo = ConfigurableInstance(Foo, default_config={'val': 5}, help='')
        bar1 = ConfigurableInstance(Bar, help='')
        bar2 = ConfigurableInstance(
            Bar, default_config={'val': 3, 'foo': {'val': 4}}, help=''
        )

    b = Baz()
    assert b.get_config() == {
        'foo': {'val': 5},
        'bar1': {'val': 2, 'foo': {'val': 1}},
        'bar2': {'val': 3, 'foo': {'val': 4}},
    }
    assert b.foo.val == 5
    assert b.bar1.val == 2
    assert b.bar1.foo.val == 1
    assert b.bar2.val == 3
    assert b.bar2.foo.val == 4

    b = Baz(bar1=Bar(foo=Foo(val=10)))
    assert b.bar1.foo.val == 10
    assert b.bar1.val == 2
    assert b.bar2.foo.val == 4


def test_two_of_same_class():
    from config import Configurable, ConfigurableInstance, Int

    class Foo(Configurable):
        val = Int(default=1, help='')

    class Bar(Configurable):
        foo1 = ConfigurableInstance(cls=Foo, default_config={'val': 2}, help='')
        foo2 = ConfigurableInstance(cls=Foo, default_config={'val': 3}, help='')

    bar = Bar()
    assert bar.foo1.val == 2
    assert bar.foo2.val == 3

    bar = Bar(config={'foo1': {'val': 4}})
    assert bar.foo1.val == 4
    assert bar.foo2.val == 3


def test_subclasses():
    from config import Configurable, ConfigurableInstance, Int

    class Foo(Configurable):
        val = Int(default=1, help='')

    class SubFoo(Foo):
        pass

    class Bar(Configurable):
        foo = ConfigurableInstance(cls=Foo, help='')

    bar = Bar(config={'foo': {'cls': 'SubFoo', 'val': 2}})
    assert isinstance(bar.foo, SubFoo)
    assert bar.foo.val == 2

    with pytest.raises(ConfigError):
        Bar(config={'foo': {'cls': 'blabla', 'val': 2}})
