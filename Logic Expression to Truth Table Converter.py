# -*- coding: utf-8 -*-
"""Copy of DM PROJECT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H04qAE1RzsGu023I9FilOcpxm_suVk--
"""

from pyparsing import infixNotation, opAssoc, Keyword, ParserElement, Word, alphas
import itertools

# Define logical operations with binary values
def NOT(p):
    return 1 if p == 0 else 0

def AND(p, q):
    return p & q

def OR(p, q):
    return p | q

def XOR(p, q):
    return p ^ q

def IMPLIES(p, q):
    return 1 if p == 0 or q == 1 else 0

def IFF(p, q):
    return 1 if p == q else 0

# Define expression parsing
ParserElement.enablePackrat()

class BoolOperand:
    def __init__(self, tokens):
        self.name = tokens[0]

    def __str__(self):
        return self.name

    def eval(self, value_dict):
        return value_dict[self.name]

class BoolBinOp:
    def __init__(self, tokens):
        self.args = tokens[0][0::2]

    def __str__(self):
        sep = " " + self.op + " "
        return "(" + sep.join(map(str, self.args)) + ")"

    def eval(self, value_dict):
        raise NotImplementedError

class BoolNot(BoolBinOp):
    def __init__(self, tokens):
        self.arg = tokens[0][1]

    def __str__(self):
        return "~" + str(self.arg)

    def eval(self, value_dict):
        return NOT(self.arg.eval(value_dict))

class BoolAnd(BoolBinOp):
    op = 'AND'

    def eval(self, value_dict):
        return AND(self.args[0].eval(value_dict), self.args[1].eval(value_dict))

class BoolOr(BoolBinOp):
    op = 'OR'

    def eval(self, value_dict):
        return OR(self.args[0].eval(value_dict), self.args[1].eval(value_dict))

class BoolXor(BoolBinOp):
    op = 'XOR'

    def eval(self, value_dict):
        return XOR(self.args[0].eval(value_dict), self.args[1].eval(value_dict))

class BoolImplies(BoolBinOp):
    op = '->'

    def eval(self, value_dict):
        return IMPLIES(self.args[0].eval(value_dict), self.args[1].eval(value_dict))

class BoolIff(BoolBinOp):
    op = '<->'

    def eval(self, value_dict):
        return IFF(self.args[0].eval(value_dict), self.args[1].eval(value_dict))

# Define grammar
variable = Word(alphas, max=1).setParseAction(BoolOperand)
not_ = Keyword("NOT") | Keyword("~") | Keyword("¬")
and_ = Keyword("AND") | Keyword("&") | Keyword("∧") | Keyword("*")
or_ = Keyword("OR") | Keyword("|") | Keyword("∨") | Keyword("+")
xor_ = Keyword("XOR") | Keyword("^") | Keyword("⊻") | Keyword("⊕") | Keyword("⨁")
implies_ = Keyword("->") | Keyword("→") | Keyword("⟹") | Keyword("⟶") | Keyword("⇒")
iff_ = Keyword("<->") | Keyword("↔") | Keyword("⇔") | Keyword("⟷") | Keyword("⟺")

bool_expr = infixNotation(variable,
                          [
                              (not_, 1, opAssoc.RIGHT, BoolNot),
                              (and_, 2, opAssoc.LEFT, BoolAnd),
                              (or_, 2, opAssoc.LEFT, BoolOr),
                              (xor_, 2, opAssoc.LEFT, BoolXor),
                              (implies_, 2, opAssoc.RIGHT, BoolImplies),
                              (iff_, 2, opAssoc.LEFT, BoolIff),
                          ])

# Helper function to extract variables from the parsed expression tree
def extract_variables(parsed_expr):
    variables = set()
    if isinstance(parsed_expr, BoolOperand):
        variables.add(parsed_expr.name)
    elif isinstance(parsed_expr, BoolNot):
        variables.update(extract_variables(parsed_expr.arg))
    else:
        for arg in parsed_expr.args:
            variables.update(extract_variables(arg))
    return variables

# Function to generate intermediate expressions
def intermediate_expr(parsed_expr, value_dict):
    if isinstance(parsed_expr, BoolOperand):
        return value_dict[parsed_expr.name]
    elif isinstance(parsed_expr, BoolNot):
        return NOT(intermediate_expr(parsed_expr.arg, value_dict))
    elif isinstance(parsed_expr, BoolAnd):
        return AND(intermediate_expr(parsed_expr.args[0], value_dict), intermediate_expr(parsed_expr.args[1], value_dict))
    elif isinstance(parsed_expr, BoolOr):
        return OR(intermediate_expr(parsed_expr.args[0], value_dict), intermediate_expr(parsed_expr.args[1], value_dict))
    elif isinstance(parsed_expr, BoolXor):
        return XOR(intermediate_expr(parsed_expr.args[0], value_dict), intermediate_expr(parsed_expr.args[1], value_dict))
    elif isinstance(parsed_expr, BoolImplies):
        return IMPLIES(intermediate_expr(parsed_expr.args[0], value_dict), intermediate_expr(parsed_expr.args[1], value_dict))
    elif isinstance(parsed_expr, BoolIff):
        return IFF(intermediate_expr(parsed_expr.args[0], value_dict), intermediate_expr(parsed_expr.args[1], value_dict))
    else:
        raise ValueError("Unknown expression type")

# Function to generate truth table
def generate_truth_table(expr):
    parsed_expr = bool_expr.parseString(expr)[0]

    # Extract variables from the parsed expression
    variables = sorted(extract_variables(parsed_expr))

    truth_combinations = list(itertools.product([0, 1], repeat=len(variables)))

    # Collect intermediate expressions for header
    intermediate_expressions = []
    def collect_intermediate_expressions(expr):
        if isinstance(expr, BoolBinOp) and not isinstance(expr, BoolOperand):
            for arg in expr.args:
                collect_intermediate_expressions(arg)
            intermediate_expressions.append(str(expr))
        elif isinstance(expr, BoolNot):
            collect_intermediate_expressions(expr.arg)
            intermediate_expressions.append(str(expr))
    collect_intermediate_expressions(parsed_expr)

    # Print header
    headers = variables + intermediate_expressions
    print(" | ".join(headers))
    print("-" * (len(headers) * 6 + 1))

    for combination in truth_combinations:
        value_dict = dict(zip(variables, combination))
        intermediate_values = [str(intermediate_expr(bool_expr.parseString(ie)[0], value_dict)) for ie in intermediate_expressions]
        row = [str(value_dict[var]) for var in variables] + intermediate_values
        print(" | ".join(row))

# Main code to get user input and generate truth table
if __name__ == "__main__":
    user_expression = input("Enter a logical expression: ")
    generate_truth_table(user_expression)