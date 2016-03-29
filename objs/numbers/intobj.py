from objs import numobj, pyobj
from objs import floatobj
class intobj(pyobj, numobj):
    """ A whole number. """
    _regex = r'\b([1-9][0-9]*|0)[wW]?\b' #w for whole
    _pyobj = int
    _pyobj_rank = 1
    def __div__(self, left, right, knowndict):
        """ 
            if l and r are ints, return int
            if l or r is float, return float
        """
        if __debug__:
            assert hasattr(right.obj, '_pyobj'), "Cannot divide an '{}' by a non-simple type '{}'".format(left.obj,
                                                                                                          right.obj)
        result = left.obj._pyobj(left.data) / right.obj._pyobj(right.data)
        result = int(result) if float(result) == int(result) else float(result)
        return left.new(data = str(result), obj = isinstance(result, int) and intobj or floatobj)
    @staticmethod
    def _genfromstr(data):
        return data[0:data[-1] in 'wW' and -1 or None], floatobj()