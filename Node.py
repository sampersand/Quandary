class node():
    def __init__(self, const, **kwargs):
        super().__setattr__('const', const)
        super().__setattr__('_attrs', {})
        for key in kwargs:
            self._attrs[key] = kwargs[key]

    def __getattr__(self, attr):
        """ gets 'self._attrs[attr]' """
        return self._attrs[attr]
    def __setattr__(self, attr, val):
        """ sets 'self._attrs[attr]' to val"""
        self._attrs[attr] = val
    def __delattr__(self, attr):
        """ deletes 'attr' from self._attrs """
        del self._attrs[attr]

    @property
    def attrs(self):
        return {k:self._attrs[k] for k in self._attrs if k != 'const'}
    
    @staticmethod
    def fromiter(const, itrable):
        if __debug__:
            assert hasattr(itrable, '__iter__'), 'cannot run fromiter on a non-iterable...'
        args = []
        return node(const, args = args)

    def __repr__(self):
        return repr(self.attrs)
