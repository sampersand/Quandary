class complexobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('numobj')):
    """ A complex object """
    _regex = r'((\d+)?\.(?(2)\d*|\d+)[iIjJ])'
    _pyobj = complex