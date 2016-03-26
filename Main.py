# from Constants import constants
# from Node import node

# if __name__ == '__main__':
#     with open('qfiles/testcode.qq') as f:
#         n = node.fromiter(constants(), f.read())
def evalinp(inp):
    ns, os = [], []
    inp = inp.replace(' ', '')
    opers = {'+':('__radd__',0),
             '-':('__rsub__',0),
             '*':('__rmul__',1),
             '/':('__rdiv__',1),
             '%':('__rmod__',1),
             '^':('__rpow__',2)}

    for c in inp:
        print('b4',os, ns, c)
        if c not in opers:
            ns.append(int(c))
        if c in opers:
            while os and opers[os[-1]][1] > opers[c][1]:
                ns.append(getattr(ns.pop(), opers[os.pop()][0])(ns.pop()))
            os.append(c)
    while os:
        ns.append(getattr(ns.pop(), opers[os.pop()][0])(ns.pop()))
    return ns.pop()
# print(evalinp('1 + 2 * 3 + 4')) #3,079
print(evalinp('1 + 2 * 3 + 4 ^ 5 * 3')) #3,079