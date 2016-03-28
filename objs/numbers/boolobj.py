from objs import intobj
class boolobj(intobj):
    """ A boolean - either True or False. """
    _regex = r'\b([Tt]rue|[Ff]alse)\b'
    _pyobj = bool