from objs import intobj, pyobj
class boolobj(intobj, pyobj):
    """ A boolean - either True or False. """
    _regex = r'\b([Tt]rue|[Ff]alse)\b'
    _pyobj = bool