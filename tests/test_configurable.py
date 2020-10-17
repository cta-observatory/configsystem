import pytest


def test_class_definition():
    from config import Configurable, SimpleItem

    class Test(Configurable):
        val = SimpleItem()

    assert 'val' in Test.__config_items__


def test_instantiation():
    from config import Configurable, SimpleItem

    class Test(Configurable):
        val = SimpleItem()

    t = Test()
    assert t.val is None

    t = Test(val=10)
    assert t.val == 10

    # assert unknown config raises
    with pytest.raises(TypeError):
        Test(foo=10)


def test_assignment():
    from config import Configurable, SimpleItem

    class Test(Configurable):
        val = SimpleItem()

    t = Test()
    assert t.val is None
    t.val = 5
    assert t.val == 5


def test_config():
    from config import Configurable, SimpleItem

    class Test(Configurable):
        val = SimpleItem(default=1)

    t = Test()
    assert t.val == 1

    t = Test(config={'val': 2})
    assert t.val == 2

    # test precedence of kwargs over config
    t = Test(config={'val': 2}, val=3)
    assert t.val == 3


def test_get_config_simple():
    from config import Configurable, SimpleItem

    class Test(Configurable):
        val = SimpleItem()

    t = Test()
    assert t.get_config() == {'val': None}

    t.val = 10
    assert t.get_config() == {'val': 10}


def test_get_config_nested():
    from config import Configurable, SimpleItem, ConfigurableItem

    class Sub(Configurable):
        val = SimpleItem()

    class Main(Configurable):
        val = SimpleItem()
        sub = ConfigurableItem(Sub, default_config=dict(val=10))

    m = Main()
    assert m.get_config() == {'val': None, 'sub': {'val': 10}}

    m = Main(val=4, sub=Sub(val=42))
    assert m.get_config() == {'val': 4, 'sub': {'val': 42}}


def test_get_default_config():
    from config import Configurable, SimpleItem, ConfigurableItem

    class Foo(Configurable):
        val = SimpleItem()

    class Main(Configurable):
        val = SimpleItem()
        foo = ConfigurableItem(Foo, default_config=dict(val=10))

    m = Main()
    assert m.get_config() == Main.get_default_config()

    # test with subclass
    class Foo(Configurable):
        val1 = SimpleItem(1)

    class Sub(Foo):
        val2 = SimpleItem(2)

    class Main(Configurable):
        val = SimpleItem()
        foo = ConfigurableItem(
            Foo,
            default_config={'cls': 'Sub', 'val1': 3, 'val2': 4},
        )

    m = Main()
    assert isinstance(m.foo, Sub)
    assert m.foo.val1 == 3
    assert m.foo.val2 == 4
    assert m.get_config() == Main.get_default_config()


def test_get_nonabstract_subclasses():
    from config import Configurable
    from abc import ABCMeta, abstractmethod

    class Foo(Configurable):
        pass

    class Bar(Foo, metaclass=ABCMeta):
        @abstractmethod
        def test():
            pass

    class Baz(Bar, metaclass=ABCMeta):
        def test():
            pass

    class Quuz(Foo):
        pass

    assert Foo.get_nonabstract_subclasses() == {
        'Foo': Foo, 'Baz': Baz, 'Quuz': Quuz
    }
