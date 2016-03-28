class obj():
    """ The overarching class for all objects. """
    def __repr__(self):
        return type(self).__qualname__+'()'