from typing import Callable
from objs import obj
class pyobj(obj):
    """ The superclass for all Quandary objects that are linked to python objects (_pyobj) """

    _pyobj = None
    _pyobj_default_rank = 0

    def _pyobj_valof(self: 'pyobj', node: 'node', v: 'flatdict') -> object:
        """
        Get the python equivalent of an object.
        By default, it returns 'self._pyobj(node.data)'
        """
        return self._pyobj(node.data)

    def _pyobj_rank(self: 'pyobj', v: 'flatdict') -> (int, float):
        return self._pyobj_default_rank

    def _pyobj_compare(self: 'pyobj', other: 'pyobj', v: 'flatdict') -> 'pyobj':
        """
        Returns which object the datas should be converted to.
        By default, the one with the higher rank is returned (in a tie, self is returned).
        """
        return self if self._pyobj_rank(v) >= other._pyobj_rank(v) else other

    def _pyobj_getattr(self: 'pyobj', base: type, attr: 'str', v: 'flatdict') -> Callable:
        """ get the attribution from a python object with the string attr.
        currently, attr is expected to be '_oper_FUNCTION'. this returns base's function '__FUNCTION__'.
        """
        return getattr(base, '__' + attr[6:] + '__')

    def __getattr__(self: 'pyobj', attr: str) -> Callable:
        """ Get an attribute - like __add__ and __mod__ - that doesn't exist.
            Provides a default implementation that otherwise wouldn't exist"""
        def ret(node1: 'node', node2: 'node', v: 'flatdict') -> 'node':
            if __debug__:
                assert hasattr(node1, 'obj'), 'every object should!'
                assert hasattr(node1.obj, '_pyobj_valof'),\
                    "The Node's object should have a python object associated with it!"
            objtopass = node1.obj._pyobj_compare(node2.obj, v)
            return node1.new(\
                        data = str(self._pyobj_getattr(objtopass._pyobj_valof(node1, v), attr, v)\
                                (objtopass._pyobj_valof(node2, v))),
                        obj = objtopass)
        return attr[:6] == '_oper_' and ret or super().__getattr__(attr)






















