from typing import Callable
import copy
class operobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('funcobj')):
    """ An operator. """
    def evalobj(knowns: 'knownsdict', gen: Callable, *args: (list, tuple), **kwargs: dict) -> 'node':
        if __debug__:
            assert 'oper' in kwargs, "Cannot evalobj on an operobj with no operator!"
            assert len(args) == 2, "currently, only accepting binary functions"
            assert 'obj' in args[0], "Cannot evaluate a node with no object!"
        oper = kwargs['oper']
        base = args[0]
        othr = args[1]
        ret = getattr(base.obj, base.consts._loperfuncs[oper])(base, othr)
        if ret == NotImplemented:
            ret = getattr(othr.obj, base.consts._roperfuncs[oper])(base, base)
            if ret == NotImplemented:
                raise AttributeError("No known way to apply operator '{}' to objects '{}' and '{}'".format(\
                    oper, base, othr))
        return ret
