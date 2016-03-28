from objs import numobj
class complexobj(numobj):
    """ A complex object """
    _regex = r'((\d+)?\.(?(2)\d*|\d+)[iIjJ])'