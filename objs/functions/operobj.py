import copy
from decimal import Decimal
from typing import Callable
from types import GeneratorType as gentype
from objs import varobj, funcobj
class operobj(funcobj):
    """ An operator. """

    @staticmethod
    def _getobj(node: 'node', v: 'flatdict') -> 'node':
        if isinstance(node.obj, varobj) and node.data in v.knowns: #doesn't check for anything else
            return v.knowns[node.data]
        return node

    @staticmethod
    def _pop(ts: list, v: 'flatdict', pos: int = -1)-> 'node':
        ret = operobj._getobj(ts.pop(pos), v)
        v.knowns.c.last = ret #this is the last element fount
        return ret

    def evaloper(self: 'operobj', v: 'flatdict', oper: str) -> 'node':
        """ if opers are none, use v.knowns.consts.keywords.opers"""
        opers = v.knowns.consts.keywords.opers
        if __debug__:
            assert oper in opers, "Trying to evaloper with no operator!"
            reqs = opers[oper]['reqs']
            assert len(v.ts) >= min(reqs[0]),\
                "Too few tokens {} to perform '{}' ({})".format(v.ts, oper, reqs[0])
            assert len(v.os) >= min(reqs[1]),\
                "Too few opers {} to perform '{}' ({})".format(v.os, oper, reqs[1])
            del reqs

        worked = False
        #first see if it's a simple operator
        if worked == False and oper in opers['simple_binary']:
            worked = self._eval_simple(v, oper)

        #second see if it's an assignment
        elif worked == False and oper in opers['assignment']:
            worked = self._eval_assign(v, oper)

        #third, see if it's a deliminator
        elif worked == False:
            worked = self._eval_etc(v, oper)

        #lastly, throw an exception
        if worked == False:
            raise AttributeError("No known way to apply operator '{}' to stacks '{}' and '{}'".format(\
                oper, v.ts, v.os))

    def _eval_simple(self: 'operobj', v: 'flatdict', oper: str) -> bool:
        left = self._getobj(v.ts[-2], v)
        right = self._getobj(v.ts[-1], v)

        #first, try 'a.__OPER__.(b)'
        if hasattr(left.obj, v.consts.opers[oper]['loper']) and\
                left.obj == left.obj._pyobj_compare(right.obj): # KeyError: oper isnt recognized
            result = getattr(left.obj, v.consts.opers[oper]['loper'])(left, right, v)
            if result != NotImplemented:
                v.ts.pop(); v.ts.pop(); v.ts.append(result);
                return True
        #second, try 'b.__rOPER__.(a)'
        if hasattr(right.obj, left.consts.opers[oper]['roper']) and\
                right.obj == right.obj._pyobj_compare(left.obj): #KeyError: oepr isnt recognized
            result = getattr(right.obj, left.consts.opers[oper]['roper'])(right, left, v)
            if result != NotImplemented:
                v.ts.pop(); v.ts.pop(); v.ts.append(result);
                return True

        return False

    def _eval_assign(self: 'operobj',
                    ts: list,
                    os: list,
                    gen: gentype,
                    knowns: 'knownsdict',
                    oper: str) -> bool:
        direc = oper == '->'
        left = ts.pop(~direc) #if direc is 1, pop second to last.
        right = ts.pop()
        if __debug__:
            assert type(right.obj) == varobj, "Not able to assignment a value to the non-var obj '{}'".format(right.obj)
            assert list(sorted(right.attrs.keys())) == ['data', 'obj'] #can only be data and object,
                                                                       # nothing more complex than that
        knowns[right.data] = left
        ts.append(knowns[right.data])
        return True

    def _eval_etc(self: 'operobj',
                   ts: list,
                   os: list,
                   gen: gentype,
                   knowns: 'knownsdict',
                   oper: str) -> bool:
        if oper == ';':
            while os:
                print(os, ts)
                os[-1]._reduce_os(ts, os, gen, knowns)
            ts.append(self._pop(ts, knowns))
            return True
        return False

        # if ret == NotImplemented and oper == '.':
        #     """ if len(os) - len(ts) == 2: 'ts[-2].ts[-1]'
        #         if len(os) - len(ts) == 1: '0.ts[-1]'
        #         else: NotImplemented
        #     """
        #     if ret == NotImplemented and hasattr(left.obj, left.consts.opers[oper]['loper']) and\
        #             left.obj == left.obj._pyobj_compare(right.obj): # KeyError: oper isnt recognized
        #         #problem is int base 2 and int base 10 are the same priority... maybe 2.02 and 2.10
        #         ret = getattr(left.obj, left.consts.opers[oper]['loper'])(left, right, knowns)

        #     #second, try 'b.__rOPER__.(a)'
        #     if ret == NotImplemented and hasattr(right.obj, left.consts.opers[oper]['roper']) and\
        #             right.obj == right.obj._pyobj_compare(left.obj): #KeyError: oepr isnt recognized
        #         ret = getattr(right.obj, left.consts.opers[oper]['roper'])(right, left, knowns)

            # if ret == NotImplemented and (len(ts) - len(os)) == 1:
            #     ret = ts[-1].new(data = str('0.'+self._pop(ts, knowns).data), genobj = True)
            
            # if ret == NotImplemented and (len(ts) - len(os)) == 2:
            #     ret = ts[-1].new(
            #                data = str(self._pop(ts, knowns, -2).data + '.' + self._pop(ts, knowns).data),
            #                genobj = True)

    @classmethod
    def fromstr(self: type, data: str, consts: 'constants') -> ((str, 'operobj'), None):
        if data in consts.opers:
            return data, consts.opers[data]['obj']()
        return None

















