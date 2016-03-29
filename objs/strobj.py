from objs import obj, pyobj
class strobj(pyobj, obj):
    """ A String object. """
    _regex = r'["\'].*["\']'
    _pyobj = str
    _pyobj_rank = 4
    @staticmethod
    def _isquotedstr(s: str, consts: 'constants'):
        return s[0] in consts.punc.quotes and s[-1] in consts.punc.quotes

    def __radd__(self, right, left, knowndict):
        return self.__add__(left, right, knowndict)
    def __add__(self, left, right, knowndict):
        """ 
            if l is quoted and r is quoted, use l's quotes.
            if one and not the other is quoted, use that one's quotes
            if neither are quoted, use no quotes
            """
        lstr, rstr = str(left.data), str(right.data)
        lisq, risq = self._isquotedstr(lstr, knowndict.consts), self._isquotedstr(rstr, knowndict.consts)
        if lisq:
            data = lstr[:-1] + (rstr[1:-1] if risq else rstr) + lstr[-1]
        elif risq:
            data = rstr[0] + lstr + rstr[1:]
        else:
            data = lstr + rstr
        return left.new(data = data, obj = strobj)
        # if args[0][-1] in args[0].control
