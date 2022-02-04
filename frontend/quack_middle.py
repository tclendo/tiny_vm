from lark import Transformer, v_args
from quack_codegen import codegen

class Tables():
    '''
    '''
    pass

class ASTNode():
    '''
    '''
    pass

@v_args(inline=True)    # Affects the signatures of the methods
class QuackTransformer(Transformer):
    from operator import add, sub, mul, truediv as div, neg

    def __init__(self):
        # dictionary of all the elements and their types
        self.types = {}

    def assign_var(self, name, typ, value):
        codegen.add_instruction("store " + name, -1)
        self.types[name] = typ
        codegen.set_var(name, value)
        return name 

    def add(self, a, b):
        if (self.types[a] == "Int"):
            codegen.add_instruction("call Int:plus", -1)
        elif (self.types[a] == "String"):
            codegen.add_instruction("roll 1", 0)
            codegen.add_instruction("call String:plus", -1)

        return a
    
    def sub(self, a, b):
        codegen.add_instruction("roll 1", 0)
        codegen.add_instruction("call Int:minus", -1)
        return a
        
    def mul(self, a, b):
        codegen.add_instruction("call Int:times", -1)
        return a

    def div(self, a, b):
        codegen.add_instruction("roll 1", 0)
        codegen.add_instruction("call Int:divide", -1)
        return a

    def neg(self, num):
        codegen.add_instruction("call Int:negate", 0)
        return num

    def call(self, callee, function):
        typ = self.types[callee]
        inst = "call " + typ + ":" + function
        codegen.add_instruction(inst, 0)
        
    def number(self, val):
        self.types[val] = "Int"
        codegen.add_instruction("const " + val, 1)
        return val

    def str_lit(self, text):
        codegen.add_instruction("const " + text, 1)
        self.types[text] = "String"
        return text

    def lit_nothing(self, nothing="Nothing"):
        self.types["Nothing"] = "Nothing"
        codegen.add_instruction("const Nothing", 1)
        return nothing

    def lit_true(self, true="true"):
        self.types["true"] = "Bool"
        codegen.add_instruction("const true", 1)
        return true

    def lit_false(self, false="false"):
        self.types["false"] = "Bool"
        codegen.add_instruction("const false", 1)
        return false 
    
    def var(self, name):
        try:
            codegen.add_instruction("load " + name, 1)
            return codegen.get_var(name)

        except KeyError:
            raise Exception("Variable not found: %s" % name)


