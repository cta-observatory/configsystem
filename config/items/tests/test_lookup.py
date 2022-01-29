import pytest


def test_single_key():
    from config import Int
    from config.items.lookup import LookupDatabase

    lookup = LookupDatabase(
        item=Int(1),
        hierarchy=("type", ),
        lookups=[
            ("type", "LST", 2),
            ("type", "MST", 3),
        ],
    )

    assert lookup["LST"] == 2
    assert lookup["MST"] == 3

    # not matching anything -> default
    assert lookup["SST"] == 1


def test_two_keys():
    from config.items.lookup import LookupDatabase
    from config import Int

    lookup = LookupDatabase(
        item=Int(1),
        hierarchy=("type", "id"),
        lookups=[
            ("type", "LST", 2),
            ("type", "MST", 3),
            ("id", 5, 4),
            ("id", 30, 5),
        ],
    )

    assert lookup["LST", 1] == 2
    assert lookup["MST", 2] == 3

    # id more important then type
    assert lookup["LST", 5] == 4

    # unknown type, but matches id
    assert lookup["SST", 30] == 5

    # not matching anything -> default
    assert lookup["SST", 3] == 1


def test_lookup_invalid():
    from config.items.lookup import LookupDatabase
    from config import Int

    # invalid key in configuration
    with pytest.raises(ValueError):
        LookupDatabase(
            item=Int(1),
            hierarchy=("type", "id"),
            lookups=[
                ("type", "LST", 2),
                ("type", "MST", 3),
                ("invalid", 5, 4),
            ],
        )

    # invalid key in configuration
    with pytest.raises(ValueError):
        LookupDatabase(
            item=Int(1),
            hierarchy=("type", "id"),
            lookups=[
                ("type", "MST", 3),
                ("type", 2),
            ],
        )

    # invalid value in configuration
    with pytest.raises(ValueError):
        LookupDatabase(
            item=Int(1),
            hierarchy=("type", "id"),
            lookups=[
                ("type", "MST", 3),
                ("type", "LST", "foo"),
            ],
        )


    lookup = LookupDatabase(
        item=Int(1),
        hierarchy=("type", "id"),
        lookups=[
            ("type", "MST", 3),
            ("type", "LST", 2),
            ("id", 1, 2),
        ],
    )
    with pytest.raises(IndexError):
        # to few indices
        lookup[1]

    with pytest.raises(IndexError):
        # too many indices
        lookup[1, 2, 3]


def test_defaults():
    from config.items.lookup import LookupDatabase
    from config import Int

    lookup = LookupDatabase(Int(), ('foo', 'bar'))
    assert lookup[1, 2] is None

    lookup = LookupDatabase(Int(5), ('foo', 'bar'))
    assert lookup[1, 2] is 5


def test_item():
    from config import Configurable, Float
    from config.items.lookup import Lookup, LookupDatabase


    class Cleaning(Configurable):
        level = Lookup(Float(5.0), hierarchy=('type', 'id'))

    cleaning = Cleaning()
    assert isinstance(cleaning.level, LookupDatabase)
    assert cleaning.level['LST', 1] == 5.0

    # override default with a single value
    cleaning = Cleaning(level=10.0)
    assert isinstance(cleaning.level, LookupDatabase)
    assert cleaning.level['LST', 1] == 10.0

    # give a custom HierarchicalLookup
    cleaning_levels = LookupDatabase(
        item=Float(10.0),
        hierarchy=('type', 'id'),
        lookups=[
            ('type', 'LST', 5.0),
            ('type', 'MST', 15.0),
            ('id', 5, 20.0),
        ]
    )
    cleaning = Cleaning(level=cleaning_levels)
    assert isinstance(cleaning.level, LookupDatabase)
    assert cleaning.level['LST', 1] == 5.0
    assert cleaning.level['MST', 2] == 15.0
    assert cleaning.level['LST', 5] == 20.0
    assert cleaning.level['SST', 5] == 20.0
    assert cleaning.level['SST', 10] == 10.0


def test_invalid():
    from config import Configurable, Float, Int
    from config.items.lookup import Lookup, LookupDatabase
    from config.exceptions import ConfigError


    class Cleaning(Configurable):
        level = Lookup(item=Float(5.0, allow_none=False), hierarchy=('type', 'id'))

    with pytest.raises(ConfigError):
        Cleaning(level=None)

    cleaning = Cleaning()

    wrong_item = LookupDatabase(item=Int(5), hierarchy=('type', 'id'))
    with pytest.raises(ConfigError):
        cleaning.level = wrong_item

    wrong_hierarchy = LookupDatabase(item=Float(5.0), hierarchy=('foo', 'id'))
    with pytest.raises(ConfigError):
        cleaning.level = wrong_hierarchy
