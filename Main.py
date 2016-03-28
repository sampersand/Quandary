from Constants import constants
from Node import getiter
from KnownDict import knowndict

if __name__ == '__main__':
    with open('qfiles/testcode.qq') as f:
        gen = getiter(constants(), f.read())
    n = next(gen)
    known = knowndict(n.consts)
    print('\n----')
    n.evalnode(gen, known)
    print('----\n')
    if __debug__ and '$dnd' not in known:
        print(known, end = '\n--\n')
        print(repr(known))
# def evalinp(inp):
#     ns, os = [], []
#     opers = {'+':('__radd__',0),
#              '-':('__rsub__',0),
#              '*':('__rmul__',1),
#              '/':('__rdiv__',1),
#              '%':('__rmod__',1),
#              '^':('__rpow__',2)}
#     parens = {'(': 0, ')': 1}
#     inpiter = iter(inp)
#     for c in inpiter:
#         if c == ' ':continue
#         if c in parens:
#             if not parens[c]:
#                 ns.append(evalinp(inpiter))
#             elif parens[c]:
#                 while os:
#                     ns.append(getattr(ns.pop(), opers[os.pop()][0])(ns.pop()))
#                 return ns.pop()
#         elif c not in opers:
#             ns.append(int(c))
#         elif c in opers:
#             while os and opers[os[-1]][1] >= opers[c][1]:
#                 ns.append(getattr(ns.pop(), opers[os.pop()][0])(ns.pop()))
#             os.append(c)
#     while os:
#         ns.append(getattr(ns.pop(), opers[os.pop()][0])(ns.pop()))
#     return ns.pop()
# # print(evalinp('1 + 2 * 3 + 4')) #3,079
# print(evalinp('1 + 2 * (3 - 4) ^ 5 % 3'))