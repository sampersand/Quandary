class _dict(dict):
    def __new__(self, *a):
        return super().__new__(self, {})
    def __init__(self, *a):
        """ forces passing to be ('1', 2, '3', 4, ...), and will gen {'1':2, '3':4}. """
        super().__init__(zip((a[x] for x in range(len(a)) if not x & 1), (a[x] for x in range(len(a)) if x & 1)))

    def flatiter(self):
        for k in self:
            v = super().__getitem__(k)
            if isinstance(v, dict):
                for n in getattr(v, isinstance(v, _dict) and 'flatiter' or '__iter__')():
                    yield n
            else:
                yield k
        
    def __contains__(self, item: str) -> bool:
        # print(list(self.flatiter()),'@')
        return item in self.flatiter()
        # for k in self.flatiter():


    def __getitem__(self, item: str):
        for k in self:
            v = super().__getitem__(k)
            if k == item:
                return v
            if isinstance(v, dict) and item in v:
                return v[item]

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
print(q)

