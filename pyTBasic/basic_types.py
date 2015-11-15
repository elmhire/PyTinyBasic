#!/usr/bin/env python3

class Node:
    pass

    def __repr__(self):
        return ''.join([str(type(self).__name__), '(', str(self.value), ')'])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ \
                and type(self).__name__ == type(other).__name__

class UnaryOperator(Node):
    def __init__(self, operand):
        self.operand = operand

    def __repr__(self):
        return ''.join([str(type(self).__name__), '(', str(self.operand), ')'])

class BinaryOperator(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return ''.join([str(type(self).__name__),
                        '(', repr(self.left), ',', repr(self.right), ')'])

# Operators
class Add(BinaryOperator):
    pass

class Sub(BinaryOperator):
    pass

class Mul(BinaryOperator):
    pass

class Div(BinaryOperator):
    pass

class Equal(BinaryOperator):
    pass

class NotEqual(BinaryOperator):
    pass

class GreaterThan(BinaryOperator):
    pass

class GreaterOrEqualThan(BinaryOperator):
    pass

class LessThan(BinaryOperator):
    pass

class LessOrEqualThan(BinaryOperator):
    pass

class Assign(BinaryOperator):
    pass

# Terminals
class Num(Node):
    def __init__(self, value):
        self.value = value

class Var(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return ''.join([str(type(self).__name__), '(', str(self.value), ')'])

# Keywords
class Print(UnaryOperator):
    pass

class If(BinaryOperator):
    pass

class Goto(UnaryOperator):
    pass

class Input(UnaryOperator):
    pass

class Let(UnaryOperator):
    pass

class Gosub(UnaryOperator):
    pass

class List(UnaryOperator):
    pass

if __name__ == '__main__':
    a = Var('A')
    b = Var('B')
    a_plus_b = Add(a, b)
    print(a_plus_b)

