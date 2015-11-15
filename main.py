#!/usr/bin/env python3

from pyTBasic import parser
from pyTBasic import evaluator


if __name__ == '__main__':
    b_parser = parser.BasicParser()
    b_evaluator = evaluator.Evaluator()
    _input = ''
    while _input != 'exit()':
        _input = input("] ")
        try:
            parsed = b_parser.parse(_input.upper())
            result = b_evaluator.visit(parsed)
        except SyntaxError as e:
            print("SYNTAX ERROR ", e)
        else:
            continue


