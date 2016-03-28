from typing import Callable
import copy
class operobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('funcobj')):
    """ An operator. """
    def evalobj(self: 'operobj', knowns: 'knownsdict', gen: Callable, *args: (list, tuple), **kwargs: dict) -> 'node':
        if __debug__:
            assert 'oper' in kwargs, "Cannot evalobj on an operobj with no operator!"
            assert len(args) == 2, "currently, only accepting binary functions"
            assert 'obj' in args[0], "Cannot evaluate a node with no object!"

        oper = kwargs['oper']
        left, rght = args
        ret = NotImplemented

        if oper in left.consts.operators['assignment']:
            quit()

        #first, try 'a.__OPER__.(b)'
        if hasattr(left.obj, left.consts._loperfuncs[oper]): #if this rasies a KeyError, its b/c oper isn't recognized
            ret = getattr(left.obj, left.consts._loperfuncs[oper])(left, rght)
        
        #second, try 'b.__iOPER__.(a)'
        if ret == NotImplemented and hasattr(rght.obj, left.consts._roperfuncs[oper]): # KeyError = oper isnt recognized
            ret = getattr(rght.obj, left.consts._roperfuncs[oper])(rght, left)
        
        #lastly, throw an exception
        if ret == NotImplemented:
            raise AttributeError("No known way to apply operator '{}' to objects '{}' and '{}'".format(\
                oper, left, rght))
        return ret
