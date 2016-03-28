from objs import numobj, pyobj
class floatobj(numobj, pyobj):
    """ A floating point number. """
    _regex = r'\b(\d+)?\.(?(1)\d*|\d+)[fF]?\b'
    _pyobj = float