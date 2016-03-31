from objs import obj, regexobj
class nullobj(regexobj, obj):
    """ A null object - usually gotten by the keywords 'nil', 'null', and 'None'. """
    _regex = r'[nN](?:one|il|ull)'
