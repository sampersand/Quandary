from objs import operobj
from functools import reduce
class constants():
    class _set(set):
        def __contains__(self, val) -> bool:
            return bool(val and super().__contains__(val))
        def __or__(self, val: set) -> set:
            val = super().__or__(val)
            return val if val == NotImplemented else constants._set(val)
    class _splitstr(str):
        def __iter__(self):
            yield self[:-1]
            yield self[-1]
            # yield self[:self.index('.') - 1]
            # yield self[self.index('.'):]
    # class _dict(dict):
    #     def __contains__(self, val):
    #         for key in self:
    #             if val == self[key]:
    #                 return True
    #             if isinstance(self[key], _dict) and val in self[key]:
    #                 return True
    #         return False

    def __init__(self) -> None:
        _set = self._set
        self.comment = _set({'#'})
        self.escape = _set({'\\'})
        self.linebreak = _set({';', '\n'}) #ends a line codewise
        self.endcomment = _set({'\n', '\r'}) | self.comment #ends a line for comments
        self.quotes = _set({"'", '"'})
        self.whitespace = _set({' ', '\n', '\t', '\r'})
        self.operators = {
            '+': operobj('+'), '-': operobj('-'), '*': operobj('*'),
            '/': operobj('/'), '%': operobj('%'), '^': operobj('^'), 
            'bxor': operobj('bxor'), '&': operobj('&'), '|': operobj('|'), '>>': operobj('>>'), 
            '<<': operobj('<<'), '~': operobj('~'),
            '=': operobj('='), '<>': operobj('<>'), 
            '<': operobj('<'), '<=': operobj('<='), '>': operobj('>'), '>=': operobj('>='), 
            'and': operobj('and'), 'or': operobj('or'), 'nand': operobj('nand'), 'nor': operobj('nor'),
            '->': operobj('->'), '<-': operobj('<-'),
        }
        self.delims = {':':  operobj(':'), ',': operobj(','), '.':  operobj('.'), ';':  operobj(';')}
        self.operators.update(self.delims)
        self.parens = dict((x[0], int(x[1])) for x in ('(0', '[0:', '{0', ')1', ']1:', '}0'))
        # self.parens = {'{':0, '[':0, '(':0, ')':1 ']':1, '}':1,}
    @staticmethod
    def _parentype(p):
        return p in '])}'
    @property
    def punctuation(self) -> _set:
        return reduce(lambda a,b: a | b, (getattr(self, k) if isinstance(getattr(self, k), constants._set) else\
                        constants._set(getattr(self, k).keys()) for k in vars(self)))

    def _operpriority(self, oper:str) -> int:
        """ smaller it is, the more important it is"""
        return {
            ':':0, '.':0, #1 and 2 are used for unary
            '**':3, '*':4, '/':4, '%':4, '+':5, '-':5,
            '<<':6, '>>':6, '&':7, '^':8, '|':9,
            '<':10, '>':10, '<=':10, '>=':10, '=':10, '<>':10,
            '&&':11, '||':12,
            '<-':13, '->':13,
            ',': 14, ';':16
        }[oper]
        # return int(dict((constants._splitstr(e) for e in (
        #     ':0',
        #     'orc', 'norc', 'andb', 'nandb', 'notd',
        #     '=a', '<>a', '<a', '>a', '<=a', '>=a',
        #     '|9', '^8', '&7', '>>6', '<<6', 
        #     '+5', '-5', '*4', '/4', '%4', '**3', '~c',
        #     ':d', '.d', ',e', ';f'
        #     '->'
        # )))[oper], 16) 










