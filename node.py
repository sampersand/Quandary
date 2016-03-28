from typing import Callable, Any
from types import GeneratorType as gentype
from copy import deepcopy
import objs
class node():
    def __init__(self: 'node', consts: 'constants', **kwargs: dict) -> None:
        super().__setattr__('consts', consts)
        super().__setattr__('_attrs', {})
        if 'genobj' in kwargs and 'data' in kwargs:
            if kwargs['genobj']:
                if __debug__ and 'obj' in kwargs:
                    raise KeyError("Error! both 'genobj' and 'obj' were passed!") #might be a warning in the future
                kwargs['obj'] = objs.getobj(self, kwargs['data'])
            del kwargs['genobj']

        if 'obj' not in kwargs:
            kwargs['obj'] = objs.getobj(self, None)

        for key in kwargs:
            self._attrs[key] = kwargs[key]


    def __getattr__(self: 'node', attr: str) -> Any:
        """ gets 'self._attrs[attr]' """
        return self._attrs[attr] if attr in self else None

    def __setattr__(self: 'node', attr: str, val: Any) -> None:
        """ sets 'self._attrs[attr]' to val"""
        self._attrs[attr] = val

    def __delattr__(self: 'node', attr: str) -> None:
        """ deletes 'attr' from self._attrs """
        del self._attrs[attr]

    def __contains__(self: 'node', attr: str) -> bool:
        return attr in self._attrs

    @property
    def attrs(self: 'node') -> dict:
        return self._attrs

    def __repr__(self: 'node') -> str:
        return repr(self.attrs)
    
    def __str__(self: 'node') -> str:
        """ """ #todo this
        return str(self.data)

    def __deepcopy__(self, memo):
        return node(self.consts, deepcopy(self._attrs, memo))

    def evalnode(self: 'node', gen: gentype, knowns: 'knowndict') -> 'node':
        ts, os = [], [] #token / oper stack
        def reduce_os():
            o = os.pop()
            if __debug__:
                assert issubclass(o.obj, objs.operobj), "Expected an operobj, not a '{}'".format(o.obj)
            ts.append(o.obj.evalobj(knowns, gen, ts.pop(-2), ts.pop(), oper = o.data))
            #-2 is because they need to be flipped
        for t in gen:
            if t.data in self.consts.parens:
                if not self.consts.parens[t.data]:
                    ts.append(next(gen).evalnode(gen, knowns))
                else:
                    while os:
                        reduce_os()
                    return ts.pop()
            elif issubclass(t.obj, objs.operobj):
                while os and self.consts._evalorder(os[-1].data) <= self.consts._evalorder(t.data):
                    reduce_os()
                os.append(t)
            else:
                ts.append(t)
        while os:
            reduce_os()
        return ts.pop()

def getiter(consts: 'constants', iterable: Callable) -> node:
    """ get an iterable, where each successive element is a node."""
    punc = consts.punctuation
    if __debug__:
        assert hasattr(iterable, '__iter__'), 'cannot run getiter on a non-iterable...'
    def iesc(_iterable: gentype):
        """ yields each individual character, or two if the first one is a '\\'. """
        for c in _iterable:
            yield c + ('' if c not in consts.escape else next(_iterable))

    def itoken(_iterable: gentype):
        """ yields each individual token. """
        last = ''
        for c in _iterable:
            if c in consts.quotes:
                toyield = [c]
                try:
                    toyield.append(next(_iterable))
                    while(toyield[-1] != toyield[0]):
                        toyield.append(next(_iterable))
                    yield ''.join(toyield)
                    continue
                except StopIteration:
                    raise SyntaxError('Error: Unclosed string literal!')
            if ((last in punc) and (last + c not in punc)) or (c in punc and last not in punc):
                if last: yield last
                last = ''
            last += c
        yield last

    def icmnt(_iterable: gentype):
        """ skips over comments. """
        i = iter(_iterable)
        for t in i:
            if t in consts.comment:
                try:
                    t = next(i)
                    while t not in consts.endcomment:
                        t = next(i)
                    t = next(i) #else you get stuck with the '#'
                except StopIteration:
                    raise SyntaxError('Error: Unclosed comment!')
            yield t

    def iws(_iterable: gentype):
        """ yields each token if it isn't only a whitespace token. """
        return (t for t in _iterable if t not in consts.whitespace)

    def ieof(_iterable: gentype):
        """ yields each t before and '@eof', if it exists. """
        for t in _iterable:
            if t == '@eof': break
            yield t
    def iopers(_iterable: gentype):
        return (node(consts, data = x, genobj = True) for x in _iterable)

    yield node(consts)
    for t in iopers(ieof(iws(icmnt(itoken(iesc(iter(iterable))))))):
        yield t