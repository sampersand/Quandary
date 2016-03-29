from obj import obj
class regexobj(obj):
    """ The overarching class for all objects with regexes. """

    @classmethod
    def fromstr(self: 'obj', data: 'str'):
        if __debug__:
            assert hasattr(self, '_regex'), "non-regex object '{}' shouldn't extend regexobj!".format(self)
        