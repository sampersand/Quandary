class complexobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('numobj')):
    """ A complex object """
    _regex = r'\b((\d+)?\.(?(2)\d*|\d+)[iIjJ])\b'
    _pyobj = complex