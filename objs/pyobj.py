from objs import obj
class pyobj(obj):
    """ The superclass for all Quandary objects that are linked to python objects (_pyobj) """
    _pyobj = None
    _pyobj_rank = 0

    def pyvalof(self:'intobj', node: 'node'):
        return self._pyobj(node.data)

    def _compare_and_get_obj(self, other):
        return self if self._pyobj_rank >= other._pyobj_rank else other

    def __getattr__(self, attr: str):
        """ Get an attribute - like __add__ and __mod__ - that doesn't exist.
            Provides a default implementation that otherwise wouldn't exist"""
        def ret(node1: 'node', node2: 'node', knowns: 'knownsdict') -> 'node':
            if __debug__:
                assert hasattr(node1, 'obj'), 'every object should!'
                assert hasattr(node1.obj, 'pyvalof'), "The Node's object should have a python object associated with it!"
            objtopass = node1.obj._compare_and_get_obj(node2.obj)
            return node1.new(\
                        data = getattr(objtopass.pyvalof(node1), attr)(objtopass.pyvalof(node2)),
                        obj = objtopass)
        return ret

