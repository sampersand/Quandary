from objs import numobj, pyobj
class complexobj(numobj, pyobj):
    """ A complex object """
    _regex = r'\b((\d+)?\.(?(2)\d*|\d+)[iIjJ])\b'
    _pyobj = complex
    _pyobj_rank = 3