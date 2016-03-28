class floatobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('numobj')):
    """ A floating point number. """
    _regex = r'\b(\d+)?\.(?(1)\d*|\d+)[fF]?\b'
    _pyobj = float