from typing import Callable
import copy
varobj = __import__((__package__ + ' ')[:__package__.find('.')])._import('varobj')
class operobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('funcobj')):
    """ An operator. """
    def evaloper(self: 'operobj', tstack: list, ostack: list, knowns: 'knownsdict', oper: str) -> 'node':
        opers = knowns.consts.keywords.opers
        if __debug__:
            assert oper in opers, "Trying to evaloper with no operator!"
            reqs = opers[oper]['reqs']
            assert len(tstack) >= reqs[0], "Too few tokens ({}) to perform {} ({})".format(tstack, oper, reqs[0])
            assert len(ostack) >= reqs[1], "Too few opers ({}) to perform {} ({})".format(ostack, oper, reqs[1])
            del reqs
        ret = NotImplemented
        if oper in opers['assignment']:
            ret = self._evalassign(tstack, ostack, knowns, oper)
    #     args = [next(gen) for x in range(base.)]

    #     if oper in left.consts.opers['assignment']:
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

    def _evalsimple(self: 'operobj', tstack: list, ostack: list, knowns: 'knownsdict', oper: str) -> 'node':
        pass
    def _evalassign(self: 'operobj', tstack: list, ostack: list, knowns: 'knownsdict', oper: str) -> 'node':
        direc = oper == '->'
        left = tstack.pop(-1 -direc) #if direc is 1, pop second to last.
        right = tstack.pop()
        if __debug__:
            assert type(right.obj) == varobj, "Not able to assignment a value to the non-var obj '{}'".format(right.obj)
            assert list(sorted(right.attrs.keys())) == ['data', 'obj'] #can only be data and object,
                                                                       # nothing more complex than that
        knowns[right.data] = left
        return knowns[right.data]






