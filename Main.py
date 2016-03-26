from Constants import constants
from Node import getiter
from KnownDict import knowndict
class foo():
    def __init__(self, arg):
        super().__init__()
        self.arg = arg

if __name__ == '__main__':
    with open('qfiles/testcode.qq') as f:
        gen = getiter(constants(), f.read())
        n = next(gen)
        n.evaluate(gen, )