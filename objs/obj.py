class obj():
    """ The overarching class for all objects. """
    def __init__(self: 'obj') -> None:
        pass # not required, i just want it here

    def __repr__(self: 'obj', **kwargs: dict) -> str:
        return type(self).__qualname__+'({})'.\
            format(kwargs and ', '.join(str(k) + ' = ' + str(v) for k,v in kwargs.items()) or '')

    @classmethod
    def fromstr(self: type, data: str, consts: 'constants') -> 'obj':
        return None