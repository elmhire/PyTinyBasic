#!/usr/bin/env python3

from pyTBasic import parser


if __name__ == '__main__':
    b_parser = parser.BasicParser()
    _input = ''
    while _input != 'exit()':
        _input = input("> ")
        try:
            out = b_parser.parse(_input)
        except SyntaxError as e:
            print("SYNTAX ERROR ", e)
        else:
            print(out)
