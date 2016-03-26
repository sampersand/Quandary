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
        def iterescaped(_iterable):
            for c in _iterable:
                yield c + ('' if c not in const.escape else next(_iterable))
        def iterconsts(_iterable):
            last = ''
            for c in _iterable:
                if c in const.quotes:
                    toyield = [c, next(_iterable)]
                    while(toyield[-1] != toyield[0]):
                        toyield.append(next(_iterable))
                    yield ''.join(toyield)
                    continue
                print(c, last, sep = '::')
                if ((last in punc) and (last + c not in punc)) or (c in punc and last not in punc):
                    if last:
                        yield last
                    last = ''
                last += c
            if last:
                yield last
        def removewspace(_iterable):
            return (x for x in _iterable if x not in const.whitespace)
        def removeAtEOF(_iterable):
            for x in _iterable:
                if x == '@eof': break
                yield x

        iterable = removeAtEOF(removewspace(iterconsts(iterescaped(iter(iterable)))))
        args = list(iterable)
        return node(const, args = args)

    def __repr__(self) -> str:
        return repr(self.attrs)

with open('qfiles/testcode.qq') as f:
    n = node.fromiter(constants(), f.read())
    print(n)




