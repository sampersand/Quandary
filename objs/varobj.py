class varobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('nullobj')):
    """ The object that represents a missing object, rather than just a null object. """