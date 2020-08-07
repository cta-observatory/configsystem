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


def test_assignment():
    from config import Configurable, SimpleItem

    class Test(Configurable):
        val = SimpleItem()

    t = Test()
    assert t.val is None
    t.val = 5
    assert t.val == 5


def test_get_config_simple():
    from config import Configurable, SimpleItem

    class Test(Configurable):
        val = SimpleItem()

    t = Test()
    assert t.get_config() == {'val': None}

    t.val = 10
    assert t.get_config() == {'val': 10}


def test_get_config_nested():
    from config import Configurable, SimpleItem

    class Sub(Configurable):
        val = SimpleItem()

    class Main(Configurable):
        val = SimpleItem()
        sub = SimpleItem(default=Sub(val=10))

    m = Main()
    assert m.get_config() == {'val': None, 'sub': {'val': 10}}

    m = Main(val=4, sub=Sub(val=42))
    assert m.get_config() == {'val': 4, 'sub': {'val': 42}}
