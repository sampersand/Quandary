from objs import numobj
class complexobj(numobj):
    """ A complex object """
    _regex = r'\b((\d+)?\.(?(2)\d*|\d+)[iIjJ])\b'
    _pyobj = complex