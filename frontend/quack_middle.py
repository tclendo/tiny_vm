from lark import Transformer, v_args
from quack_codegen import QuackCodeGen

class Tables():
    '''
    Keep track of all the default types, classes, and methods.
    Also update data as tree traversals occur.
    '''
    def __init__(self):
        # dictionary for variable types
        self.variables = {}
        # table for function signatures
        self.signatures = {}
        # dictionary for objects and their methods
        self.objects = {}

    def initialize_objects(self):
        self.objects["Obj"] = {"string",
                               "print",
                               "equals"}

        self.objects["String"] = self.objects["Obj"] | {
            "less", "plus"}

        self.objects["Bool"] = self.objects["Obj"]
        self.objects["Nothing"] = self.objects["Obj"]
        self.objects["Int"] = self.objects["Obj"] | {
            "negate", "plus", "minus", "times", "divide"}
                               
    def set_type(self, item, typ):
        self.variables[item] = typ
        
    def get_type(self, item):
        if item not in self.variables.keys():
            return None

        return self.variables[item]

    def get_variables(self) -> list:
        return ([x for x in self.variables.keys()])

    def set_signature(self, func, typ):
        self.signatures[func] = typ

    def get_signature(self, func):
        if func not in self.signatures.keys():
            return None

        return self.signatures[func]

tables = Tables()
tables.initialize_objects()
codegen = QuackCodeGen(tables)

###
# Our AST Visitor pattern class
###

class ASTVisitor():
    def __init__(self):
        pass

    def generate_unary(self, node):
        if node.op == '-':
            codegen.add_instruction(f"call {node.get_type()}:negate", 0)

    def generate_binary(self, node):
        if node.op == '-':
            codegen.add_instruction(f"call {node.get_type()}:minus", -1)
        elif node.op == '/':
            codegen.add_instruction(f"call {node.get_type()}:divide", -1)

        elif node.op == '+':
            codegen.add_instruction(f"call {node.get_type()}:plus", -1)

        elif node.op == '*':
            codegen.add_instruction(f"call {node.get_type()}:times", -1)

            
    def generate_assignment(self, node):
        codegen.add_instruction(f"store {node.left.var}", -1)

    def generate_call(self, node):
        codegen.add_instruction(f"call {node.get_type()}:{node.function}", 0)

    def generate_var(self, node):
        codegen.add_instruction(f"load {node.var}", 1)

    def generate_string(self, node):
        codegen.add_instruction(f"const {node.val}", 1)
        
    def generate_int(self, node):
        codegen.add_instruction(f"const {node.val}", 1)

    def generate_bool(self, node):
        codegen.add_instruction(f"const {node.val}", 1)

    def generate_nothing(self, node):
        codegen.add_instruction(f"const {node.val}", 1)
        
class ASTNode():
    '''
    Base class for all AST nodes
    '''
    def r_eval(self):
        raise NotImplementedError("Base class")

    def l_eval(self):
        raise NotImplementedError("Base class")
        
    def c_eval(self):
        raise NotImplementedError("Base class")

    def get_type(self):
        raise NotImplementedError("Base class")

    def generate(self, visitor):
        raise NotImplementedError("Base class")
        
class StringLiteralNode(ASTNode):
    def __init__(self, val: str):
        self.val = val

    def r_eval(self):
        return self.val

    def get_type(self):
        return "String"
    
    def generate(self, visitor: ASTVisitor):
        return visitor.generate_string(self)

class IntLiteralNode(ASTNode):
    def __init__(self, val: int):
        self.val = val

    def r_eval(self):
        return self.val

    def get_type(self):
        return "Int"

    def generate(self, visitor: ASTVisitor):
        return visitor.generate_int(self)

class NothingLiteralNode(ASTNode):
    def __init__(self, val = "Nothing"):
        self.val = val

    def r_eval(self):
        return self.val

    def get_type(self):
        return "Nothing"

    def generate(self, visitor: ASTVisitor):
        return visitor.generate_nothing(self)

class BooleanLiteralNode(ASTNode):
    def __init__(self, val: str):
        self.val = val

    def r_eval(self):
        return self.val

    def get_type(self):
        return "Bool"

    def generate(self, visitor: ASTVisitor):
        return visitor.generate_bool(self)

class VariableNode(ASTNode):
    def __init__(self, var: str):
        self.var = var

    def r_eval(self):
        return self.var
    
    def get_type(self):
        return tables.get_type(self.var)

    def generate(self, visitor: ASTVisitor):
        return visitor.generate_var(self)

class UnaryOpNode(ASTNode):
    def __init__(self, op: str, child: ASTNode):
        self.op = op
        self.child = child
        
    def r_eval(self):
        pass

    def get_type(self):
        return tables.get_type(self.child)

    def generate(self, visitor: ASTVisitor):
        self.child.generate(visitor)
        return visitor.generate_unary(self)
        
