class obj():
    """ The overarching class for all objects. """
    _pyobj = None
    def __init__(self): pass #not required, i just want it here

    def __repr__(self: 'obj') -> str:
        return type(self).__qualname__+'()'