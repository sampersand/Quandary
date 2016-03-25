from functools import reduce
class constants():
    class _set(set):
        def __contains__(self, val) -> bool:
            return bool(val and super().__contains__(val))
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
        self.comment = constants._set({'#'})
        self.escape = constants._set({'\\'})
        self.linebreak = constants._set({';', '\n'})
        self.quotes = constants._set({"'", '"'})
        self.whitespace = constants._set({' ', '\n', '\t'})
        self.operators = {
            '+':None, '-':None, '*':None, '/':None, '%':None, '^':None, 
            'bxor':None, '&':None, '|':None, '>>':None, '<<':None, '~':None,
            '=':None, '<>':None, 
            '<':None, '<=':None, '>':None, '>=':None, 
            'and':None, 'or':None, 'nand':None, 'nor':None,
            '->':None, '<-':None,
        }
        self.delims = {':': None, ',':None, '.': None}
        self.operators.update(self.delims)
        self.parens = constants._set({'{', '}', '[', ']', '(', ')'})
    @property
    def punctuation(self) -> _set:
        return reduce(lambda a,b: a | b, (getattr(self, k) if isinstance(getattr(self, k), constants._set) else\
                        constants._set(getattr(self, k).keys()) for k in vars(self)))

    def getoperpriority(self, oper:str) -> int:
        """ larger it is, the more important it is"""
        return int(dict((constants._splitstr(e) for e in (
            'or0', 'nor0', 'and1', 'nand1', 'not2',
            '=3', '<>3', '<4', '>4', '<=4', '>=4',
            '|5', '^6', '&7', '>>8', '<<8', 
            '+9', '-9', '*a', '/a', '%a', '**b', '~c'
        )))[oper], 16) 