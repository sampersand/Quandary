class operobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('funcobj')):
    """ An operator. """
    def evalobj(*args, **kwargs):
        if __debug__:
            assert 'oper' in kwargs, "Cannot evalobj on an operobj with no operator!"
        print(args)