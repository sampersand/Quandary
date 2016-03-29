from objs import obj, pyobj
class strobj(pyobj, obj):
    """ A String object. """
    _regex = r'["\'].*["\']'
    _pyobj = str
    _pyobj_rank = 4
    def __add__(self, left, right, knowndict):
        if left.data[-1] in knowndict.consts.punc.quotes:
            pass
        # if args[0][-1] in args[0].control
