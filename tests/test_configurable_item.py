import pytest


def test_simple():
    from config import Configurable, ConfigurableItem, SimpleItem

    class Foo(Configurable):
        val = SimpleItem(default=1)

    class Bar(Configurable):
        foo = ConfigurableItem(type=Foo)

    bar = Bar()
    assert isinstance(bar.foo, Foo)
    assert bar.foo.val == 1

    with pytest.raises(TypeError):
        bar.foo = 1


def test_default_config():
    from config import Configurable, ConfigurableItem, SimpleItem

    class Foo(Configurable):
        val = SimpleItem(default=1)

    class Bar(Configurable):
        foo = ConfigurableItem(type=Foo, default_config={'val': 2})

    bar = Bar()
    assert isinstance(bar.foo, Foo)
    assert bar.foo.val == 2


def test_default_nested():
    from config import Configurable, ConfigurableItem, SimpleItem

    class Foo(Configurable):
        val = SimpleItem(default=1)

    class Bar(Configurable):
        foo = ConfigurableItem(type=Foo, default_config={'val': 2})

    class Baz(Configurable):
        bar = ConfigurableItem(type=Bar, default_config={'foo': {'val': 3}})

    baz = Baz()
    assert isinstance(baz.bar.foo, Foo)
    assert baz.bar.foo.val == 3


def test_config_nested():
    from config import Configurable, SimpleItem, ConfigurableItem

    class Foo(Configurable):
        val = SimpleItem(default=1)

    class Bar(Configurable):
        val = SimpleItem(default=2)
        foo = ConfigurableItem(Foo, default_config={'val': 3})

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
    from config import Configurable, SimpleItem, ConfigurableItem

    class Foo(Configurable):
        val = SimpleItem(default=1)

    class Bar(Configurable):
        val = SimpleItem(default=2)
        foo = ConfigurableItem(Foo)

    class Baz(Configurable):
        foo = ConfigurableItem(Foo, default_config={'val': 5})
        bar1 = ConfigurableItem(Bar)
        bar2 = ConfigurableItem(
            Bar, default_config={'val': 3, 'foo': {'val': 4}}
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
    from config import Configurable, ConfigurableItem, SimpleItem

    class Foo(Configurable):
        val = SimpleItem(default=1)

    class Bar(Configurable):
        foo1 = ConfigurableItem(type=Foo, default_config={'val': 2})
        foo2 = ConfigurableItem(type=Foo, default_config={'val': 3})

    bar = Bar()
    assert bar.foo1.val == 2
    assert bar.foo2.val == 3

    bar = Bar(config={'foo1': {'val': 4}})
    assert bar.foo1.val == 4
    assert bar.foo2.val == 3


def test_subclasses():
    from config import Configurable, ConfigurableItem, SimpleItem

    class Foo(Configurable):
        val = SimpleItem(default=1)

    class SubFoo(Foo):
        pass

    class Bar(Configurable):
        foo = ConfigurableItem(type=Foo)

    bar = Bar(config={'foo': {'type': 'SubFoo', 'val': 2}})
    assert isinstance(bar.foo, SubFoo)
    assert bar.foo.val == 2

    with pytest.raises(TypeError):
        Bar(config={'foo': {'type': 'blabla', 'val': 2}})
