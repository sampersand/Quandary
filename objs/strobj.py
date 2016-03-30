from objs import obj, pyobj, regexobj
class strobj(regexobj, pyobj, obj):
    """ A String object. """
    _regex = r'(["\']).*\1'
    _pyobj = str
    _pyobj_rank = 4

    @staticmethod
    def _isquotedstr(s: str, consts: 'constants') -> bool:
        return s[0] in consts.punc.quotes and s[-1] in consts.punc.quotes

    def _oper_radd(self: 'strobj', right: 'node', left: 'node', knowns: 'knowndict') -> 'node':
        return self._oper_add(left, right, knowns)

    def _oper_add(self: 'strobj', left: 'node', right: 'node', knowns: 'knowndict') -> 'node':
        """ 
            if l is quoted and r is quoted, use l's quotes.
            if one and not the other is quoted, use that one's quotes
            if neither are quoted, use no quotes
        """
        lstr, rstr = str(left.data), str(right.data)
        lisq, risq = self._isquotedstr(lstr, knowns.consts), self._isquotedstr(rstr, knowns.consts)
        if lisq:
            data = lstr[:-1] + (rstr[1:-1] if risq else rstr) + lstr[-1]
        elif risq:
            data = rstr[0] + lstr + rstr[1:]
        else:
            data = lstr + rstr
        return left.new(data = data, obj = strobj)
        # if args[0][-1] in args[0].control

    def _oper_attribute(self: 'strobj', left: 'node', right: 'node', knowns: 'knowndict') -> 'node':
        ret = super()._oper_attribute(left, right, knowns)
        if ret != NotImplemented:
            return ret
        if not isinstance(right.obj, intobj):
            return NotImplemented
        #This is assuming that both left and right are intobjs
        #This is effectively ####.####
        return left.new(data = '{}.{}'.format(left.obj._pyobj_valof(left), left.obj._pyobj_valof(right)), genobj = True)

























