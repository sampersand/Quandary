import copy
from decimal import Decimal
from typing import Callable
from types import GeneratorType as gentype
from objs import varobj, funcobj
class operobj(funcobj):
    """ An operator. """

    @staticmethod
    def _pop(tstack, knowns, pos = -1, dothrow = True):
        ret = tstack.pop(pos)
        if ret.obj.isreference():
            if ret.data in knowns: #doesn't check for anything else
                return knowns[ret.data]
            elif dothrow: 
                raise SyntaxError("Unknown variable '{}'!".format(ret.data))
        knowns.c.last = ret #is this a good place to put it
        return ret

    def evaloper(self: 'operobj',
                 tstack: list,
                 ostack: list,
                 gen: gentype,
                 knowns: 'knownsdict',
                 oper: str,
                 opers = None) -> 'node':
        """ if opers are none, use knowns.consts.keywords.opers"""
        opers = opers or knowns.consts.keywords.opers
        if __debug__:
            assert oper in opers, "Trying to evaloper with no operator!"
            reqs = opers[oper]['reqs']
            assert len(tstack) >= min(reqs[0]), "Too few tokens {} to perform '{}' ({})".format(tstack, oper, reqs[0])
            assert len(ostack) >= min(reqs[1]), "Too few opers {} to perform '{}' ({})".format(ostack, oper, reqs[1])
            del reqs
        ret = NotImplemented

        #first see if it's a simple operator
        if ret == NotImplemented and oper in opers['simple_binary']:
            ret = self._eval_simple(tstack, ostack, gen, knowns, oper)

        #second see if it's an assignment
        elif ret == NotImplemented and oper in opers['assignment']:
            ret = self._eval_assign(tstack, ostack, gen, knowns, oper)

        #third, see if it's a deliminator
        elif ret == NotImplemented and oper in opers['delims']:
            ret = self._eval_delim(tstack, ostack, gen, knowns, oper)

        #lastly, throw an exception
        if ret == NotImplemented:
            raise AttributeError("No known way to apply operator '{}' to stacks '{}' and '{}'".format(\
                oper, tstack, ostack))
        return ret

    def _eval_simple(self: 'operobj',
                    tstack: list,
                    ostack: list,
                    gen: gentype,
                    knowns: 'knownsdict',
                    oper: str) -> ('node', NotImplemented):
        ret = NotImplemented
        left = self._pop(tstack, knowns, -2)
        right = self._pop(tstack, knowns)

        #first, try 'a.__OPER__.(b)'
        if ret == NotImplemented and hasattr(left.obj, left.consts.opers[oper]['loper']) and\
                left.obj == left.obj._pyobj_compare(right.obj): # KeyError: oper isnt recognized
            #problem is int base 2 and int base 10 are the same priority... maybe 2.02 and 2.10
            ret = getattr(left.obj, left.consts.opers[oper]['loper'])(left, right, knowns)

        #second, try 'b.__iOPER__.(a)'
        if ret == NotImplemented and hasattr(right.obj, left.consts.opers[oper]['roper']) and\
                right.obj == right.obj._pyobj_compare(left.obj): #KeyError: oepr isnt recognized
            ret = getattr(right.obj, left.consts.opers[oper]['roper'])(right, left, knowns)

        return ret

    def _eval_assign(self: 'operobj',
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

    def _eval_delim(self: 'operobj',
                   tstack: list,
                   ostack: list,
                   gen: gentype,
                   knowns: 'knownsdict',
                   oper: str) -> ('node', NotImplemented):
        ret = NotImplemented

        if ret == NotImplemented and oper == ';':
            ret = self._pop(tstack, knowns)

        if ret == NotImplemented and oper == '.':
            """ if len(ostack) - len(tstack) == 2: 'tstack[-2].tstack[-1]'
                if len(ostack) - len(tstack) == 1: '0.tstack[-1]'
                else: NotImplemented
            """
            if ret == NotImplemented and (len(tstack) - len(ostack)) == 1:
                ret = tstack[-1].new(data = str('0.'+self._pop(tstack, knowns).data), genobj = True)
            
            if ret == NotImplemented and (len(tstack) - len(ostack)) == 2:
                ret = tstack[-1].new(
                           data = str(self._pop(tstack, knowns, -2).data + '.' + self._pop(tstack, knowns).data),
                           genobj = True)
        
        return ret

    @classmethod
    def fromstr(self: type, data: str, consts: 'constants') -> ((str, 'operobj'), None):
        if data in consts.opers:
            return data, consts.opers[data]['obj']()
        return None























