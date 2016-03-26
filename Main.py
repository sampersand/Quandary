from Constants import constants
from Node import getiter
from KnownDict import knowndict

if __name__ == '__main__':
    with open('qfiles/testcode.qq') as f:
        gen = getiter(constants(), f.read())
        n = next(gen)
        n.evaluate(gen, knowndict(n.const))
        print(knowndict(n.const))