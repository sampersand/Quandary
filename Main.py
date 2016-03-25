from Constants import constants
from Node import node
if __name__ == '__main__':
    with open('qfiles/testcode.qq') as f:
        n = node.fromiter(constants(), f.read())
        print(n)