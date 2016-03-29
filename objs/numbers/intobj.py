from objs import numobj, pyobj, floatobj
class intobj(pyobj, numobj):
    """ A whole number. """
    BASES = {'0x': 16, '0o': 8, '0b': 2, '0d': 10, 'default': 10}
    _regex = r'''(?x)\b
        ([1-9][0-9]*|
            [0]
            (
                ([xX][0-9A-Fa-f]*)|
                ([oO][0-7]*)|
                ([bB][01]*)|
                ([dD][0-9]*)
            )?
        )[wW]?\b
        ''' #w for whole
    _pyobj = int
    _pyobj_rank = 1
    def __init__(self, base = BASES['default']):
        self.base = base

    def __repr__(self):
        return super().__repr__(base = self.base) 


    def getpyval(self:'intobj', node: 'node'):
        return int(node.data, self.base)

    # _regex = r'\b([1-9][0-9]*|0)[wW]?\b' #w for whole
    def __div__(self, left, right, knowndict):
        """ 
            if l and r are ints, return int
            if l or r is float, return float
        """
        if __debug__:
            assert hasattr(right.obj, '_pyobj'), "Cannot divide an '{}' by a non-simple type '{}'".format(left.obj,
                                                                                                          right.obj)
        result = left.obj.getpyval(left) / right.obj.getpyval(right)
        result = int(result) if float(result) == int(result) else float(result)
        return left.new(data = str(result), obj = isinstance(result, int) and intobj or floatobj)
    @staticmethod
    def _genfromstr(data):
        return data[0:data[-1] in 'wW' and -1 or None],\
            intobj(intobj.BASES[data[:2]] if len(data) > 1 and data[:2] in intobj.BASES else intobj.BASES['default'])
































