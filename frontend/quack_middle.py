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
        # TODO: implement class hierarchy for builtins
        pass
                               
    def set_type(self, item, typ):
        self.variables[item] = typ
        
    def get_type(self, item):
        if item not in self.variables.keys():
            return "Obj" 

        return self.variables[item]

    def get_variables(self) -> list:
        return ([x for x in self.variables.keys()])

    def set_signature(self, func, typ):
        self.signatures[func] = typ

    def get_signature(self, func):
        if func not in self.signatures.keys():
            return "Obj" 

        return self.signatures[func]

tables = Tables()
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

    def generate_comparison(self, node):
        if node.op == '==':
            codegen.add_instruction(f"call {node.get_type()}:equals", 0)

        elif node.op == '!=':
            codegen.add_instruction(f"call {node.get_type()}:equals", 0)
            codegen.add_instruction(f"call Bool:negate", 0)
            
        
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
        # TODO: type checking here to traverse type tree
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
        # TODO: type should actually be the function return signature
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
            # print(f"Set {self.left.var} type: {self.typ}")
            tables.set_type(self.left.var, self.typ)

        else:
            tables.set_type(self.left.var, self.right.get_type())
            # print(f"Set {self.left.var} type: {tables.get_type(self.left.var)}")

    def r_eval(self):
        pass
        
    def get_type(self):
        return self.right.get_type()

    def generate(self, visitor: ASTVisitor):
        self.left.generate(visitor)
        self.right.generate(visitor)
        return visitor.generate_assignment(self)

class ComparisonNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode, op: str):
        self.left = left
        self.right = right
        self.op = op

    def r_eval(self):
        pass

    def get_type(self):
        return "Bool"

    def generate(self, visitor):
        pass

class BlockNode(ASTNode):
    def __init__(self, statements: ASTNode):
        self.statements = statements

    def r_eval(self):
        pass

    def get_type(self):
        return self.statements.get_type()

    def generate(self, visitor):
        self.statements.generate(visitor)

class ProgramNode(ASTNode):

    def __init__(self, program: ASTNode,
                 final: ASTNode):

        self.program = program
        self.final = final 

    def r_eval(self):
        pass

    def get_type(self):
        pass

    def generate(self, visitor):
        self.program.generate(visitor)
        self.final.generate(visitor)

@v_args(inline=True)    # Affects the signatures of the methods
class ASTBuilder(Transformer):
    from operator import add, sub, mul, truediv as div, neg

    def __init__(self):
        # dictionary of all the elements and their types
        pass

    def prog(self, program, statement):
        return ProgramNode(program, statement)
        
    def block(self, statements):
        return BlockNode(statements)
    
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

    def or_op(self, left, right):
        pass

    def and_op(self, left, right):
        pass

    def equal_compare(self, left, right):
        pass

    def notequal_compare(self, left, right):
        pass

    def greater_than(self, left, right):
        pass

    def greater_than_eq(self, left, right):
        pass

    def less_than(self, left, right):
        pass

    def less_than_eq(self, left, right):
        pass
    
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

    def lit_nothing(self, nothing):
        # print(f"{nothing}")
        return NothingLiteralNode()

    def lit_true(self, true="true"):
        # print(f"{true}")
        return BooleanLiteralNode(true)

    def lit_false(self, false="false"):
        # print(f"{false}")
        return BooleanLiteralNode(false)
