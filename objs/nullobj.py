from objs import obj
class nullobj(obj):
    """ A null object - usually gotten by the keywords 'nil', 'null', and 'None'. """
    _regex = r'[nN](?:one|il|ull)'
