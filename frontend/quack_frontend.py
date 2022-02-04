from lark import Lark
from quack_middle import ASTBuilder
from quack_codegen import codegen

import argparse

parser = argparse.ArgumentParser(description=
                                 'Compile quack into assembly')

parser.add_argument('-i', '--input', default=None,
                    help="Specify input file name, otherwise will take lines from standard input.")
parser.add_argument('-o', '--output', default=None,
                    help="Specify output file name, otherwise will print to standard output.")
args = parser.parse_args()

quack_grammar = """
?start: program

?program: stmt*

?stmt: assignment ";"
| r_expr ";" 

?assignment: l_expr ":" type "=" r_expr -> assign_var

?type: NAME

?l_expr: NAME 

?r_expr: sum
| r_expr "." NAME "()" -> call

?sum: product
| sum "+" product   -> add
| sum "-" product   -> sub

?product: atom
| product "*" atom  -> mul
| product "/" atom  -> div

?atom: NUMBER      -> number
| STRING -> str_lit
| "-" atom         -> neg
| l_expr -> var
| "(" sum ")"
| bool
| "Nothing" -> lit_nothing

?bool: "true" -> lit_true
| "false" -> lit_false

%import common.CNAME -> NAME
%import common.ESCAPED_STRING -> STRING
%import common.NUMBER

EOL: /\\n/

%import common.WS_INLINE
%ignore WS_INLINE
%ignore EOL
"""

# Easy front end. Thanks lark
quack_parser = Lark(quack_grammar, parser='lalr')

def main():

    # configure command line args
    arguments = vars(args)
    f_input: str = arguments["input"]
    f_output = arguments["output"]
    s = ""

    # hacky way to get base filename for main class name
    mainclass = f_input.split('.')[0]
    mainclass = mainclass.split('/')[1]
    # end hacky way to get base filename
    codegen.set_filename(mainclass)

    # if there exists an inputfilename
    if (f_input):
        with open(f_input, 'r', encoding='utf-8') as f:
            for line in f:
                s += line

    else:
        while True:
            try:
                s += input()
            except EOFError:
                break

    # Middle-end optimizations
    quack = quack_parser.parse(s)
    ast = ASTBuilder().transform(quack)
    # Back-end optimizations and godegen
    codegen.print_instructions(f_output)
        
if __name__ == '__main__':
    main()