class BinaryOpNode(ASTNode):
    def __init__(self, op: str, left: ASTNode, right: ASTNode):
        self.op = op
        self.left = left
        self.right = right
    
    def r_eval(self):
        pass

    def get_type(self):
        l_type = self.left.get_type()
        r_type = self.right.get_type()
        if l_type != r_type:
            raise TypeError(f"{l_type} and {r_type} different types")

        return l_type
    
    def get_op(self):
        return self.op
    
    def generate(self, visitor: ASTVisitor):
        self.left.generate(visitor)
        self.right.generate(visitor)
        return visitor.generate_binary(self)

class CallNode(ASTNode):
    def __init__(self, callee: ASTNode,
                 function: str, params: list):

        self.callee = callee
        self.function = function
        self.params = []
        # flatten the params list
        for element in params:
            if type(element) == list:
                for item in element:
                    self.params.append(item)

            else:
                self.params.append(element)
                    
    def r_eval(self):
        pass

    def get_type(self):
        return self.callee.get_type()

    def generate(self, visitor: ASTVisitor):
        self.callee.generate(visitor)
        for element in self.params:
            element.generate(visitor)

        return visitor.generate_call(self)
        
class AssignmentNode(ASTNode):
    def __init__(self, left: VariableNode, right: ASTNode,
                 typ: str = None):

        self.left = left
        self.right = right
        self.typ = typ
        if self.typ is not None:
            print(f"Set {self.left.var} type: {self.typ}")
            tables.set_type(self.left.var, self.typ)

        else:
            tables.set_type(self.left.var, self.right.get_type())

    def r_eval(self):
        pass
        
    def get_type(self):
        return self.right.get_type()

    def generate(self, visitor: ASTVisitor):
        self.left.generate(visitor)
        self.right.generate(visitor)
        return visitor.generate_assignment(self)

class ProgramNode(ASTNode):

    def __init__(self, statements: ASTNode,
                 statement: ASTNode):
        self.statements = statements
        self.final = statement

    def r_eval(self):
        pass

    def get_type(self):
        pass

    def generate(self, visitor):
        self.statements.generate(visitor)
        self.final.generate(visitor)

quack_grammar = """
?start: program

?program: stmt 
| program stmt -> prog

?stmt: assignment ";"
| r_expr ";" 

?assignment: l_expr ":" type "=" r_expr -> assign_var_typ
| l_expr "=" r_expr -> assign_var

?type: IDENT

?l_expr: IDENT -> var

?r_expr: sum
| r_expr "." IDENT "(" params? ")" -> call

?params: l_expr
| params "," l_expr -> parameters

?sum: product
| sum "+" product   -> add
| sum "-" product   -> sub

?product: atom
| product "*" atom  -> mul
| product "/" atom  -> div

?atom: NUMBER      -> number
| STRING -> str_lit
| "-" atom         -> neg
| l_expr
| "(" sum ")"
| bool
| "Nothing" -> lit_nothing

?bool: "true" -> lit_true
| "false" -> lit_false

%import common.ESCAPED_STRING -> STRING
%import common.NUMBER

EOL: /\\n/
IDENT: /[_a-zA-Z][_a-zA-A0-9]*/

%import common.WS_INLINE
%ignore WS_INLINE
%ignore EOL
"""

@v_args(inline=True)    # Affects the signatures of the methods
class ASTBuilder(Transformer):
    from operator import add, sub, mul, truediv as div, neg

    def __init__(self):
        # dictionary of all the elements and their types
        self.types = {}

    def prog(self, program, statement):
        # print(f"{program} {statement}")
        return ProgramNode(program, statement)

    def assign_var_typ(self, name, typ, value):
        # print(f"{name}: {typ} = {value}")
        return AssignmentNode(name, value, typ)

    def assign_var(self, name, value):
        # print(f"{name} = {value}")
        return AssignmentNode(name, value)

    def call(self, callee, function, params=[]):
        # print(f"{callee}.{function}()")
        return CallNode(callee, function, params)

    def parameters(self, params, stmt):
        return [params, stmt]
    
    def add(self, left, right):
        # print(f"{left} + {right}")
        return BinaryOpNode("+", left, right)
    
    def sub(self, left, right):
        # print(f"{left} - {right}")
        return BinaryOpNode("-", left, right)
        
    def mul(self, left, right):
        # print(f"{left} * {right}")
        return BinaryOpNode("*", left, right)

    def div(self, left, right):
        # print(f"{left} / {right}")
        return BinaryOpNode("/", left, right)

    def neg(self, expr):
        # print(f"-{expr}")
        return UnaryOpNode("-", expr)
        
    def var(self, name):
        # print(f"{name}")
        return VariableNode(name)

    def number(self, val):
        # print(f"{val}")
        return IntLiteralNode(val)

    def str_lit(self, text):
        # print(f"{text}")
        return StringLiteralNode(text)

    def lit_nothing(self, nothing="Nothing"):
        # print(f"{nothing}")
        return NothingLiteralNode()

    def lit_true(self, true="true"):
        # print(f"{true}")
        return BooleanLiteralNode(true)

    def lit_false(self, false="false"):
        # print(f"{false}")
        return BooleanLiteralNode(false)
