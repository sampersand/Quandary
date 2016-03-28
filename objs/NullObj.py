class nullobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('obj')):
    """ A null object - usually gotten by the keywords 'nil', 'null', and 'None'. """