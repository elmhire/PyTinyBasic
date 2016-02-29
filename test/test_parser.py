#!/usr/bin/env python3

import unittest
from pyTBasic import parser
from pyTBasic.basic_types import *


class BasicParserTest(unittest.TestCase):
    def setUp(self):
        self.e = parser.BasicParser()

    def test_expr(self):
        test_expr1 = 'PRINT X - -2 * 2'
        test_expr2 = 'PRINT (-X + +Y) - +2 * 2'
        test_expr3 = 'PRINT ((4 + 2) / (7 + 5) - 2) * 3'
        test_expr4 = 'PRINT 2 + 10 / (2 + 2)'
        expr_parsed1 = Print([Sub(Var('X'), (Mul(Num(-2), Num(2))))])
        expr_parsed2 = Print([Sub(Add(Var('-X'), Var('Y')), Mul(Num(2), Num(2)))])
        expr_parsed3 = Print([Mul(Sub(Div(Add(Num(4), Num(2)), Add(Num(7), Num(5))),
                               Num(2)), Num(3))])
        expr_parsed4 = Print([Add(Num(2), Div(Num(10), Add(Num(2), Num(2))))])

        self.assertEqual(self.e.parse(test_expr1), expr_parsed1)
        self.assertEqual(self.e.parse(test_expr2), expr_parsed2)
        self.assertEqual(self.e.parse(test_expr3), expr_parsed3)
        self.assertEqual(self.e.parse(test_expr4), expr_parsed4)

    # def test_line(self):
        # line_test1 = '10 PRINT X'
        # line_test2 = 'PRINT X - 2'
        # parsed_test1 = (10, ('PRINT', ('V_X')))
        # parsed_test2 = ('PRINT', ('-', 'V_X', 2))

        # self.assertEqual(self.e.parse(line_test1), parsed_test1)
        # self.assertEqual(self.e.parse(line_test2), parsed_test2)

    def test_print_statement(self):
        print_statement1 = 'PRINT "The variable B is ", B'
        print_statement2 = 'PRINT "Hello, World!"'
        print_statement3 = 'PRINT "B is ", B, " cents ", C'
        print_statement4 = 'PRINT X'
        print_statement5 = 'PRINT X, " is a test."'
        print_statement6 = 'PRINT X - 2, " is x - 2."'
        print_statement7 = 'PRINT ((((( ((((( ((((( 15 ))))) ))))) )))))'
        print_statement8 = 'PRINT'
        parsed_statement1 = Print([String('The variable B is '), Var('B')])
        parsed_statement2 = Print([String('Hello, World!')])
        parsed_statement3 = Print([String('B is '), Var('B'), String(' cents '),
                                   Var('C')])
        parsed_statement4 = Print([Var('X')])
        parsed_statement5 = Print([Var('X'), String(' is a test.')])
        parsed_statement6 = Print([Sub(Var('X'), Num(2)), String(' is x - 2.')])
        parsed_statement7 = Print([Num(15)])
        parsed_statement8 = Print([])
        print_statement_invalid1 = 'PRINT "The variable B is " B'

        self.assertEqual(self.e.parse(print_statement1), parsed_statement1)
        self.assertEqual(self.e.parse(print_statement2), parsed_statement2)
        self.assertEqual(self.e.parse(print_statement3), parsed_statement3)
        self.assertEqual(self.e.parse(print_statement4), parsed_statement4)
        self.assertEqual(self.e.parse(print_statement5), parsed_statement5)
        self.assertEqual(self.e.parse(print_statement6), parsed_statement6)
        self.assertEqual(self.e.parse(print_statement7), parsed_statement7)
        self.assertEqual(self.e.parse(print_statement8), parsed_statement8)

        with self.assertRaises(SyntaxError):
            self.e.parse(print_statement_invalid1)

    def test_if_statement(self):
        if_statement1 = 'IF X = 2 THEN PRINT "X = 2"'
        if_statement2 = 'IF X > 2 THEN PRINT "X > 2"'
        if_statement3 = 'IF X > 2 THEN LET Y = 3'
        if_statement4 = 'IF X <> 2 THEN LET Y = 3'
        if_statement5 = 'IF X+2 <> 2-2 THEN LET Y = 3'
        parsed_statement1 = If(Equal(Var('X'), Num(2)),
                               Print([String('X = 2')]))
        parsed_statement2 = If(GreaterThan(Var('X'), Num(2)),
                               Print([String('X > 2')]))
        parsed_statement3 = If(GreaterThan(Var('X'), Num(2)),
                               Let(Assign(String('Y'), Num(3))))
        parsed_statement4 = If(NotEqual(Var('X'), Num(2)),
                               Let(Assign(String('Y'), Num(3))))
        parsed_statement5 = If(NotEqual(Add(Var('X'), Num(2)),
                                        Sub(Num(2), Num(2))),
                               Let(Assign(String('Y'), Num(3))))

        self.assertEqual(self.e.parse(if_statement1), parsed_statement1)
        self.assertEqual(self.e.parse(if_statement2), parsed_statement2)
        self.assertEqual(self.e.parse(if_statement3), parsed_statement3)
        self.assertEqual(self.e.parse(if_statement4), parsed_statement4)
        self.assertEqual(self.e.parse(if_statement5), parsed_statement5)

        with self.assertRaises(SyntaxError):
            self.e.parse('IF X THEN LET Y = 3')
        with self.assertRaises(SyntaxError):
            self.e.parse('IF X')

    def test_goto_statement(self):
        goto_statement1 = 'GOTO 10'
        goto_statement2 = 'GOTO 10+4'
        parsed_statement1 = Goto(Num(10))
        parsed_statement2 = Goto(Add(Num(10), Num(4)))
        goto_statement_invalid = 'GOTO'

        self.assertEqual(self.e.parse(goto_statement1), parsed_statement1)
        self.assertEqual(self.e.parse(goto_statement2), parsed_statement2)

        with self.assertRaises(SyntaxError):
            self.e.parse(goto_statement_invalid)

    def test_input(self):
        input_statement1 = 'INPUT A'
        input_statement2 = 'INPUT A, B'
        input_statement3 = 'INPUT A, B, C'
        input_statement4 = '10 INPUT A, B, C'
        parsed_input1 = Input([Var('A')])
        parsed_input2 = Input([Var('A'), Var('B')])
        parsed_input3 = Input([Var('A'), Var('B'), Var('C')])
        parsed_input4 = LineNum(Num(10), Input([Var('A'), Var('B'), Var('C')]))
        input_statement_invalid = 'INPUT A B'

        self.assertEqual(self.e.parse(input_statement1), parsed_input1)
        self.assertEqual(self.e.parse(input_statement2), parsed_input2)
        self.assertEqual(self.e.parse(input_statement3), parsed_input3)
        self.assertEqual(self.e.parse(input_statement4), parsed_input4)
        with self.assertRaises(SyntaxError):
            self.e.parse(input_statement_invalid)

    def test_let_statement(self):
        let_statement1 = 'LET X = 3'
        let_statement2 = 'LET X = -3'
        let_statement3 = 'LET X'
        let_statement4 = 'LET X ='
        parsed_let1 = Let(Assign(String('X'), Num(3)))
        parsed_let2 = Let(Assign(String('X'), Num(-3)))

        self.assertEqual(self.e.parse(let_statement1), parsed_let1)
        self.assertEqual(self.e.parse(let_statement2), parsed_let2)

        with self.assertRaises(SyntaxError):
            self.e.parse(let_statement3)
        with self.assertRaises(SyntaxError):
            self.e.parse(let_statement4)

    def test_gosub_statement(self):
        gosub_statement1 = 'GOSUB 10'
        parsed_gosub1 = Gosub(Num(10))
        gosub_statement_invalid = 'GOSUB'

        self.assertEqual(self.e.parse(gosub_statement1), parsed_gosub1)

        with self.assertRaises(SyntaxError):
            self.e.parse(gosub_statement_invalid)

    def test_return_statement(self):
        return_statement1 = 'RETURN'
        return_statement2 = '10 RETURN'

        parsed_return1 = Return(None)
        parsed_return2 = LineNum(Num(10), Return(None))

        self.assertEqual(self.e.parse(return_statement1), parsed_return1)
        self.assertEqual(self.e.parse(return_statement2), parsed_return2)

    def test_list_statement(self):
        list_statement1 = 'LIST'
        list_statement2 = 'LIST 20'
        parsed_statement1 = List(None)
        parsed_statement2 = List(Num(20))
        list_statement_invalid = 'LIST PRINT'

        self.assertEqual(self.e.parse(list_statement1), parsed_statement1)
        self.assertEqual(self.e.parse(list_statement2), parsed_statement2)

        with self.assertRaises(SyntaxError):
            self.e.parse(list_statement_invalid)


if __name__ == '__main__':
    unittest.main()
