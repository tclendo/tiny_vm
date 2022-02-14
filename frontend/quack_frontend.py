from lark import Lark
from quack_grammar import quack_grammar
from quack_middle import ASTBuilder, ASTVisitor
from quack_codegen import codegen

import argparse

parser = argparse.ArgumentParser(description=
                                 'Compile quack into assembly')

parser.add_argument('-i', '--input', default=None,
                    help="Specify input file name, otherwise will take lines from standard input.")
parser.add_argument('-o', '--output', default=None,
                    help="Specify output file name, otherwise will print to standard output.")
args = parser.parse_args()

quack_parser = Lark(quack_grammar, parser='lalr')

def main():

    # configure command line args
    arguments = vars(args)
    f_input: str = arguments["input"]
    f_output = arguments["output"]
    s = ""

    # hacky way to get base filename for main class name
    try:
        mainclass = f_input.split('.')[0]
        mainclass = mainclass.split('/')[2]
        # end hacky way to get base filename
        codegen.set_filename(mainclass)
    except:
        codegen.set_filename("")

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
    ast.generate(codegen)
    # Back-end optimizations and godegen
    codegen.print_instructions(f_output)
        
if __name__ == '__main__':
    main()
