#!/usr/bin/env python3

# import types
from pyTBasic.basic_types import *
# from pyTBasic import parser

symbol_table = {chr(i): 0 for i in range(65, 91)}


class NodeVisitor:
    def visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):
        raise RuntimeError('No {} method'
                           .format('visit_' + type(node).__name__))


class Evaluator(NodeVisitor):
    def visit_String(self, node):
        return node.value

    def visit_Num(self, node):
        return node.value

    def visit_Var(self, node):
        return symbol_table[node.value]

    def visit_Add(self, node):
        return self.visit(node.left) + self.visit(node.right)

    def visit_Sub(self, node):
        return self.visit(node.left) - self.visit(node.right)

    def visit_Mul(self, node):
        return self.visit(node.left) * self.visit(node.right)

    def visit_Div(self, node):
        return self.visit(node.left) // self.visit(node.right)

    def visit_Equal(self, node):
        return self.visit(node.left) == self.visit(node.right)

    def visit_NotEqual(self, node):
        return self.visit(node.left) != self.visit(node.right)

    def visit_GreaterThan(self, node):
        return self.visit(node.left) > self.visit(node.right)

    def visit_GreaterOrEqualThan(self, node):
        return self.visit(node.left) >= self.visit(node.right)

    def visit_LessThan(self, node):
        return self.visit(node.left) < self.visit(node.right)

    def visit_LessOrEqualThan(self, node):
        return self.visit(node.left) <= self.visit(node.right)

    def visit_Print(self, node):
        print_string = [str(self.visit(i)) for i in node.operand]

        print(''.join(print_string))

    def visit_If(self, node):
        methname = 'visit_' + type(node.left).__name__
        visit_relop = getattr(self, methname, None)
        if visit_relop is not None:
            result = visit_relop(node.left)
        else:
            raise SyntaxError('Whoa, something went completely wrong!')
        if result:
            return self.visit(node.right)

    def visit_Goto(self, node):
        pass

    def visit_Input(self, node):
        pass

    def visit_Let(self, node):
        self.visit(node.operand)

    def visit_Assign(self, node):
        symbol_table[self.visit(node.left)] = self.visit(node.right)

    def visit_Gosub(self, node):
        pass

    def visit_Return(self, node):
        pass

    def visit_Clear(self, node):
        pass

    def visit_List(self, node):
        pass

    def visit_Run(self, node):
        pass

    def visit_End(self, node):
        pass


class PrintParseTree(NodeVisitor):
    def visit_String(self, node):
        print(node)

    def visit_Num(self, node):
        print(node)

    def visit_Var(self, node):
        print(node)

    def visit_Add(self, node):
        print(node)

    def visit_Sub(self, node):
        print(node)

    def visit_Mul(self, node):
        print(node)

    def visit_Div(self, node):
        print(node)

    def visit_Print(self, node):
        print(node)

    def visit_If(self, node):
        print(node)

    def visit_Goto(self, node):
        print(node)

    def visit_Input(self, node):
        print(node)

    def visit_Let(self, node):
        print(node)

    def visit_Assign(self, node):
        print(node)

    def visit_Gosub(self, node):
        print(node)

    def visit_Return(self, node):
        print(node)

    def visit_Clear(self, node):
        print(node)

    def visit_List(self, node):
        print(node)

    def visit_Run(self, node):
        print(node)

    def visit_End(self, node):
        print(node)
