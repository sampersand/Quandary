class obj():
    """ The overarching class for all objects. """
    def __init__(self: 'obj') -> None:
        pass # not required, i just want it here

    def __repr__(self: 'obj', **kwargs: dict) -> str:
        return type(self).__qualname__+'({})'.\
            format(kwargs and ', '.join(str(k) + ' = ' + str(v) for k,v in kwargs.items()) or '')

    @classmethod
    def fromstr(self: type, data: str, consts: 'constants') -> ((str, 'obj'), None):
        return None

    def _oper_attribute(self: 'obj', left: 'node', right: 'node', v: 'flatdict') -> 'node':
        from objs import varobj
        if isinstance(right.obj, varobj):
            return self._oper_attribute_getattr(left, right.data, v)
        return NotImplemented

    def _oper_attribute_getattr(self: 'strobj', left: 'node', attr: str, v: 'flatdict') -> 'node':
        return NotImplemented