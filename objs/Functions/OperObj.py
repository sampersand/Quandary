class operobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('funcobj')):
    """ An operator. """
    def evalobj(*args, **kwargs):
        if __debug__:
            assert 'oper' in kwargs, "Cannot evalobj on an operobj with no operator!"
            assert len(args) == 2, "Currently, only accepting binary operators."
        oper = kwargs['oper']
        import copy
        ret = args[0]
        ret = copy.copy(args[0])
        if oper == '+':
            ret.data += args[1].data
        return ret
