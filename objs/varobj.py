from objs import nullobj, pyobj
class varobj(nullobj, pyobj):
    """ The object that represents a missing object, rather than just a null object. """
    _regex = None