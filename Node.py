from typing import Callable, Union, Any
from types import GeneratorType as gentype
import objs
class node():
    def __init__(self: 'node', consts: 'constants', **kwargs: dict) -> None:
        super().__setattr__('consts', consts)
        super().__setattr__('_attrs', {})
        if 'genobj' in kwargs and 'data' in kwargs:
            if kwargs['genobj']:
                if __debug__ and 'obj' in kwargs:
                    raise KeyError("Error! both 'genobj' and 'obj' were passed!") #might be a warning in the future
                kwargs['obj'] = self.getobj(kwargs['data'])
            del kwargs['genobj']

        for key in kwargs:
            self._attrs[key] = kwargs[key]

        if 'obj' not in self:
            self['obj'] = getobj(None)

    def __getattr__(self: 'node', attr: str) -> Any:
        """ gets 'self._attrs[attr]' """
        return self._attrs[attr]

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
        return self.data



    def getobj(self: 'node', data: Union[str, None]) -> objs.obj:
        if data == None:
            return objs.noneobj()
        if data in self.consts.operators:
            return self.consts.operators[data]
        return objs.noneobj()

    def evaluate(self: 'node', gen: gentype, knowns: 'knowndict') -> float:
        tstack, ostack = [], []
        def evalt():
            tstack.append(ostack.pop().obj.evaluate(tstack.pop(), tstack.pop()))
        for t in gen:
            if t.data in self.consts.parens:
                if not self.consts.parens[t.data]:
                    tstack.append(next(gen).evaluate(knowns))
                elif self.consts.parens[t.data]:
                    while ostack:
                        evalt()
                    return tstack.pop()
            elif isinstance(t.obj, objs.operobj):
                while ostack and self.consts._operpriority(ostack[-1].data) >= self.consts._operpriority(t.data):
                    evalt()
                ostack.append(t)
            else:
                tstack.append(t)
        while ostack:
            evalt()
        print(list(str(x) for x in tstack),list(str(x) for x in ostack), sep = '\n')






























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

    return iopers(ieof(iws(icmnt(itoken(iesc(iter(iterable)))))))

