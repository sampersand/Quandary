from constants import constants
from node import getiter
from knowndict import knowndict

if __name__ == '__main__':
    with open('qfiles/testcode.qq') as f:
        gen = getiter(constants(), f.read())
    n = next(gen)
    known = knowndict(n.consts)
    print('----')
    print(n.evalnode(gen, known))
    print('----\n')
    if __debug__ and '$dnd' not in known:
        print(known, end = '\n--\n')
        print(repr(known))