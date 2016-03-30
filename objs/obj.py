class obj():
    """ The overarching class for all objects. """
    def __init__(self: 'obj') -> None:
        pass # not required, i just want it here

    def __repr__(self: 'obj', **kwargs: dict) -> str:
        return type(self).__qualname__+'({})'.\
            format(kwargs and ', '.join(str(k) + ' = ' + str(v) for k,v in kwargs.items()) or '')

    def isreference(self: 'obj') -> bool:
        """ True if this class is a reference to another object. Currently, only varobj returns true."""
        return False

    @classmethod
    def fromstr(self: type, data: str, consts: 'constants') -> ((str, 'obj'), None):
        return None

    def _oper_attribute(self: 'strobj', left: 'node', right: 'node', knowns: 'knowndict') -> ('node', NotImplemented):
        if right.obj.isreference():
            return self._oper_attribute_attr(left, right.data, knowns)
        return NotImplemented

    def _oper_rattribute(self: 'strobj', left: 'node', right: 'node', knowns: 'knowndict') -> ('node', NotImplemented):
        return _oper_attribute

    def _oper_attribute_attr(self: 'strobj', left: 'node', attr: str, knowns: 'knowndict') -> 'node':
        return NotImplemented