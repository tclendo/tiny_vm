from lark import Lark, Transformer, v_args
import argparse

parser = argparse.ArgumentParser(description=
                                 'Compile quack into assembly')

parser.add_argument('-i', '--input', default=None,
                    help="Specify input file name, otherwise will take lines from standard input.")
parser.add_argument('-o', '--output', default=None,
                    help="Specify output file name, otherwise will print to standard output.")
args = parser.parse_args()

class QuackCodeGen:
    """
    QuackCodeGen is our class that handles generating code, and
    can be injected into the transformer classes so that they
    may modify this codegen class.
    """

    def __init__(self):
        # instruction stream that will be dumped at the end
        self.vars = {}
        self.instructions = []
        self.pusharg = 0

    def set_var(self, var, val):
        self.vars[var] = val
        
    def get_var(self, var):
        return self.vars[var]
    
    def add_instruction(self, instruction, arg):
        self.instructions.append(instruction)
        self.pusharg += arg

    def print_instructions(self, stream):
        if not stream:
            print(".class MAIN:Obj")
            print()
            print(".method $constructor")
            print(f".local {','.join(self.vars.keys())}")
            for element in self.instructions:
                print(element)

            while self.pusharg > 0:
                print("pop")
                self.pusharg -= 1

            print("return 0\n")

        else:
            with open(stream, 'w') as f:
                f.write(".class Sample:Obj\n")
                f.write("\n")
                f.write(".method $constructor\n")
                f.write(".local {}".format(','.join(self.vars.keys())))
                f.write('\n')
                # print(f".local {','.join(self.vars.keys())}")
                for instruction in self.instructions:
                    f.write(instruction)
                    f.write('\n')


                while self.pusharg > 0:
                    f.write("pop\n")
                    self.pusharg -= 1

                f.write("return 0")
        
quack_codegen = QuackCodeGen()

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

@v_args(inline=True)    # Affects the signatures of the methods
class QuackTransformer(Transformer):
    from operator import add, sub, mul, truediv as div, neg

    def __init__(self):
        # Codegen singleton class communicator
        self.codegen = QuackCodeGen()
        # dictionary of all the elements and their types
        self.types = {}

    def assign_var(self, name, typ, value):
        quack_codegen.add_instruction("store " + name, -1)
        self.types[name] = typ
        quack_codegen.set_var(name, value)
        return name 

    def add(self, a, b):
        if (self.types[a] == "Int"):
            quack_codegen.add_instruction("call Int:plus", -1)
        elif (self.types[a] == "String"):
            quack_codegen.add_instruction("roll 1", 0)
            quack_codegen.add_instruction("call String:plus", -1)

        return a
    
    def sub(self, a, b):
        quack_codegen.add_instruction("roll 1", 0)
        quack_codegen.add_instruction("call Int:minus", -1)
        return a
        
    def mul(self, a, b):
        quack_codegen.add_instruction("call Int:times", -1)
        return a

    def div(self, a, b):
        quack_codegen.add_instruction("roll 1", 0)
        quack_codegen.add_instruction("call Int:divide", -1)
        return a

    def neg(self, num):
        quack_codegen.add_instruction("call Int:negate", 0)
        return num

    def call(self, callee, function):
        typ = self.types[callee]
        inst = "call " + typ + ":" + function
        quack_codegen.add_instruction(inst, 0)
        
    def number(self, val):
        self.types[val] = "Int"
        quack_codegen.add_instruction("const " + val, 1)
        return val

    def str_lit(self, text):
        quack_codegen.add_instruction("const " + text, 1)
        self.types[text] = "String"
        return text

    def lit_nothing(self, nothing="Nothing"):
        self.types["Nothing"] = "Nothing"
        quack_codegen.add_instruction("const Nothing", 1)
        return nothing

    def lit_true(self, true="true"):
        self.types["true"] = "Bool"
        quack_codegen.add_instruction("const true", 1)
        return true

    def lit_false(self, false="false"):
        self.types["false"] = "Bool"
        quack_codegen.add_instruction("const false", 1)
        return false 
    
    def var(self, name):
        try:
            quack_codegen.add_instruction("load " + name, 1)
            return quack_codegen.get_var(name)

        except KeyError:
            raise Exception("Variable not found: %s" % name)

quack_parser = Lark(quack_grammar, parser='lalr', transformer=QuackTransformer())
quack = quack_parser.parse

def main():
    arguments = vars(args)
    f_input = arguments["input"]
    f_output = arguments["output"]
    s = ""

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

    quack(s)

    quack_codegen.print_instructions(f_output)
        
if __name__ == '__main__':
    # test()
    main()
