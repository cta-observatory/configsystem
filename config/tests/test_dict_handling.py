import pytest


def test_recursive_merge():
    from config.dict_handling import recursive_update

    # basic behaviour, this should be the same as dict.update
    assert recursive_update({}, {}) == {}
    assert recursive_update({}, {'a': 5}) == {'a': 5}
    assert recursive_update({'a': 10}, {'a': 5}) == {'a': 5}
    assert recursive_update({'a': 10}, {'b': 5}) == {'a': 10, 'b': 5}

    # no we get into the recursive part
    d1 = {'a': {'b': 1}}
    d2 = {'a': {'b': 5}}
    assert recursive_update(d1, d2) == {'a': {'b': 5}}

    d1 = {'a': {'b': 1}}
    d2 = {'a': {'c': 5}}
    assert recursive_update(d1, d2) == {'a': {'b': 1, 'c': 5}}

    d1 = {'a': {'b': 1}, 'c': 3}
    d2 = {'a': {'c': 5}}
    assert recursive_update(d1, d2) == {'a': {'b': 1, 'c': 5}, 'c': 3}


def test_recursive_merge_wrong_args():
    from config.dict_handling import recursive_update

    with pytest.raises(TypeError):
        recursive_update({}, [])

    with pytest.raises(TypeError):
        recursive_update({}, [])

    with pytest.raises(TypeError):
        # a is a simple value in first dict, but a subdict in the second
        recursive_update({'a': 5}, {'a': {'b': 'c'}})
