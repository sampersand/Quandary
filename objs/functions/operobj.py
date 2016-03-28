import copy
from decimal import Decimal
from typing import Callable
from types import GeneratorType as gentype
from node import node
varobj = __import__((__package__ + ' ')[:__package__.find('.')])._import('varobj')
class operobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('funcobj')):
    """ An operator. """
    def evaloper(self: 'operobj',
                 tstack: list,
                 ostack: list,
                 gen: gentype,
                 knowns: 'knownsdict',
                 oper: str) -> 'node':
        opers = knowns.consts.keywords.opers
        if __debug__:
            assert oper in opers, "Trying to evaloper with no operator!"
            reqs = opers[oper]['reqs']
            assert len(tstack) >= min(reqs[0]), "Too few tokens {} to perform '{}' ({})".format(tstack, oper, reqs[0])
            assert len(ostack) >= min(reqs[1]), "Too few opers {} to perform '{}' ({})".format(ostack, oper, reqs[1])
            del reqs
        ret = NotImplemented

        #first see if it's a simple operator
        if ret == NotImplemented and oper in opers['simple_binary']:
            ret = self._evalsimple(tstack, ostack, gen, knowns, oper)

        #second see if it's an assignment
        elif ret == NotImplemented and oper in opers['assignment']:
            ret = self._evalassign(tstack, ostack, gen, knowns, oper)

        #third, see if it's a deliminator
        elif ret == NotImplemented and oper in opers['delims']:
            ret = self._evaldelim(tstack, ostack, gen, knowns, oper)

        #lastly, throw an exception
        if ret == NotImplemented:
            raise AttributeError("No known way to apply operator '{}' to stacks '{}' and '{}'".format(\
                oper, tstack, ostack))
        return ret


    def _evalsimple(self: 'operobj',
                    tstack: list,
                    ostack: list,
                    gen: gentype,
                    knowns: 'knownsdict',
                    oper: str) -> ('node', NotImplemented):
        ret = NotImplemented
        left = tstack.pop(-2)
        right = tstack.pop()
        #first, try 'a.__OPER__.(b)'
        if ret == NotImplemented and hasattr(left.obj, left.consts._loperfuncs[oper]): # KeyError: oper isnt recognized
            ret = getattr(left.obj, left.consts._loperfuncs[oper])(left, right)
        
        #second, try 'b.__iOPER__.(a)'
        if ret == NotImplemented and hasattr(right.obj, left.consts._roperfuncs[oper]): # KeyError: oper isnt recognized
            ret = getattr(right.obj, left.consts._roperfuncs[oper])(right, left)
        return ret

    def _evalassign(self: 'operobj',
                    tstack: list,
                    ostack: list,
                    gen: gentype,
                    knowns: 'knownsdict',
                    oper: str) -> ('node', NotImplemented):
        direc = oper == '->'
        left = tstack.pop(-1 -direc) #if direc is 1, pop second to last.
        right = tstack.pop()
        if __debug__:
            assert type(right.obj) == varobj, "Not able to assignment a value to the non-var obj '{}'".format(right.obj)
            assert list(sorted(right.attrs.keys())) == ['data', 'obj'] #can only be data and object,
                                                                       # nothing more complex than that
        knowns[right.data] = left
        return knowns[right.data]

    def _evaldelim(self: 'operobj',
                   tstack: list,
                   ostack: list,
                   gen: gentype,
                   knowns: 'knownsdict',
                   oper: str) -> ('node', NotImplemented):
        ret = NotImplemented

        if ret == NotImplemented and oper == ';':
            ret = tstack.pop()

        if ret == NotImplemented and oper == '.':
            """ if len(ostack) - len(tstack) == 2: 'tstack[-2].tstack[-1]'
                if len(ostack) - len(tstack) == 1: '0.tstack[-1]'
                else: NotImplemented
            """
            if ret == NotImplemented and (len(tstack) - len(ostack)) == 1:
                ret = node(knowns.consts, data = str('0.'+tstack.pop().data), genobj = True)
            if ret == NotImplemented and (len(tstack) - len(ostack)) == 2:
                ret = node(knowns.consts, data = str(tstack.pop(-2).data + '.' + tstack.pop().data), genobj = True)
        
        return ret

























