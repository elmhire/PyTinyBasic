#!/usr/bin/env python

import re
from collections import namedtuple

''' Tiny Basic Grammar, EBNF

 line ::= number statement CR | statement CR

   statement ::= PRINT expr-list
                 IF expression relop expression THEN statement
                 GOTO expression
                 INPUT var-list
                 LET var = expression
                 GOSUB expression
                 RETURN
                 CLEAR
                 LIST
                 RUN
                 END

   expr-list ::= (string|expression) (, (string|expression) )*

   var-list ::= var (, var)*

   expression ::= (+|-|ε) term ((+|-) term)*

   term ::= factor ((*|/) factor)*

   factor ::= var | number | (expression)

   var ::= A | B | C ... | Y | Z

   number ::= digit digit*

   digit ::= 0 | 1 | 2 | 3 | ... | 8 | 9

   relop ::= < (>|=|ε) | > (<|=|ε) | =

Added by me (maybe help with negative numbers?):
   unary_op ::= "+" | "-"

   binary_op ::= "+" | "-" | "*" | "/" | "%" | "**"
'''

KWORD   = r'(?P<KWORD>PRINT|IF|THEN|GOTO|INPUT|LET|GOSUB|RETURN|CLEAR|LIST|RUN|END)'
STRNG   = r'(?P<STRNG>"([^"]*)")'
VAR     = r'(?P<VAR>[A-Z])'
NUM     = r'(?P<NUM>\d*\.\d+|\d+)'
PLUS    = r'(?P<PLUS>\+)'
MINUS   = r'(?P<MINUS>-)'
TIMES   = r'(?P<TIMES>\*)'
DIVIDE  = r'(?P<DIVIDE>/)'
LPAREN  = r'(?P<LPAREN>\()'
RPAREN  = r'(?P<RPAREN>\))'
RELOP   = r'(?P<RELOP><>|><|<=|>=|<|>|=)'
WS      = r'(?P<WS>\s+)'
COM     = r'(?P<COM>,)'
SEMI    = r'(?P<SEMI>;)'

master_pat = re.compile('|'.join([KWORD, STRNG, VAR, NUM, PLUS, MINUS, TIMES,
                                  DIVIDE, LPAREN, RPAREN, RELOP, WS, COM,
                                  SEMI]))

# Tokenizer
Token = namedtuple('Token', ['type', 'value'])

def generate_tokens(text):
    '''
    pattern: re object,
    text: string to generate tokens from
    '''
    scanner = master_pat.scanner(text)
    for match in iter(scanner.match, None):
        tok = Token(match.lastgroup, match.group())
        if tok.type != 'WS':
            if tok.type == 'VAR':
                yield Token('VAR', 'V_' + tok.value)
            else:
                yield tok


