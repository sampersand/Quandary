class obj():
    """ The overarching class for all objects. """
    def __init__(self: 'obj') -> None:
        pass # not required, i just want it here

    def __repr__(self: 'obj', **kwargs: dict) -> str:
        return type(self).__qualname__+'({})'.\
            format(kwargs and ', '.join(str(k) + ' = ' + str(v) for k,v in kwargs.items()) or '')

    def __getattr__(self: 'obj', attr: str) -> object:
        if len(attr) < 2 or attr[:2] != 'is':
            raise SyntaxError("Unknown {} attribute '{}'!".format(type(self), attr))
        return False#attr[2:] in self._ATTRS

    @classmethod
    def fromstr(self: type, data: str, consts: 'constants') -> ((str, 'obj'), None):
        return None

