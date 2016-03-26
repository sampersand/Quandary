from Constants import constants
class node():
    def __init__(self, const: constants, **kwargs: dict) -> None:
        super().__setattr__('const', const)
        super().__setattr__('_attrs', {})
        for key in kwargs:
            self._attrs[key] = kwargs[key]

    def __getattr__(self, attr: str):
        """ gets 'self._attrs[attr]' """
        return self._attrs[attr]
    def __setattr__(self, attr: str, val) -> None:
        """ sets 'self._attrs[attr]' to val"""
        self._attrs[attr] = val
    def __delattr__(self, attr: str) -> None:
        """ deletes 'attr' from self._attrs """
        del self._attrs[attr]

    @property
    def attrs(self) -> dict:
        return {k:self._attrs[k] for k in self._attrs if k != 'const'}
    
    @staticmethod
    def fromiter(const: constants, iterable):
        punc = const.punctuation
        if __debug__:
            assert hasattr(iterable, '__iter__'), 'cannot run fromiter on a non-iterable...'
        def iesc(_iterable):
            """ yields each individual character, or two if the first one is a '\\'. """
            for c in _iterable:
                yield c + ('' if c not in const.escape else next(_iterable))

        def itoken(_iterable):
            """ yields each individual token. """
            last = ''
            for c in _iterable:
                if c in const.quotes:
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

        def icmnt(_iterable):
            """ skips over comments. """
            i = iter(_iterable)
            for t in i:
                if t in const.comment:
                    try:
                        t = next(i)
                        while t not in const.endcomment:
                            t = next(i)
                        t = next(i) #else you get stuck with the '#'
                    except StopIteration:
                        raise SyntaxError('Error: Unclosed comment!')
                yield t

        def iws(_iterable):
            """ yields each token if it isn't only a whitespace token. """
            return (t for t in _iterable if t not in const.whitespace)

        def ieof(_iterable):
            """ yields each t before and '@eof', if it exists. """
            for t in _iterable:
                if t == '@eof': break
                yield t
        def iopers(_iterable):
            """ yields them in order of operations. """
            nstack, ostack = [], []
            for token in _iterable:
                if token in const.parens:
                    if const.parens[token]: #aka if it's )}]
                        pass
                if token not in const.operators:
                    nstack.append(token)
            return nstack
        iterable = iopers(ieof(iws(icmnt(itoken(iesc(iter(iterable)))))))
        args = list(iterable)
        return node(const, args = args)

    def __repr__(self) -> str:
        return repr(self.attrs)

with open('qfiles/testcode.qq') as f:
    n = node.fromiter(constants(), f.read())
    print(n)




