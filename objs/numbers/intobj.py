from objs import numobj, pyobj
class intobj(numobj, pyobj):
    """ A whole number. """
    _regex = r'\b([1-9][0-9]*|0)[wW]?\b' #w for whole
    _pyobj = int
    _pyobj_rank = 1