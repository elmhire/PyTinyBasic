#!/usr/bin/env python3


class Node:
    __slots__ = ()

    def __repr__(self):
        return ''.join([str(type(self).__name__), '(', str(self.value), ')'])

    # def __eq__(self, other):
    #       return self.__dict__ == other.__dict__ \
    #            and type(self).__name__ == type(other).__name__


class UnaryOperator(Node):
    __slots__ = ['operand']

    def __init__(self, operand):
        self.operand = operand

    def __repr__(self):
        return ''.join([str(type(self).__name__), '(', str(self.operand), ')'])

    def __str__(self):
        return ''.join([str(type(self).__name__), ' ', str(self.operand)])


class BinaryOperator(Node):
    __slots__ = ['left', 'right']

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return ''.join([str(type(self).__name__),
                        '(', repr(self.left), ', ', repr(self.right), ')'])

    def __str__(self):
        return ''.join([str(self.left), ' ',
                        str(self.right)
                        ])


class Relop(BinaryOperator):
    __slots__ = ()


class LineNum(BinaryOperator):
    __slots__ = ()

    def __str__(self):
        return ''.join([str(self.left.value), ' ', str(self.right)])


# Operators
class Add(BinaryOperator):
    __slots__ = ()


class Sub(BinaryOperator):
    __slots__ = ()


class Mul(BinaryOperator):
    __slots__ = ()


class Div(BinaryOperator):
    __slots__ = ()


# Relative Operators
class Equal(Relop):
    __slots__ = ()

    def __str__(self):
        return ''.join([str(self.left), ' = ', str(self.right)])


class NotEqual(Relop):
    __slots__ = ()


class GreaterThan(Relop):
    __slots__ = ()


class GreaterOrEqualThan(Relop):
    __slots__ = ()


class LessThan(Relop):
    __slots__ = ()


class LessOrEqualThan(Relop):
    __slots__ = ()


class Assign(BinaryOperator):
    __slots__ = ()


# Terminals
class Num(Node):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Var(Node):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class String(Node):
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Keywords
class Print(UnaryOperator):
    __slots__ = ()

    def __str__(self):
        return 'PRINT ' + ''.join([str(i) for i in self.operand])


class If(BinaryOperator):
    __slots__ = ()

    def __str__(self):
        # return 'IF ' + ''.join([str(self.left)])
        return ''.join(['IF ', str(self.left), ' THEN ', str(self.right)])


class Goto(UnaryOperator):
    __slots__ = ()


class Input(UnaryOperator):
    __slots__ = ()


class Let(BinaryOperator):
    __slots__ = ()

    def __str__(self):
        return ''.join(['LET ', str(self.left), ' = ', str(self.right)])


class Gosub(UnaryOperator):
    __slots__ = ()


class Return(UnaryOperator):
    __slots__ = ()


class Clear(UnaryOperator):
    __slots__ = ()


class List(UnaryOperator):
    __slots__ = ()


class Run(UnaryOperator):
    __slots__ = ()


class End(UnaryOperator):
    __slots__ = ()