# Parser
class BasicParser:
    '''
    Implementation of a recursive descent parser. Each method
    implements a simple grammar rule. Use the ._accept() method
    to test and accept the current lookahead token. Use the ._expect()
    method to exactly match and discard the next token on the input
    (or raise a SyntaxError if it doesn't match).
    '''

    def parse(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None             # Last symbol consumed
        self.nexttok = None         # Next symbol tokenized
        self._advance()             # Load first lookahead token
        return self.line()

    def _advance(self):
        'Advance one token ahead'
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        'Test and consume the next token if it matches toktype'
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self, toktype):
        'Consume next token if it matches toktype or raise SyntaxError'
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    # Grammar rules follow

    def line(self):
        '''
         line ::= number statement CR | statement CR
        '''
        if self._accept('NUM'):
            num = self.try_int(self.tok.value)
            right = self.statement()
            ret_val = (num, right)
        else:
            ret_val = self.statement()
        return ret_val

    def statement(self):
        '''
        statement ::= PRINT expr-list
                      IF expression relop expression THEN statement
                      GOTO expression
                      INPUT var-list
                      LET var = expression
                      GOSUB expression
                      RETURN
                      CLEAR
                      LIST
                      RUN
                      END
        '''
        if self._accept('KWORD'):
            if self.tok.value == 'PRINT':
                ret_val = self.kw_print()
            elif self.tok.value == 'IF':
                ret_val = self.kw_if()
            elif self.tok.value == 'GOTO':
                ret_val = self.kw_goto()
            elif self.tok.value == 'INPUT':
                ret_val = self.kw_input()
            elif self.tok.value == 'LET':
                ret_val = self.kw_let()
            elif self.tok.value == 'GOSUB':
                ret_val = self.kw_gosub()
            elif self.tok.value == 'RETURN':
                return 'RETURN'
            elif self.tok.value == 'CLEAR':
                return 'CLEAR'
            elif self.tok.value == 'LIST':
                return self.kw_list()
            elif self.tok.value == 'RUN':
                return 'RUN'
            elif self.tok.value == 'END':
                return 'END'
        else:
            ret_val = self.expr()
        return ret_val

    def kw_print(self):
        kw = self.tok.value
        if not self.nexttok:
            return (kw, '')
        right = self.expr_list()
        ret_val = (kw, right)
        return ret_val

    def kw_if(self):
        kw = self.tok.value
        left_expr = self.expr()
        self._expect('RELOP')
        relop = self.tok.value
        right_expr = self.expr()
        self._expect('KWORD')
        kw2 = 'THEN'
        then_statement = self.statement()
        return (kw, (relop, left_expr, right_expr), kw2, then_statement)

    def kw_goto(self):
        kw = self.tok.value
        if not self.nexttok:
            raise SyntaxError('Expected NUM')
        right = self.expr()
        return (kw, right)

    def kw_input(self):
        kw = self.tok.value
        right = self.var_list()
        return (kw, right)

    def kw_let(self):
        kw = self.tok.value
        self._expect('VAR')
        var = self.tok.value
        self._expect('RELOP')
        op = self.tok.value
        if op != '=':
            raise SyntaxError('Expected EQUAL')
        expr_val = self.expr()
        return (kw, (op, var, expr_val))

    def kw_gosub(self):
        kw = 'GOSUB'
        right = self.expr()
        if not right:
            raise SyntaxError('Expected EXPRESSION')
        return (kw, right)

    def kw_list(self):
        kw = 'LIST'
        if self._accept('NUM'):
            right = self.try_int(self.tok.value)
        elif self.nexttok:
            raise SyntaxError('Expected NUM')
        else:
            return (kw)
        return (kw, right)

    def expr_list(self):
        '''
        expr-list ::= (string|expression) (, (string|expression) )*
        '''
        expr_list = []

        temp = self.expr()
        if temp:
            expr_list.append(temp)

        while self._accept('STRNG') or self._accept('COM'):
            if self.tok.type == 'STRNG':
                expr_list.append(self.tok.value)
            elif self.nexttok.type != 'STRNG':
                expr_list.append(self.expr())

        if self.nexttok:
            raise SyntaxError('Expected COMA')

        if len(expr_list) > 1:
            expr_string = tuple(i.strip('"') if type(i) == type('') else i
                               for i in expr_list)
        else:
            expr_string = (expr_list[0].strip('"')
                           if type(expr_list[0]) == type('') else expr_list[0])

        return expr_string

    def var_list(self):
        '''
        var-list ::= var (, var)*
        '''
        var_list = []
        while self.nexttok and self._accept('VAR'):
            var_list.append(self.tok.value)
            if self.nexttok:
                self._expect('COM')
            else:
                break
        return tuple(var_list)

    def expr(self):
        '''
        expression ::= (+|-|ε) term ((+|-) term)*

        '''
        expr_val = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.tok.type
            right = self.term()
            if op == 'PLUS':
                expr_val = ('+', expr_val, right)
            elif op == 'MINUS':
                expr_val = ('-', expr_val, right)
        return expr_val

    def term(self):
        '''
        term ::= factor ((*|/) factor)*
        '''
        term_val = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            if op == 'TIMES':
                term_val = ('*', term_val, right)
            elif op == 'DIVIDE':
                term_val = ('/', term_val, right)
        return term_val

    def factor(self):
        '''
        factor ::= var | number | (expression)
        '''
        # Is the next token a PLUS operator. Case is unary PLUS
        if self.nexttok and self.nexttok.type == 'PLUS':
            self._accept('PLUS')
            if self._accept('NUM'):
                ret_val = self.try_int(self.tok.value)
            elif self._accept('VAR'):
                ret_val = str(self.tok.value)
            else:
                raise SyntaxError('Expected NUM or VAR')
        # Is the next token a MINUS operator. Case is unary MINUS
        elif self.nexttok and self.nexttok.type == 'MINUS':
            self._accept('MINUS')
            if self._accept('NUM'):
                ret_val = int(-(self.try_int(self.tok.value)))
            elif self._accept('VAR'):
                ret_val = '-'+str(self.tok.value)
            else:
                raise SyntaxError('Expected NUM or VAR')
        elif self._accept('NUM'):
            ret_val = self.try_int(self.tok.value)
        elif self._accept('VAR'):
            ret_val = str(self.tok.value)
        elif self._accept('LPAREN'):
            expr_val = self.expr()
            self._expect('RPAREN')
            ret_val = expr_val
        # Is this just a string that ended up here?
        elif self.nexttok and type(self.nexttok.value) == type(''):
            return None
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')
        return ret_val

    def try_int(self, integer):
        try:
            new_int = int(integer)
        except ValueError:
            raise SyntexError('Expected NUM')
        return new_int
