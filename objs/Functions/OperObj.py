import copy
class operobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('funcobj')):
    """ An operator. """
    def evalobj(knowns, *args, **kwargs):
        if __debug__:
            assert 'oper' in kwargs, "Cannot evalobj on an operobj with no operator!"
            assert len(args) == 2, "Currently, only accepting binary operators."
        oper = kwargs['oper']
        if __debug__: #this should be removed later when copy works
            from node import node
            ret = node(args[0].consts, **args[0]._attrs.copy())
        # ret = copy.copy(args[0])
        if oper == '+': ret.data = int(ret.data) + int(args[1].data)
        if oper == '-': ret.data = int(ret.data) - int(args[1].data)
        if oper == '/': ret.data = int(ret.data) / int(args[1].data)
        if oper == '*': ret.data = int(ret.data) * int(args[1].data)
        if oper == '%': ret.data = int(ret.data) % int(args[1].data)
        return ret
