from Node import node
from types import GeneratorType as gentype

class _dict(dict):
    """
        A dicitonary that uses all of it's elements.
        That is, when cycling through, getting, setting (elements that are there), or deleting, it will go through
        it, and all subdicts.
        Terminology note: subdict is any _dict that is a 'value' (rather than a key).
    """
    # def __new__(self: '_dict', *a) -> dict:
    #     """ creates a new instance of _dict. """
    #     return super().__new__(self, {})
    # def __init__(self: '_dict', *a) -> dict:
    #     """ forces passing to be ('1', 2, '3', 4, ...), and will gen {'1':2, '3':4}. """
    #     super().__init__(zip((a[x] for x in range(len(a)) if not x & 1), (a[x] for x in range(len(a)) if x & 1)))

    @property
    def flat(self: '_dict') -> gentype:
        """ A generator that yields each key from this class and any subdicts. """
        return (kv[0] for kv in self.flatpair)

    @property
    def flatpair(self: '_dict') -> gentype:
        """ A generator that yields a tuple of (key, value) from each elementin this and each subdict. """
        for k in self:
            v = super().__getitem__(k)
            if isinstance(v, _dict) and v:
                for n in v.flatpair:
                    yield n
            else:
                yield k, v
        
    def __contains__(self: '_dict', item: str) -> bool:
        """ Returns true if this or any of the subdicts contain 'item'. """
        return item in self.flat

    def __getitem__(self: '_dict', item: str) -> Union['node', 'dict']:
        if __debug__ and item not in self.flat:
            raise KeyError("'{}' doesn't exist!".format(item))
        return dict(self.flatpair)[item]
        # for k, v in self.flatpair:
        #     if k == item:
        #         return v

    def __delitem__(self: '_dict', item: str) -> None:
        for k in self:
            v = super().__getitem__(k)
            if k == item:
                return v
            if isinstance(v, dict) and item in v:
                return v[item]

    def __repr__(self: '_dict') -> str:
        return '_d' + super().__repr__()
    def __str__(self):
        return str({str(k): str(self[k]) for k in self})
class knowndict(_dict):
    """ The object that keeps tracks of all the currently known variables. """

    VAL_NAMES = {'global':'_$g', 'local': '_$l'}

    def __init__(self: 'knowndict', const: 'constants', args: dict = None) -> None:
        super().__init__(args or {})
        self.g, l = _dict(_dict()), _dict()

    def g():
        doc = "The known global variables"
        def fget(self: 'knowndict') -> 'node':
            return self[self.VAL_NAMES['global']]
        def fset(self: 'knowndict', value: 'node') -> None:
            self[self.VAL_NAMES['global']] = value
        def fdel(self: 'knowndict') -> None:
            self[self.VAL_NAMES['global']] = _dict()
        return locals()
    g = property(**g())

    def l():
        doc = "The known local variables"
        def fget(self: 'knowndict') -> 'node':
            return self[self.VAL_NAMES['local']]
        def fset(self: 'knowndict', value: 'node') -> None:
            self[self.VAL_NAMES['local']] = value
        def fdel(self: 'knowndict') -> None:
            self[self.VAL_NAMES['local']] = _dict()
        return locals()
    l = property(**l())










