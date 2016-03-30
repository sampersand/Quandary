from objs import numobj, pyobj, regexobj
class floatobj(regexobj, pyobj, numobj):
    """ A floating point number. """
    _regex = r'\b([0-9]+)?(\.)?(?(1)[0-9]*|[0-9]+)(?(2)[fF]?|[fF])\b'
    # _pyobj = float
    class _float(float):
        def __div__(self, other): return self / other
        def __rdiv__(self, other): return other / self
    _pyobj = _float
    _pyobj_default_rank = 2

    # @classmethod
    # def fromstr(self: type, data: str, consts: 'constants') -> 'obj':
    #     return data[0:data[-1] in 'fF' and -1 or None], floatobj()