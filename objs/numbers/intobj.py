from objs import numobj
class intobj(numobj):
    """ A whole number. """
    _regex = r'\b([1-9][0-9]*|0)[wW]?\b' #w for whole
    _pyobj = int