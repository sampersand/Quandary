class intobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('numobj')):
    """ A whole number. """
    _regex = r'([1-9][0-9]*|0)[wW]?' #w for whole
    _pyobj = int