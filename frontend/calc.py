"""
Basic calculator
================

A simple example of a REPL calculator

This example shows how to write a basic calculator with variables.
"""
from lark import Lark, Transformer, v_args

try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass

calc_grammar = """
    ?start: sum
          | NAME "=" sum    -> assign_var

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div

    ?atom: NUMBER           -> number
         | "-" atom         -> neg
         | NAME             -> var
         | "(" sum ")"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
"""


@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg

    def __init__(self):
        print(".class Sample:Obj")
        print()
        print(".method $constructor")

    def __del__(self):
        print("pop")
        print("return 0")

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def add(self, first, second):
        print("call Int:add")
        return first + second
    
    def sub(self, first, second):
        print("call Int:minus")
        return first - second
        
    def mul(self, first, second):
        print("call Int:times")
        return first * second

    def div(self, first, second):
        print("call Int:divide")
        return first // second

    def number(self, value):
        print("const ", value)
        return int(value)

    def var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            raise Exception("Variable not found: %s" % name)


calc_parser = Lark(calc_grammar, parser='lalr', transformer=CalculateTree())
calc = calc_parser.parse


def main():
    s = input()
    result = calc(s)
    # extra code to verify our parser is working properly
    print("call String:print")
          
def test():
    print(calc("a = 1+2"))
    print(calc("1+a*-3"))


if __name__ == '__main__':
    # test()
    main()
