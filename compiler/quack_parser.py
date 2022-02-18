from lark import Lark, Transformer, v_args
from quack_codegen import codegen

class Tables():
    '''
    This class holds information for builtin functions and classes
    It will also update information such as user-defined classes
    and methods as middle end tree passes occur.
    '''
    pass

class ASTNode():
    '''
    Abstract AST node representation
    '''
    pass

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
