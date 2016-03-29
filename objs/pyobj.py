from node import node
from objs import obj
class pyobj(obj):
    _pyobj = None
    _pyobj_rank = 0
    """ The superclass for all Quandary objects that are linked to python objects (_pyobj) """
    def __getattr__(self, attr: str):
        def ret(node1: 'node', node2: 'node') -> 'node':
            if __debug__:
                assert hasattr(node1, 'obj'), 'every object should!'
                assert hasattr(node1.obj, '_pyobj'), "The Node's object should have a python object associated with it!"
            nodeobj = node1.obj if node1.obj._pyobj_rank >= node2.obj._pyobj_rank else node2.obj
            return node(node1.consts, data = getattr(nodeobj._pyobj(node1.data), attr)(nodeobj._pyobj(node2.data)),
                        obj = nodeobj)
        return ret
    # def __add__(self, a, b):
        # ret = 
