from lark import Lark, Transformer, v_args

try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass

calc_grammar = """
?start: program

?program: stmt*

?stmt: lhs ":" ident "=" rhs ";" -> assign_var
| rhs ";" 

?ident: NAME

?lhs: NAME

?rhs: sum

?sum: product
| sum "+" product   -> add
| sum "-" product   -> sub

?product: atom
| product "*" atom  -> mul
| product "/" atom  -> div

?atom: NUMBER      -> number
| STRING -> str_lit
| "-" atom         -> neg
| NAME -> var
| "(" sum ")"

%import common.CNAME -> NAME
%import common.ESCAPED_STRING -> STRING
%import common.NUMBER

EOL: /\\n/

%import common.WS_INLINE
%ignore WS_INLINE
"""


@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg

    def __init__(self):
        self.vars = {}
        self.instructions = []

    def __del__(self):
        print(".class Sample:Obj")
        print()
        print(".method $constructor")
        print(f".local {','.join(self.vars.keys())}")
        for element in self.instructions:
            print(element)

        print("pop")
        print("return 0")

    def assign_var(self, name, typ, value):
        self.instructions.append("store " + name)
        # print("store", name)
        self.vars[name] = value
        # return value

    def str_lit(self, text):
        value = "const " + text
        self.instructions.append(value)
        # return str(text)

    def add(self, a, b):
        self.instructions.append("call Int:add")
        # print("call Int:add")
        # return a + b 
    
    def sub(self, a, b):
        self.instructions.append("roll 1")
        self.instructions.append("call Int:minus")
        # print("call Int:minus")
        # return a - b 
        
    def mul(self, a, b):
        self.instructions.append("call Int:times")
        # print("call Int:times")
        # return a * b 

    def div(self, a, b):
        self.instructions.append("roll 1")
        self.instructions.append("call Int:divide")
        # print("call Int:divide")
        # return a // b 

    def number(self, value):
        self.instructions.append("const " + value)
        # print("const ", value)
        # return int(value)

    def neg(self, num):
        self.instructions.append("call Int:negate")
        # print("call Int:negate")
        # return -num
        
    def var(self, name):
        try:
            self.vars[name]
            self.instructions.append("load " + name)
            # print("load ", name)
            # return self.vars[name]
        except KeyError:
            raise Exception("Variable not found: %s" % name)


calc_parser = Lark(calc_grammar, parser='lalr', transformer=CalculateTree())
calc = calc_parser.parse


def main():
    s = ""

    while True:
        try:
            s += input()
        except EOFError:
            break;

    calc(s)
    # print(result)
          
def test():
    print(calc("a = 1+2"))
    print(calc("1+a*-3"))


if __name__ == '__main__':
    # test()
    main()
