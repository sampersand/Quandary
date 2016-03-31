from typing import Callable, Any
from types import GeneratorType as gentype
from copy import deepcopy
from knowndict import flatdict
import objs
from utils import thisfunc, checkparams
class node():
    def __init__(self: 'node', consts: 'constants', **kwargs: dict) -> None:
        if __debug__:
            print(globals().keys(), globals()['node'])
            assert checkparams(thisfunc(globals))
        super().__setattr__('consts', consts)
        super().__setattr__('_attrs', {})
        if 'genobj' in kwargs and 'data' in kwargs:
            if kwargs['genobj']:
                if __debug__ and 'obj' in kwargs:
                    raise KeyError("Error! both 'genobj' and 'obj' were passed!") #might be a warning in the future
                kwargs['data'], kwargs['obj'] = objs.getobj(self.consts, kwargs['data'])
            del kwargs['genobj']

        if 'obj' not in kwargs:
            kwargs['obj'] = objs.getobj(self.consts, None)

        for key in kwargs:
            self._attrs[key] = kwargs[key]


    def __getattr__(self: 'node', attr: str) -> Any:
        """ gets 'self._attrs[attr]' """
        return self._attrs[attr] #doesn't check if it exists anymore
        # return self._attrs[attr] if attr in self else None

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
        return node(self.consts, kwargs = deepcopy(self._attrs, memo))

    @staticmethod
    def _reduce_os(v: flatdict) -> None:
        if __debug__:
            assert isinstance(v.os[-1].obj, objs.operobj),\
                "Expected an operobj, not a '{}'".format(v.os[-1].obj)
        v.os[-1].obj.evaloper(v, v.os.pop().data)

    @staticmethod
    def evalnode(gen: gentype, knowns: 'knowndict') -> 'node':
        v = flatdict(knowns = knowns, gen = gen, ts = [], os = [], consts = knowns.consts)
        #ONLY SETS TOKENS, NOT OPERS, TO knowns.c.last
        for t in v.gen:
            if t.data in v.consts.punc.parens:
                if not v.consts.punc.parens[t.data]:
                    v.ts.append(node.evalnode(gen, v.knowns))
                else:
                    while v.os:
                        node._reduce_os(v)
                    return v.ts.pop()
            elif isinstance(t.obj, objs.operobj):
                while v.os and v.consts.opers[v.os[-1].data].rank <=\
                                      v.consts.opers[t.data].rank:
                    node._reduce_os(v)
                v.os.append(t)
            else:
                v.ts.append(t)
        while v.os:
            node._reduce_os(v)
        return v

    def new(self: 'node', consts = None, **kwargs):
        return node(consts or self.consts, **kwargs)

def getiter(consts: 'constants', iterable: Callable) -> node:
    """ get an iterable, where each successive element is a node."""
    kws = consts.keywords.copy()
    kws['ws'] = consts.punc.whitespace
    if __debug__:
        assert hasattr(iterable, '__iter__'), 'cannot run getiter on a non-iterable...'
    def iesc(_iterable: gentype):
        """ yields each individual character, or two if the first one is a '\\'. """
        for c in _iterable:
            yield c + ('' if c not in consts.punc.escape else next(_iterable))

    def itoken(_iterable: gentype):
        """ yields each individual token. """
        last = ''
        for c in _iterable:
            if c in consts.punc.quotes:
                toyield = [c]
                try:
                    toyield.append(next(_iterable))
                    while(toyield[-1] != toyield[0]):
                        toyield.append(next(_iterable))
                    yield ''.join(toyield)
                    continue
                except StopIteration:
                    raise SyntaxError('Error: Unclosed string literal!')
            elif ((last in kws) and (last + c not in kws)) or\
                    (c in kws and last not in kws):
                if last: yield last
                last = ''
            last += c
        yield last

    def icmnt(_iterable: gentype):
        """ skips over comments. """
        i = iter(_iterable)
        for t in i:
            if t in consts.punc.comment:
                try:
                    t = next(i)
                    while t not in consts.punc.endcomment:
                        t = next(i)
                    t = next(i) #else you get stuck with the '#'
                except StopIteration:
                    raise SyntaxError('Error: Unclosed comment!')
            yield t

    def iws(_iterable: gentype):
        """ yields each token if it isn't only a whitespace token. """
        return (t for t in _iterable if t not in consts.punc.whitespace)

    def ieof(_iterable: gentype):
        """ yields each t before and '@eof', if it exists. """
        for t in _iterable:
            if t == '@eof': break
            yield t
    def iopers(_iterable: gentype):
        return (node(consts, data = x, genobj = True) for x in _iterable)
    return iopers(ieof(iws(icmnt(itoken(iesc(iter(iterable)))))))