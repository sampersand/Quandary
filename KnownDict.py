from Node import node
class _dict(dict):
    """
        A dicitonary that uses all of it's elements.
        That is, when cycling through, getting, setting (elements that are there), or deleting, it will go through
        it, and all subdicts.
        Terminology note: subdict is any _dict that is a 'value' (rather than a key).
    """
    def __new__(self, *a):
        """ creates a new instance of _dict. """
        return super().__new__(self, {})
    def __init__(self, *a):
        """ forces passing to be ('1', 2, '3', 4, ...), and will gen {'1':2, '3':4}. """
        super().__init__(zip((a[x] for x in range(len(a)) if not x & 1), (a[x] for x in range(len(a)) if x & 1)))

    @property
    def flat(self):
        """ A generator that yields each key from this class and any subdicts. """
        return (kv[0] for kv in self.flatpair)

    @property
    def flatpair(self):
        """ A generator that yields a tuple of (key, value) from each elementin this and each subdict. """
        for k in self:
            v = super().__getitem__(k)
            if isinstance(v, _dict):
                for n in v.flatpair:
                    yield n
            else:
                yield k, v
        
    def __contains__(self, item: str) -> bool:
        """ Returns true if this or any of the subdicts contain 'item'. """
        return item in self.flat

    def __getitem__(self, item: str) -> 'node':
        if __debug__ and item not in self.flat:
            raise KeyError("'{}' doesn't exist!".format(item))
        return dict(self.flatpair)[item]
        # for k, v in self.flatpair:
        #     if k == item:
        #         return v

    def __delitem__(self, item: str):
        for k in self:
            v = super().__getitem__(k)
            if k == item:
                return v
            if isinstance(v, dict) and item in v:
                return v[item]

    def __repr__(self):
        return '_d' + super().__repr__()
class knowndict(_dict):
    """ The object that keeps tracks of all the currently known variables. """

    def __init__(self):
        self['$'] = _dict('1',2,'3',_dict('5', 6, '9', 0))

q = knowndict()
print(q, '1' in q)
q.__delitem__('1')
print(q, q['5'])


