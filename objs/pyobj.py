from typing import Callable
from objs import obj
class pyobj(obj):
    """ The superclass for all Quandary objects that are linked to python objects (_pyobj) """

    _pyobj = None
    _pyobj_rank = 0

    def _pyobj_valof(self: 'intobj', node: 'node') -> object:
        """
        Get the python equivalent of an object.
        By default, it returns 'self._pyobj(node.data)'
        """
        return self._pyobj(node.data)

    def _pyobj_compare(self: 'obj', other: 'obj') -> 'obj':
        """
        Returns which object the datas should be converted to.
        By default, the one with the higher rank is returned (in a tie, self is returned).
        """
        return self if self._pyobj_rank >= other._pyobj_rank else other

    def _pyobj_getattr(self: 'obj', base: type, attr: 'str') -> Callable:
        """ get the attribution from a python object with the string attr.
        currently, attr is expected to be '_oper_FUNCTION'. this returns base's function '__FUNCTION__'.
        """
        return getattr(base, '__' + attr[6:] + '__')

    def __getattr__(self: 'obj', attr: str) -> Callable:
        """ Get an attribute - like __add__ and __mod__ - that doesn't exist.
            Provides a default implementation that otherwise wouldn't exist"""
        def ret(node1: 'node', node2: 'node', knowns: 'knownsdict') -> 'node':
            if __debug__:
                assert hasattr(node1, 'obj'), 'every object should!'
                assert hasattr(node1.obj, '_pyobj_valof'), "The Node's object should have a python object associated with it!"
            objtopass = node1.obj._pyobj_compare(node2.obj)
            return node1.new(\
                        data = self._pyobj_getattr(objtopass._pyobj_valof(node1), attr)\
                                (objtopass._pyobj_valof(node2)),
                        obj = objtopass)
        return attr[:6] == '_oper_' and ret or super().__getattr__(attr)

