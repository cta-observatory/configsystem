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
