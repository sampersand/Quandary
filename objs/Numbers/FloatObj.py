class floatobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('numobj'),
               __import__((__package__ + ' ')[:__package__.find('.')])._import('pyobj')):
    """ A floating point number. """
    _regex = r'(\d+)?\.(?(1)\d*|\d+)[fF]?'
    _pyobj = float