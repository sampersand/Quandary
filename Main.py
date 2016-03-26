from Constants import constants
from Node import node

if __name__ == '__main__':
    with open('qfiles/testcode.qq') as f:
        n = node.getiter(constants(), f.read())


