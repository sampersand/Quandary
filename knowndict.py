from typing import Union
from types import GeneratorType as gentype
from constants import _set
class flatdict(dict):
    """
        A dicitonary that uses all of it's elements.
        That is, when cycling through, getting, setting (elements that are there), or deleting, it will go through
        it, and all subdicts.
        Terminology note: subdict is any flatdict that is a 'value' (rather than a key).
    """
    # def __new__(self: 'flatdict', *a) -> dict:
    #     """ creates a new instance of flatdict. """
    #     return super().__new__(self, {})
    # def __init__(self: 'flatdict', *a) -> dict:
    #     """ forces passing to be ('1', 2, '3', 4, ...), and will gen {'1':2, '3':4}. """
    #     super().__init__(zip((a[x] for x in range(len(a)) if not x & 1), (a[x] for x in range(len(a)) if x & 1)))

    @property
    def flat(self: 'flatdict') -> gentype:
        """ A generator that yields each key from this class and any subdicts. """
        return (kv[0] for kv in self.flatpair)

    @property
    def flatpair(self: 'flatdict') -> gentype:
        """ A generator that yields a tuple of (key, value) from each elementin this and each subdict. """
        for k in self:
            v = super().__getitem__(k)
            if isinstance(v, flatdict):
                for n in v.flatpair:
                    yield n
            if isinstance(v, _set):
                for n in v:
                    yield n, k
            yield k, v
        
    def __contains__(self: 'flatdict', item: object) -> bool:
        """ Returns true if this or any of the subdicts contain 'item'. """
        return item in self.flat

    def __getitem__(self: 'flatdict', item: object) -> object:
        if __debug__ and item not in self.flat:
            raise KeyError("key '{}' doesn't exist!".format(item))
        return dict(self.flatpair)[item]
        # for k, v in self.flatpair:
        #     if k == item:
        #         return v

    def __delitem__(self: 'flatdict', item: object) -> None:
        if __debug__ and item not in self.flat:
            raise KeyError("key '{}' doesn't exist!".format(item))
        for k in self:
            v = super().__getitem__(k)
            if k == item:
                return v
            if isinstance(v, dict) and item in v:
                return v[item]

    def __getattr__(self: 'flatdict', attr: object) -> object:
        return self.__getitem__(attr) if attr in self else super().__getattr__(attr)
    def __setattr__(self: 'flatdict', attr: object, val: object) -> None:
        return self.__setitem__(attr, val) if attr in self else super().__setattr__(attr, val)
    def __delattr__(self: 'flatdict', attr: object) -> None:
        return self.__delitem__(attr) if attr in self else super().__delattr__(attr)

    def __repr__(self: 'flatdict') -> str:
        return '_' + super().__repr__()

    def __str__(self):
        return '{' + ', '.join(str(k) +': ' + str(self[k]) for k in self) + '}'

    def __add__(self, other):
        ret = flatdict(self.copy())
        ret.update(other)
        return ret
    def copy(self: 'flatdict') -> 'flatdict':
        return flatdict(super().copy())
class _control(flatdict):
    #TODO: marge this with flatdict
    CONTROL_NAMES = {'last':'$', 'ret':'$ret', 'esc':'$esc'}

    def __new__(self, knowns):
        return super().__new__(self, {})

    def __init__(self, knowns):
        self.knowns = knowns

    def last():
        doc = "The last element evaluated."
        def fget(self: '_control') -> 'node':
            return self[self.CONTROL_NAMES['last']]
        def fset(self: '_control', value: 'node') -> None:
            self[self.CONTROL_NAMES['last']] = value
        def fdel(self: '_control') -> None:
            del self[self.CONTROL_NAMES['last']]
        return locals()
    last = property(**last())

    # def __getitem__(self: '_control', item: object) -> object:
    #     if item == '$':
    #         quit()
    #     if __debug__ and item not in self.flat:
    #         raise KeyError("key '{}' doesn't exist!".format(item))
    #     return dict(self.flatpair)[item]


class knowndict(flatdict):
    """ The object that keeps tracks of all the currently known variables. """

    SCOPE_NAMES = {'global':'_$g', 'local': '_$l', 'control': '_$i'}
    def __init__(self: 'knowndict', consts: 'constants', args: dict = None) -> None:
        super().__init__(args or {})
        self.consts = consts
        self.g, self.l = flatdict(), flatdict()
        self.c = _control(self)

    def g():
        doc = "The known global variables"
        def fget(self: 'knowndict') -> 'node':
            return self[self.SCOPE_NAMES['global']]

        def fset(self: 'knowndict', value: 'node') -> None:
            self[self.SCOPE_NAMES['global']] = value

        def fdel(self: 'knowndict') -> None:
            self[self.SCOPE_NAMES['global']] = flatdict()
        return locals()
    g = property(**g())

    def c():
        doc = "The known control variables"
        def fget(self: 'knowndict') -> 'node':
            return self.l[self.SCOPE_NAMES['control']]

        def fset(self: 'knowndict', value: 'node') -> None:
            self.l[self.SCOPE_NAMES['control']] = value

        def fdel(self: 'knowndict') -> None:
            self.l[self.SCOPE_NAMES['control']] = flatdict()
        return locals()
    c = property(**c())

    def l():
        doc = "The known local variables"
        def fget(self: 'knowndict') -> ('node', flatdict):
            return self[self.SCOPE_NAMES['local']]

        def fset(self: 'knowndict', value: ('node', dict)) -> None:
            self[self.SCOPE_NAMES['local']] = value

        def fdel(self: 'knowndict') -> None:
            self[self.SCOPE_NAMES['local']] = flatdict()
        return locals()
    l = property(**l())

    # def __getitem__(self: 'flatdict', item: object) -> object:
    #     ret = super().__getitem__(item)
    #     print(item, repr(ret))
    #     # print(super(flatdict, ret).__str__())
    #     # if not isinstance(ret, flatdict):
    #     #     return ret
    #     return ret
    #     # if item in super().__getitem__(self.SCOPE_NAMES['control']):
    #     #     return self.c[item]
    #     # return super().__getitem__(item)

    def __setitem__(self: 'knowndict', item: object, val: 'node') -> None:
        #TODO: make it so when you set an item, and it exists further down, it sets it there instead.
        ret = super().__setitem__(item, val)
        if item[:2] != '_$':
            self.c.last = val
        return ret
    def __str__(self: 'knowndict') -> None:
        return '{' + ', '.join(str(k) + ': ' + str(v) for k,v in self.flatpair if not isinstance(v, flatdict)) + '}'