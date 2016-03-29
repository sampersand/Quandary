from objs import obj, pyobj
class strobj(pyobj, obj):
    """ A String object. """
    _regex = r'["\'].*["\']'
    _pyobj = str
    _pyobj_rank = 4
    def __add__(self, left, right, knowndict):
        ldata, rdata = str(left.data), str(right.data)
        if ldata[-1] in knowndict.consts.punc.quotes:
            data = ldata[:-1] + rdata + ldata[-1]
        else:
            data = ldata + rdata
        return left.new(data = data, obj = strobj)
        # if args[0][-1] in args[0].control
