from typing import Callable
import copy
varobj = __import__((__package__ + ' ')[:__package__.find('.')])._import('varobj')
class operobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('funcobj')):
    """ An operator. """
    def evaloper(self: 'operobj', tstack: list, ostack: list, knowns: 'knownsdict', oper: str) -> 'node':
        if __debug__:
            assert oper in knowns.consts.keywords.operators
        if oper in knowns.consts.operators['assignment']:
            pass
    #     args = [next(gen) for x in range(base.)]
    #     ret = NotImplemented

    #     if oper in left.consts.operators['assignment']:
    #         ret = self._evaloper(knowns, gen, *args, **kwargs)


    #     #first, try 'a.__OPER__.(b)'
    #     if ret == NotImplemented and hasattr(left.obj, left.consts._loperfuncs[oper]): # if raises KeyError, its b/c
    #                                                                          # oper isn't recognized
    #         ret = getattr(left.obj, left.consts._loperfuncs[oper])(left, rght)
        
    #     #second, try 'b.__iOPER__.(a)'
    #     if ret == NotImplemented and hasattr(rght.obj, left.consts._roperfuncs[oper]): # KeyError = oper isnt recognized
    #         ret = getattr(rght.obj, left.consts._roperfuncs[oper])(rght, left)
        
    #     #lastly, throw an exception
    #     if ret == NotImplemented:
    #         raise AttributeError("No known way to apply operator '{}' to objects '{}' and '{}'".format(\
    #             oper, left, rght))
    #     return ret

    # def _evaloper(self: 'operobj', knowns: 'knownsdict', gen: Callable) -> 'node':
    #     oper = kwargs['oper']
    #     direc = oper == '->'
    #     left = args[not direc]
    #     rght = args[direc]
    #     if __debug__:
    #         assert type(rght.obj) == varobj, "Not able to assignment a value to the non-basic object '{}'".\
    #             format(rght.obj)
    #         assert list(sorted(rght.attrs.keys())) == ['data', 'obj'] #can only be data and object,
    #                                                                    # nothing more complex than that
    #     knowns[rght.data] = left
    #     return knowns[rght.data]