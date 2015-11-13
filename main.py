#!/usr/bin/env python3

from pyTBasic import parser


if __name__ == '__main__':
    test = 'PRINT "+ 2 + A * 4 is ", + B + A * 4, " and 3 + 3 is ", 3 + 3'
    #test = 'PRINT X'
    test2 = 'LET X = A + -B'
    test3 = 'GOTO 3'
    test4 = 'INPUT A, B, C'

    tokens = parser.generate_tokens(test)
    for item in tokens:
        print(item)
    print()

    e = parser.BasicParser()
    x = e.parse(test)
    print(x)
    for i in x:
        print(type(i), i)
