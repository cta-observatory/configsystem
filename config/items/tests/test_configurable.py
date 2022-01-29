import pytest
from config.exceptions import ConfigError


def test_simple():
    from config import Configurable, ConfigurableInstance, Int

    class Foo(Configurable):
        val = Int(default=1)

    class Bar(Configurable):
        foo = ConfigurableInstance(cls=Foo)

    bar = Bar()
    assert isinstance(bar.foo, Foo)
    assert bar.foo.val == 1

    with pytest.raises(ConfigError):
        bar.foo = 1



def test_get_default():
    from config import Configurable, ConfigurableInstance, Int

    class Foo(Configurable):
        val = Int()

    item = ConfigurableInstance(Foo)
    foo = item.get_default()
    assert foo.val is None

    item = ConfigurableInstance(Foo, default_config=dict(val=10))
    foo = item.get_default()
    assert foo.val == 10


def test_default_config():
    from config import Configurable, ConfigurableInstance, Int

    class Foo(Configurable):
        val = Int(default=1)

    class Bar(Configurable):
        foo = ConfigurableInstance(cls=Foo, default_config={'val': 2})

    bar = Bar()
    assert isinstance(bar.foo, Foo)
    assert bar.foo.val == 2


def test_default_nested():
    from config import Configurable, ConfigurableInstance, Int

    class Foo(Configurable):
        val = Int(default=1)

    class Bar(Configurable):
        foo = ConfigurableInstance(cls=Foo, default_config={'val': 2})

    class Baz(Configurable):
        bar = ConfigurableInstance(cls=Bar, default_config={'foo': {'val': 3}})

    baz = Baz()
    assert isinstance(baz.bar.foo, Foo)
    assert baz.bar.foo.val == 3


def test_config_nested():
    from config import Configurable, Int, ConfigurableInstance

    class Foo(Configurable):
        val = Int(default=1)

    class Bar(Configurable):
        val = Int(default=2)
        foo = ConfigurableInstance(Foo, default_config={'val': 3})

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
        val = Int(default=1)

    class Bar(Configurable):
        val = Int(default=2)
        foo = ConfigurableInstance(Foo)

    class Baz(Configurable):
        foo = ConfigurableInstance(Foo, default_config={'val': 5})
        bar1 = ConfigurableInstance(Bar)
        bar2 = ConfigurableInstance(
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
    from config import Configurable, ConfigurableInstance, Int

    class Foo(Configurable):
        val = Int(default=1)

    class Bar(Configurable):
        foo1 = ConfigurableInstance(cls=Foo, default_config={'val': 2})
        foo2 = ConfigurableInstance(cls=Foo, default_config={'val': 3})

    bar = Bar()
    assert bar.foo1.val == 2
    assert bar.foo2.val == 3

    bar = Bar(config={'foo1': {'val': 4}})
    assert bar.foo1.val == 4
    assert bar.foo2.val == 3


def test_subclasses():
    from config import Configurable, ConfigurableInstance, Int

    class Node(Configurable):
        val = Int(default=1)

    class SubNode1(Node):
        sub_val1 = Int(default=2)

    class SubNode2(Node):
        sub_val2 = Int(default=3)

    class Root(Configurable):
        node = ConfigurableInstance(cls=Node)

    # test plain default
    root = Root()
    assert type(root.node) is Node
    assert root.node.val == 1

    # test giving subclass to __init__
    root = Root(node=SubNode2(val=-1, sub_val2=0))
    assert type(root.node) is SubNode2
    assert root.node.val == -1
    assert root.node.sub_val2 == 0

    # test overriding cls in config
    root = Root(config={'node': {'cls': 'SubNode1', 'val': 2}})
    assert type(root.node) is SubNode1
    assert root.node.val == 2
    assert root.node.sub_val1 == 2

    # test invalid cls raises
    with pytest.raises(ConfigError):
        Root(config={'node': {'cls': 'blabla', 'val': 2}})

    # test invalid assignment raises
    with pytest.raises(ConfigError):
        root.node = 1

    class RootWithDefault(Configurable):
        node = ConfigurableInstance(cls=Node, default_config=dict(cls=SubNode2, val=4, sub_val2=10))

    root = RootWithDefault()
    assert type(root.node) is SubNode2
    assert root.node.val == 4
    assert root.node.sub_val2 == 10


    # test allow_subclasses=False

    class RootNoSubclasses(Configurable):
        node = ConfigurableInstance(cls=Node, allow_subclasses=False)

    with pytest.raises(ConfigError):
        RootNoSubclasses(node=SubNode1())
