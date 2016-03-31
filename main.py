from typing import Callable
def checkannotations(func: Callable, params: dict):
    annotations = func.__annotations__
    for param in params:
        if param not in annotations or (type(params[param]).__qualname__ != str(annotations[param]) and
                                        type(params[param]).__qualname__ != annotations[param].__qualname__):
            return False
    return True
from constants import constants
from node import node, getiter
from knowndict import knowndict

if __name__ == '__main__':
    n = node(constants())
    with open('qfiles/testcode.qq') as f:
        gen = getiter(n.consts, f.read())
    known = knowndict(n.consts)
    print('----')
    print(n.evalnode(gen, known), known)
    print('----\n')
    if __debug__ and '$dnd' not in known:
        print(known, end = '\n--\n')
        print(repr(known))