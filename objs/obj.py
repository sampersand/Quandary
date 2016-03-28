class obj():
    """ The overarching class for all objects. """
    _pyobj = None
    def __init__(self): pass #not required, i just want it here

    def __repr__(self: 'obj') -> str:
        return type(self).__qualname__+'()'

    def __getattr__(self: 'obj', attr: str) -> object:
        if attr[:2] == attr [-2:] == '__' and self._pyobj != None: #aka, its a magic method
            return __import__((__package__ + ' ')[:__package__.find('.')])._import('pyobj')().__getattr__(attr)
        return super().__getattr__(attr)