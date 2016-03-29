from objs import numobj, pyobj
class complexobj(numobj, pyobj):
    """ A complex object """
    _regex = r'\b((\d+)?\.(?(2)\d*|\d+)[iIjJ])\b'
    _pyobj = complex
    _pyobj_rank = 3

    @classmethod
    def fromstr(self: type, data: 'str', consts: 'constants') -> 'obj': #assumes the length of data is >= 1
        return data[-1] in 'iI' and data[:-1] + 'j' or data