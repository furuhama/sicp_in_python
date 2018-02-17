"""
implement calculator
"""

from operator import mul
from functools import reduce

class Exp(object):
    """ A call expression in Calculator. """
    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

    def __repr__(self):
        return 'Exp({0}, {1})'.format(repr(self.operator), repr(self.operands))

    def __str__(self):
        operands_strs = ', '.join(map(str, self.operands))
        return '{0}({1})'.format(self.operator, operands_strs)


def calc_eval(exp):
    """ Evaluate a Calculator expression. """
    if isinstance(exp, (int, float)):
        return exp
    elif isinstance(exp, Exp):
        arguments = list(map(calc_eval, exp.operands))
        return calc_apply(exp.operator, arguments)


def calc_apply(operator, args):
    """ Apply the named operator to a list of args. """
    if operator in ('add', '+'):
        return sum(args)
    if operator in ('sub', '-'):
        if len(args) == 0:
            raise TypeError(operator + ' requires at least 1 argument')
        if len(args) == 1:
            return -args[0]
        return sum(args[:1] + [-arg for arg in args[1:]])
    if operator in ('mul', '*'):
        return reduce(mul, args, 1)
    if operator in ('div', '/'):
        if len(args) != 2:
            raise TypeError(operator + ' requires exactly 2 arguments')
        numer, denom = args
        return numer/denom


def calc_parse(line):
    """ Parse a line of calculator input and return an expression tree. """
    tokens = tokenize(line)
    expression_tree = analyze(tokens)
    if len(tokens) > 0:
        raise SyntaxError('Extra token(s): ' + ' '.join(tokens))
    return expression_tree


def tokenize(line):
    """ Convert a string into a list of tokens. """
    spaced = line.replace('(', ' ( ').replace(')', ' ) ').replace(',', ' , ')
    return spaced.split()


def analyze(tokens):
    """ Create a tree of nested lists from a sequence of tokens. """
    token = analyze_token(tokens.pop(0))
    if isinstance(token, (int, float)):
        return token
    else:
        tokens.pop(0) # Remove `(`
        return Exp(token, analyze_operands(tokens))


def analyze_token(token):
    """ Return the value of token
        if it can be analyzed as a number, or token. """
    try:
        return int(token)
    except (TypeError, ValueError):
        try:
            return float(token)
        except (TypeError, ValueError):
            return token


def analyze_operands(tokens):
    """ Read a list of commma-separated operands. """
    operands = []
    while tokens[0] != ')':
        if operands:
            tokens.pop(0) # Remove `.`
        operands.append(analyze(tokens))
    tokens.pop(0) # Remove `)`
    return operands


"""
main function(REPL)
"""

def read_eval_print_loop():
    """ Run a read-eval-print loop for calculator. """
    while True:
        try:
            expression_tree = calc_parse(input('calc> '))
            print(calc_eval(expression_tree))
        except (SyntaxError, TypeError, ZeroDivisionError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError): #  <Control>-D, etc.
            print('Calculation completed.')
            return
