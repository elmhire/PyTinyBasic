#!/usr/bin/env python3


class Node:
    pass

    def __repr__(self):
        return ''.join([str(type(self).__name__), '(', str(self.value), ')'])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ \
                and type(self).__name__ == type(other).__name__


class UnaryOperator(Node):
    __slots__ = ['operand']

    def __init__(self, operand):
        self.operand = operand

    def __repr__(self):
        return ''.join([str(type(self).__name__), '(', str(self.operand), ')'])


class BinaryOperator(Node):
    __slots__ = ['left', 'right']

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return ''.join([str(type(self).__name__),
                        '(', repr(self.left), ', ', repr(self.right), ')'])


class Relop(BinaryOperator):
    pass


class LineNum(BinaryOperator):
    pass


# Operators
class Add(BinaryOperator):
    pass


class Sub(BinaryOperator):
    pass


class Mul(BinaryOperator):
    pass


class Div(BinaryOperator):
    pass


# Relative Operators
class Equal(Relop):
    pass


class NotEqual(Relop):
    pass


class GreaterThan(Relop):
    pass


class GreaterOrEqualThan(Relop):
    pass


class LessThan(Relop):
    pass


class LessOrEqualThan(Relop):
    pass


class Assign(BinaryOperator):
    pass


# Terminals
class Num(Node):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value


class Var(Node):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value


class String(Node):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value


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


class Return(UnaryOperator):
    pass


class Clear(UnaryOperator):
    pass


class List(UnaryOperator):
    pass


class Run(UnaryOperator):
    pass


class End(UnaryOperator):
    pass
