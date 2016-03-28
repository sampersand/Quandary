from node import node
class pyobj(__import__((__package__ + ' ')[:__package__.find('.')])._import('obj')):
    """ The superclass for all Quandary objects that are linked to python objects (_pyobj) """
    def __getattr__(self, attr: str):
        def ret(node1: 'node', node2: 'node') -> 'node':
            if __debug__:
                assert hasattr(node1, 'obj'), 'every object should!'
                assert hasattr(node1.obj, '_pyobj'), "The Node's object should have a python object associated with it!"
            pyobj = node1.obj._pyobj
            return node(node1.consts, data = getattr(pyobj(node1.data), attr)(pyobj(node2.data)), obj = node1.obj)
        return ret
    # def __add__(self, a, b):
        # ret = 
