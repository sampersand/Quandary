class boolobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('intobj')):
    """ A boolean - either True or False. """
    _regex = r'\b([Tt]rue|[Ff]alse)\b'
    _pyobj = bool