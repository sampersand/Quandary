class boolobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('intobj')):
    """ A boolean - either True or False. """
    _regex = r'([Tt]rue|[Ff]alse)'