import copy
from decimal import Decimal
from typing import Callable
from types import GeneratorType as gentype
from objs import varobj, funcobj
class operobj(funcobj):
    """ An operator. """

    @staticmethod
    def _getobj(node: 'node', knowns: 'knownsdict', dothrow: bool = True) -> 'node':
        if node.obj.isreference():
            if node.data in knowns: #doesn't check for anything else
                return knowns[node.data]
            elif dothrow: #not throwing for now because some cases it isn't needed
                pass
                # raise SyntaxError("Unknown variable '{}'!".format(node.data))
        return node
    @staticmethod
    def _pop(tstack: list, knowns: 'knownsdict', pos: int = -1, dothrow: bool = True)-> 'node':
        ret = operobj._getobj(tstack.pop(pos), knowns, dothrow)
        knowns.c.last = ret #this is the last element fount
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
        worked = False

        #first see if it's a simple operator
        if worked == False and oper in opers['simple_binary']:
            worked = self._eval_simple(tstack, ostack, gen, knowns, oper)

        #second see if it's an assignment
        elif worked == False and oper in opers['assignment']:
            worked = self._eval_assign(tstack, ostack, gen, knowns, oper)

        #third, see if it's a deliminator
        elif worked == False:
            worked = self._eval_etc(tstack, ostack, gen, knowns, oper)

        #lastly, throw an exception
        if worked == False:
            raise AttributeError("No known way to apply operator '{}' to stacks '{}' and '{}'".format(\
                oper, tstack, ostack))

    def _eval_simple(self: 'operobj',
                    tstack: list,
                    ostack: list,
                    gen: gentype,
                    knowns: 'knownsdict',
                    oper: str) -> bool:
        left = self._getobj(tstack[-2], knowns)
        right = self._getobj(tstack[-1], knowns)

        #first, try 'a.__OPER__.(b)'
        if hasattr(left.obj, left.consts.opers[oper]['loper']) and\
                left.obj == left.obj._pyobj_compare(right.obj): # KeyError: oper isnt recognized
            result = getattr(left.obj, right.consts.opers[oper]['loper'])(left, right, knowns)
            if result != NotImplemented:
                tstack.pop(); tstack.pop(); tstack.append(result);
                return True
        #second, try 'b.__rOPER__.(a)'
        if hasattr(right.obj, left.consts.opers[oper]['roper']) and\
                right.obj == right.obj._pyobj_compare(left.obj): #KeyError: oepr isnt recognized
            result = getattr(right.obj, left.consts.opers[oper]['roper'])(right, left, knowns)
            if result != NotImplemented:
                tstack.pop(); tstack.pop(); tstack.append(result);
                return True

        return False

    def _eval_assign(self: 'operobj',
                    tstack: list,
                    ostack: list,
                    gen: gentype,
                    knowns: 'knownsdict',
                    oper: str) -> bool:
        direc = oper == '->'
        left = tstack.pop(~direc) #if direc is 1, pop second to last.
        right = tstack.pop()
        if __debug__:
            assert type(right.obj) == varobj, "Not able to assignment a value to the non-var obj '{}'".format(right.obj)
            assert list(sorted(right.attrs.keys())) == ['data', 'obj'] #can only be data and object,
                                                                       # nothing more complex than that
        knowns[right.data] = left
        tstack.append(knowns[right.data])
        return True

    def _eval_etc(self: 'operobj',
                   tstack: list,
                   ostack: list,
                   gen: gentype,
                   knowns: 'knownsdict',
                   oper: str) -> bool:
        if oper == ';':
            while ostack:
                print(ostack, tstack)
                ostack[-1]._reduce_os(tstack, ostack, gen, knowns)
            tstack.append(self._pop(tstack, knowns))
            return True
        return False

        # if ret == NotImplemented and oper == '.':
        #     """ if len(ostack) - len(tstack) == 2: 'tstack[-2].tstack[-1]'
        #         if len(ostack) - len(tstack) == 1: '0.tstack[-1]'
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

            # if ret == NotImplemented and (len(tstack) - len(ostack)) == 1:
            #     ret = tstack[-1].new(data = str('0.'+self._pop(tstack, knowns).data), genobj = True)
            
            # if ret == NotImplemented and (len(tstack) - len(ostack)) == 2:
            #     ret = tstack[-1].new(
            #                data = str(self._pop(tstack, knowns, -2).data + '.' + self._pop(tstack, knowns).data),
            #                genobj = True)

    @classmethod
    def fromstr(self: type, data: str, consts: 'constants') -> ((str, 'operobj'), None):
        if data in consts.opers:
            return data, consts.opers[data]['obj']()
        return None























