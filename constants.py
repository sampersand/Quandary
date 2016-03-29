class _set(set):
    def __contains__(self, val) -> bool:
        return bool(val and super().__contains__(val))
    def __or__(self, val: set) -> set:
        #TODO: make this IOR
        val = super().__or__(val)
        return val if val == NotImplemented else _set(val)
from objs import operobj
from functools import reduce
from knowndict import flatdict
class constants():
    class _splitstr(str):
        def __iter__(self):
            yield self[:-1]
            yield self[-1]
            # yield self[:self.index('.') - 1]
            # yield self[self.index('.'):]
    def __init__(self) -> None:
        self.punc = flatdict({
            'comment': _set({'#'}),
            'escape': _set({'\\'}),
            'linebreak': _set({';', '\n'}), #ends a line codewise
            'endcomment': _set({'\n', '\r'}), #ends a line for comments
            'quotes': _set({"'", '"'}),
            'whitespace': _set({' ', '\n', '\t', '\r'}),
            'parens': flatdict((x[0], int(x[1])) for x in ('(0', '[0:', '{0', ')1', ']1:', '}0'))
        })
        self.punc['endcomment'] = self.punc['endcomment'] | self.punc['comment'] #dont wanna update the magic method
        self.opers = flatdict({
            'assignment': flatdict({
                '->': flatdict({'obj':operobj, 'rank': 13, 'reqs': ((2,), (0,))}),
                '<-': flatdict({'obj':operobj, 'rank': 13, 'reqs': ((2,), (0,))}),
            }),
            'simple_binary': flatdict({
                'math': flatdict({
                    '**': flatdict({'obj':operobj, 'rank':  3, 'reqs': ((2,), (0,)), 'loper': '__pow__', 'roper': '__rpow__'}),
                    '*' : flatdict({'obj':operobj, 'rank':  4, 'reqs': ((2,), (0,)), 'loper': '__mul__', 'roper': '__rmul__'}),
                    '/' : flatdict({'obj':operobj, 'rank':  4, 'reqs': ((2,), (0,)), 'loper': '__div__', 'roper': '__rdiv__'}),
                    '%' : flatdict({'obj':operobj, 'rank':  4, 'reqs': ((2,), (0,)), 'loper': '__mod__', 'roper': '__rmod__'}),
                    '+' : flatdict({'obj':operobj, 'rank':  5, 'reqs': ((2,), (0,)), 'loper': '__add__', 'roper': '__radd__'}),
                    '-' : flatdict({'obj':operobj, 'rank':  5, 'reqs': ((2,), (0,)), 'loper': '__sub__', 'roper': '__rsub__'}),
                }),

                'bitwise': flatdict({
                    '>>': flatdict({'obj':operobj, 'rank':  6, 'reqs': ((2,), (0,)), 'loper': '__rshift__', 'roper': '__rrshift__'}),
                    '<<': flatdict({'obj':operobj, 'rank':  6, 'reqs': ((2,), (0,)), 'loper': '__lshift__', 'roper': '__rlshift__'}),
                    '&' : flatdict({'obj':operobj, 'rank':  7, 'reqs': ((2,), (0,)), 'loper': '__and__', 'roper': '__rand__'}),
                    '^' : flatdict({'obj':operobj, 'rank':  8, 'reqs': ((2,), (0,)), 'loper': '__xor__', 'roper': '__rxor__'}),
                    '|' : flatdict({'obj':operobj, 'rank':  9, 'reqs': ((2,), (0,)), 'loper': '__or__', 'roper': '__ror__'}),
                }),
            }),
            'bitwise': flatdict({
                '~' : flatdict({'obj':operobj, 'rank':None,'reqs': (1, 0)}),
            }),
            'logic': flatdict({
                '=' : flatdict({'obj':operobj, 'rank': 10, 'reqs': ((2,), (0,))}),
                '<>': flatdict({'obj':operobj, 'rank': 10, 'reqs': ((2,), (0,))}),
                '<' : flatdict({'obj':operobj, 'rank': 10, 'reqs': ((2,), (0,))}),
                '<=': flatdict({'obj':operobj, 'rank': 10, 'reqs': ((2,), (0,))}),
                '>' : flatdict({'obj':operobj, 'rank': 10, 'reqs': ((2,), (0,))}),
                '>=': flatdict({'obj':operobj, 'rank': 10, 'reqs': ((2,), (0,))}),
                '&&': flatdict({'obj':operobj, 'rank': 11, 'reqs': ((2,), (0,))}),
                '||': flatdict({'obj':operobj, 'rank': 12, 'reqs': ((2,), (0,))}),
            }),

            'delims': flatdict({
                ':' : flatdict({'obj':operobj, 'rank':  0, 'reqs': ((2,), (0,))}),
                '.' : flatdict({'obj':operobj, 'rank':  0, 'reqs': ((2, 1), (0,))}),
                ',' : flatdict({'obj':operobj, 'rank': 14, 'reqs': ((2,), (0,))}),
                ';' : flatdict({'obj':operobj, 'rank': 15, 'reqs': ((1,), (0,))}),
            }),
        })
        # self.parens = {'{':0, '[':0, '(':0, ')':1 ']':1, '}':1,}
    @staticmethod
    def _parentype(p: str) -> bool:
        return p in '])}'
        # return reduce(lambda a,b: a | b, (getattr(self, k) if isinstance(getattr(self, k), _set) else\
        #                 _set(getattr(self, k).flat) for k in vars(self)))

    @property
    def _loperfuncs(self) -> dict:
        return {'+':'__add__', '-':'__sub__', '*':'__mul__', '/':'__div__'}
    @property
    def _roperfuncs(self) -> dict:
        return {k:'__i'+v[2:] for k,v in self._loperfuncs.items()}

    @property
    def keywords(self):
        return flatdict({'opers':self.opers, 'punc': self.punc})

    







