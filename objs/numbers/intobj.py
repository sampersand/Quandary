from objs import numobj, pyobj, floatobj, regexobj
class intobj(regexobj, pyobj, numobj):
    """ A whole number. """
    BASES = {'0x': 16, '0o': 8, '0b': 2, '0d': 10, 'default': 10}
    _regex = r'''(?x)
        ([1-9][0-9]*|
            [0]
            (
                ([xX][0-9A-Fa-f]*)|
                ([oO][0-7]*)|
                ([bB][01]*)|
                ([dD][0-9]*)
            )?
        )[wW]?
        ''' #w for whole
    _pyobj = int
    _pyobj_rank = 1

    def __init__(self: 'intobj', base = None) -> None:
        super().__init__()
        self.base = base or self.BASES['default']

    def __repr__(self: 'intobj') -> str:
        return super().__repr__(base = self.base) 


    def _pyobj_valof(self: 'intobj', node: 'node') -> int:
        print(node.data, self.base, '@', self, node, node.obj)
        return int(node.data, self.base)

    def _oper_div(self: 'intobj', left: 'node', right: 'node', knowns: 'knowndict') -> 'node':
        """ 
            if l and r are ints, return int
            if l or r is float, return float
        """
        if __debug__:
            assert hasattr(right.obj, '_pyobj'), "Cannot divide an '{}' by a non-simple type '{}'".format(left.obj,
                                                                                                          right.obj)
        result = left.obj._pyobj_valof(left) / right.obj._pyobj_valof(right)
        result = int(result) if float(result) == int(result) else float(result)
        return left.new(data = str(result), obj = isinstance(result, int) and intobj or floatobj)
    @classmethod
    def fromstr(self: type, data: str, consts: 'constants') -> ((str, 'regexobj'), None):
        ret = super().fromstr(data, consts)
        if ret == None:
            return ret
        base = self.BASES['default']
        if len(ret) > 1 and ret[0][:2] in self.BASES:
            base = self.BASES[ret[0][:2]]
        return ret[0], intobj(base = base)
