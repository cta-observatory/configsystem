from collections.abc import Mapping


def recursive_update(d1, d2, copy=False):
    '''Merge dicts recursively, e.g.

    >>> d1 = {'a': {'b': 'foo'}}
    >>> d2 = {'a': {'c': 'foo'}}
    >>> recursive_update(d1, d2)
    {'a': {'b': 'foo', 'c': 'foo'}}
    >>> # As opposed to
    >>> d1.update(d2)
    {'a': {'c': 'foo'}}
    '''
    if not isinstance(d1, Mapping) or not isinstance(d2, Mapping):
        raise TypeError('Arguments must be mappings')

    if copy:
        d1 = d1.copy()

    for k, v in d2.items():
        if isinstance(v, Mapping):
            d1[k] = recursive_update(d1.get(k, {}), v)
        else:
            d1[k] = v

    # just for convenience, the input dict is actually mutated
    return d1
