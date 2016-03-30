from objs import numobj, pyobj, regexobj
class complexobj(regexobj, pyobj, numobj):
    """ A complex object """
    _regex = r'\b((\d+)?\.(?(2)\d*|\d+)[iIjJ])\b'
    _pyobj = complex
    _pyobj_default_rank = 3

    # @classmethod
    # def fromstr(self: type, data: str, consts: 'constants') -> 'obj': #assumes the length of data is >= 1
    #     return data[-1] in 'iI' and data[:-1] + 'j' or data