class obj(dict):

    """ The overarching class for every object. """
    NAMES = ('name', '')
    NAMES = {k: '$qq_' + k for k in NAMES}

    def __init__(self, data):
        super().__init__(data)

    def __getattr__(self, attr):
        if attr 