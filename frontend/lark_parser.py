from lark import Lark, Transformer, v_args

try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass

calc_grammar = """
?start: program

?program: stmt*

?stmt: assignment
| r_expr ";" 

?assignment: l_expr ":" type "=" r_expr ";" -> assign_var

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
"""


@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg

    def __init__(self):
        # dictionary of all the variables and their values
        self.vars = {}
        # dictionary of all the elements and their types
        self.types = {}

        # value to represent if the last instruction pushed a value
        # onto the stack
        self.pusharg = 0
        # instruction stream that will be dumped at the end
        self.instructions = []

    def __del__(self):
        print(".class Sample:Obj")
        print()
        print(".method $constructor")
        print(f".local {','.join(self.vars.keys())}")
        for element in self.instructions:
            print(element)

        while self.pusharg > 0:
            print("pop")
            self.pusharg -= 1

        print("return 0")

    def assign_var(self, name, typ, value):
        self.instructions.append("store " + name)
        self.types[name] = typ
        self.vars[name] = value
        self.pusharg -= 1
        return name 

    def str_lit(self, text):
        value = "const " + text
        self.types[text] = "String"
        self.instructions.append(value)
        self.pusharg += 1
        return text

    def add(self, a, b):
        if (self.types[a] == "Int"):
            self.instructions.append("call Int:plus")
        elif (self.types[a] == "String"):
            self.instructions.append("roll 1")
            self.instructions.append("call String:plus")

        self.pusharg -= 1
        return a
    
    def sub(self, a, b):
        self.instructions.append("roll 1")
        self.instructions.append("call Int:minus")
        self.pusharg -= 1
        return a
        
    def mul(self, a, b):
        self.instructions.append("call Int:times")
        self.pusharg -= 1
        return a

    def div(self, a, b):
        self.instructions.append("roll 1")
        self.instructions.append("call Int:divide")
        self.pusharg -= 1
        return a

    def neg(self, num):
        self.instructions.append("call Int:negate")
        return num

    def call(self, callee, function):
        typ = self.types[callee]
        inst = "call " + typ + ":" + function
        self.instructions.append(inst)
        
    def number(self, value):
        self.types[value] = "Int"
        self.instructions.append("const " + value)
        self.pusharg += 1
        return value

    def var(self, name):
        try:
            self.vars[name]
            self.instructions.append("load " + name)
            self.pusharg += 1
            return self.vars[name]

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
          
if __name__ == '__main__':
    # test()
    main()
