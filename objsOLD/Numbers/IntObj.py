from objs import numobj
class intobj(numobj):
    """ A whole number. """
    _regex = r'([1-9][0-9]*|0)[wW]?' #w for whole
