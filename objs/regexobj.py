import re
from objs import obj
class regexobj(obj):
    """ The overarching class for all objects with regexes. """
    _regex = None

    @classmethod
    def _regex_fixdatastr(self: type, data: str) -> str:
        return data

    @classmethod
    def fromstr(self: type, data: str, consts: 'constants') -> 'obj':
        if __debug__:
            assert hasattr(self, '_regex'), "non-regex object '{}' shouldn't extend regexobj!".format(self)
        if self._regex and re.fullmatch(self._regex, data):
            return self._regex_fixdatastr(data), self()
        return None