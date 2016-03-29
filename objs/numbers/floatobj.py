from objs import numobj, pyobj
class floatobj(numobj, pyobj):
    """ A floating point number. """
    _regex = r'\b(\d+)?(\.)?(?(1)\d*|\d+)(?(2)[fF]?|[fF])\b'
    # _pyobj = float
    class _float(float):
        def __div__(self, other): return self / other
        def __rdiv__(self, other): return other / self
    _pyobj = _float
    _pyobj_rank = 2

    @staticmethod
    def _genfromstr(data):
        return data[0:data[-1] in 'fF' and -1 or None], floatobj()