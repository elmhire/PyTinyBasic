import unittest
from pyTBasic import parser

class BasicParserTest(unittest.TestCase):
    def setUp(self):
        self.e = parser.BasicParser()

    def test_line(self):
        line_test1 = '10 PRINT X'
        line_test2 = 'PRINT X - 2'
        parsed_test1 = (10, ('PRINT', ('V_X')))
        parsed_test2 = ('PRINT', ('-', 'V_X', 2))

        self.assertEqual(self.e.parse(line_test1), parsed_test1)
        self.assertEqual(self.e.parse(line_test2), parsed_test2)

    def test_print_statement(self):
        print_statement1 = 'PRINT "The variable B is ", B'
        print_statement2 = 'PRINT "Hello, World!"'
        print_statement3 = 'PRINT "B is ", B, " cents ", C'
        print_statement4 = 'PRINT X'
        print_statement5 = 'PRINT X, " is a test."'
        print_statement6 = 'PRINT X - 2, " is x - 2."'
        print_statement7 = 'PRINT ((((( ((((( ((((( 15 ))))) ))))) )))))'
        print_statement8 = 'PRINT'
        parsed_statement1 = ('PRINT', ('The variable B is ','V_B'))
        parsed_statement2 = ('PRINT', ('Hello, World!'))
        parsed_statement3 = ('PRINT', ('B is ', 'V_B', ' cents ', 'V_C'))
        parsed_statement4 = ('PRINT', ('V_X'))
        parsed_statement5 = ('PRINT', ('V_X', ' is a test.'))
        parsed_statement6 = ('PRINT', (('-', 'V_X', 2), ' is x - 2.'))
        parsed_statement7 = ('PRINT', (15))
        parsed_statement8 = ('PRINT', (''))
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
        parsed_statement1 = ('IF', ('=', 'V_X', 2),
                             'THEN', ('PRINT', ('X = 2')))
        parsed_statement2 = ('IF', ('>', 'V_X', 2),
                             'THEN', ('PRINT', ('X > 2')))
        parsed_statement3 = ('IF', ('>', 'V_X', 2),
                             'THEN', ('LET', ('=', 'V_Y', 3)))
        parsed_statement4 = ('IF', ('<>', 'V_X', 2),
                             'THEN',('LET', ('=', 'V_Y', 3)))
        parsed_statement5 = ('IF', ('<>', ('+', 'V_X', 2), ('-', 2, 2)),
                             'THEN',('LET', ('=', 'V_Y', 3)))

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
        parsed_statement1 = ('GOTO', (10))
        parsed_statement2 = ('GOTO', ('+', 10, 4))
        goto_statement_invalid = 'GOTO'

        self.assertEqual(self.e.parse(goto_statement1), parsed_statement1)
        self.assertEqual(self.e.parse(goto_statement2), parsed_statement2)
        with self.assertRaises(SyntaxError):
            self.e.parse(goto_statement_invalid)

    def test_input(self):
        input_statement1 = 'INPUT A, B'
        input_statement2 = 'INPUT A, B, C'
        input_statement3 = '10 INPUT A, B, C'
        parsed_input1 = ('INPUT', ('V_A', 'V_B'))
        parsed_input2 = ('INPUT', ('V_A', 'V_B', 'V_C'))
        parsed_input3 = (10, ('INPUT', ('V_A', 'V_B', 'V_C')))
        input_statement_invalid = 'INPUT A B'

        self.assertEqual(self.e.parse(input_statement1), parsed_input1)
        self.assertEqual(self.e.parse(input_statement2), parsed_input2)
        self.assertEqual(self.e.parse(input_statement3), parsed_input3)
        with self.assertRaises(SyntaxError):
            self.e.parse(input_statement_invalid)

    def test_let_statement(self):
        let_statement1 = 'LET X = 3'
        let_statement2 = 'LET X = -3'
        let_statement3 = 'LET X'
        let_statement4 = 'LET X ='

        self.assertEqual(self.e.parse(let_statement1),
                         ('LET', ('=', 'V_X', 3)))
        self.assertEqual(self.e.parse(let_statement2),
                         ('LET', ('=', 'V_X', -3)))
        with self.assertRaises(SyntaxError):
            self.e.parse(let_statement3)
        with self.assertRaises(SyntaxError):
            self.e.parse(let_statement4)

    def test_gosub_statement(self):
        gosub_statement1 = 'GOSUB 10'
        parsed_gosub1 = ('GOSUB', 10)
        gosub_statement_invalid = 'GOSUB'

        self.assertEqual(self.e.parse(gosub_statement1), parsed_gosub1)

        with self.assertRaises(SyntaxError):
            self.e.parse(gosub_statement_invalid)

    def test_return_statement(self):
        return_statement1 = 'RETURN'
        return_statement2 = '10 RETURN'

        parsed_return1 = ('RETURN')
        parsed_return2 = (10, 'RETURN')
        
        self.assertEqual(self.e.parse(return_statement1),
                              parsed_return1)
        self.assertEqual(self.e.parse(return_statement2),
                              parsed_return2)

    def test_list_statement(self):
        list_statement1 = 'LIST'
        list_statement2 = 'LIST 20'
        parsed_statement1 = ('LIST')
        parsed_statement2 = ('LIST', 20)
        list_statement_invalid = 'LIST PRINT'

        self.assertEqual(self.e.parse(list_statement1), parsed_statement1)
        self.assertEqual(self.e.parse(list_statement2), parsed_statement2)

        with self.assertRaises(SyntaxError):
            self.e.parse(list_statement_invalid)


if __name__ == '__main__':
    unittest.main()
