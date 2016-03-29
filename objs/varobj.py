from objs import nullobj
class varobj(nullobj):
    """ The object that represents a missing object, rather than just a null object. """
    _regex = None
    def isreference(self: 'obj') -> bool:
        """ True if this class is a reference to another object. Currently, only varobj returns true."""
        return True