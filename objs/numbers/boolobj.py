from objs import intobj, pyobj
class boolobj(intobj, pyobj):
    """ A boolean - either True or False. """
    BASES = {'default': 2}
    def __init__(self):
        super().__init__(base = 2)
    _regex = r'\b([Tt]rue|[Ff]alse)\b'
    _pyobj = bool
    _pyobj_rank = 0

    def _pyobj_valof(self: 'intobj', node: 'node') -> bool:
        quit('todo! this')
        return int(bool(node.data))

    # @classmethod
    # def fromstr(self: type, data: str, consts: 'constants') -> 'obj':
    #     return data[0] in 'Tt' and True or False