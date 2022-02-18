from lark import Lark
from quack_grammar import quack_grammar
from quack_middle import ASTBuilder, ASTVisitor
from quack_types import typechecker
from quack_checks import initialization_check
from quack_codegen import codegen

import argparse

parser = argparse.ArgumentParser(description=
                                 'Compile quack into assembly')

parser.add_argument('-i', '--input', default=None,
                    help="Specify input file name, otherwise will take lines from standard input.")
parser.add_argument('-o', '--output', default=None,
                    help="Specify output file name, otherwise will print to standard output.")
parser.add_argument('-c', '--class', default=None,
                    help="Specify class name. Must match <class>.qk")

args = parser.parse_args()

quack_parser = Lark(quack_grammar, parser='lalr')

def main():

    # configure command line args
    arguments = vars(args)
    f_input: str = arguments["input"]
    f_output = arguments["output"]
    clazz = arguments["class"]
    s = ""

    codegen.set_filename(clazz)

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

    quack = quack_parser.parse(s)

    # Middle-end basic optimizations
    ast = ASTBuilder().transform(quack)

    # check for variable inits before uses
    ast.check_init(initialization_check, set())
    
    # run the typechecker and more middle end optimizations
    ast.check_type(typechecker)

    # Back-end optimizations and godegen
    ast.generate(codegen)

    # print the code to corresponding output
    codegen.print_instructions(f_output)
        
if __name__ == '__main__':
    main()
