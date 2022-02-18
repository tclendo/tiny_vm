from lark import Transformer, v_args
from quack_visitor import ASTVisitor
from quack_tables import tables
        
class ASTNode():
    '''
    Base class for all AST nodes
    '''

    def set_type(self, typ: str):
        raise NotImplementedError()
    
    def get_type(self):
        raise NotImplementedError()
    
    def check_type(self, visitor: ASTVisitor) -> str:
        raise NotImplementedError()
        
    def check_init(self, visitor: ASTVisitor, init: dict):
        raise NotImplementedError()
        
    def c_eval(self, visitor: ASTVisitor):
        raise NotImplementedError()

    def generate(self, visitor: ASTVisitor):
        raise NotImplementedError()
        
class StringLiteralNode(ASTNode):
    def __init__(self, val: str):
        self.val = val

    def get_type(self):
        return "String"
    
    def check_type(self, visitor: ASTVisitor):
        return self.get_type()

    def check_init(self, visitor: ASTVisitor, init: dict):
        pass

    def generate(self, visitor: ASTVisitor):
        return visitor.VisitString(self)

class IntLiteralNode(ASTNode):
    def __init__(self, val: int):
        self.val = val

    def get_type(self):
        return "Int"

    def check_type(self, visitor: ASTVisitor):
        return self.get_type()

    def check_init(self, visitor: ASTVisitor, init: dict):
        pass

    def generate(self, visitor: ASTVisitor):
        return visitor.VisitInt(self)

class NothingLiteralNode(ASTNode):
    def __init__(self, val = "Nothing"):
        self.val = val

    def get_type(self):
        return "Nothing"
    
    def check_type(self, visitor: ASTVisitor):
        return self.get_type()

    def check_init(self, visitor: ASTVisitor, init: dict):
        pass

    def generate(self, visitor: ASTVisitor):
        return visitor.VisitNothing(self)

class BooleanLiteralNode(ASTNode):
    def __init__(self, val: str):
        self.val = val

    def get_type(self):
        return "Bool"
    
    def check_type(self, visitor: ASTVisitor):
        return self.get_type()

    def check_init(self, visitor: ASTVisitor, init: dict):
        pass

    def generate(self, visitor: ASTVisitor):
        return visitor.VisitBool(self)

class VariableNode(ASTNode):
    def __init__(self, var: str):
        self.var = var
        self.typ = None
        
    def get_type(self):
        return self.typ
    
    def check_type(self, visitor: ASTVisitor):
        self.typ = tables.get_type(self.var)
        return self.typ

    def check_init(self, visitor: ASTVisitor, init: dict):
        pass

    def set_type(self, typ: str):
        tables.set_type(self.var, typ)
        
    def generate(self, visitor: ASTVisitor):
        return visitor.VisitVar(self)

class UnaryOpNode(ASTNode):
    def __init__(self, op: str, child: ASTNode):
        self.op = op
        self.child = child
        self.typ = None
        
    def get_type(self):
        return self.typ

    def check_type(self, visitor: ASTVisitor):
        self.typ = visitor.VisitUnary(self)
        return self.typ

    def check_init(self, visitor: ASTVisitor, init: dict):
        return visitor.VisitUnary(self, init)

    def c_eval(self, visitor, true_branch, false_branch):
        if self.op == '!':
            self.child.generate(visitor)
            visitor.add_jump_if_not(true_branch)

    def generate(self, visitor: ASTVisitor):
        self.child.generate(visitor)
        return visitor.VisitUnary(self)
        
class BinaryOpNode(ASTNode):
    def __init__(self, op: str, left: ASTNode, right: ASTNode):
        self.op = op
        self.left = left
        self.right = right
        self.typ = None

    def get_op(self):
        return self.op

    def get_type(self):
        return self.typ

    def check_type(self, visitor: ASTVisitor):
        self.typ = visitor.VisitBinary(self)
        return self.typ
    
    def check_init(self, visitor: ASTVisitor, init: dict):
        return visitor.VisitBinary(self, init)

    def generate(self, visitor: ASTVisitor):
        self.left.generate(visitor)
        self.right.generate(visitor)
        return visitor.VisitBinary(self)

class UnusedStmtNode(ASTNode):
    def __init__(self, statement: ASTNode):
        self.statement = statement
    
    def check_type(self, visitor: ASTVisitor):
        return self.statement.check_type(visitor)

    def check_init(self, visitor: ASTVisitor, init: dict):
        return self.statement.check_init(visitor, init)

    def generate(self, visitor: ASTVisitor):
        self.statement.generate(visitor)
        return visitor.VisitUnused(self)
        
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

        self.typ = None

    def get_type(self):
        return self.typ
    
    def check_type(self, visitor: ASTVisitor):
        self.typ = visitor.VisitCall(self)
        return self.typ

    def check_init(self, visitor: ASTVisitor, init: dict):
        return visitor.VisitCall(self, init)

    def generate(self, visitor: ASTVisitor):
        self.callee.generate(visitor)
        for element in self.params:
            element.generate(visitor)

        return visitor.VisitCall(self)
        
class AssignmentNode(ASTNode):
    def __init__(self, left: VariableNode, right: ASTNode,
                 typ: str = None):

        self.left = left
        self.right = right
        self.typ = typ
        tables.set_type(self.left.var, self.typ)
        
    def get_type(self):
        return self.typ

    def set_type(self, typ: str):
        self.typ = typ
    
    def check_type(self, visitor: ASTVisitor):
        return visitor.VisitAssignment(self)

    def check_init(self, visitor: ASTVisitor, init: dict):
        return visitor.VisitAssignment(self, init)

    def generate(self, visitor: ASTVisitor):
        self.left.generate(visitor)
        self.right.generate(visitor)
        return visitor.VisitAssignment(self)

class ComparisonNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode, op: str):
        self.left = left
        self.right = right
        self.op = op

    def c_eval(self, visitor, true_branch, false_branch):
        # generate short-circuit 'or' comparison
        if self.op == "||":
            self.left.generate(visitor)
            # jump to block if first one is true
            visitor.add_jump_if(true_branch)
            self.right.generate(visitor)
            # jump to block if second one is true
            visitor.add_jump_if(true_branch)

        # generate short-circuit 'and' comparison
        elif self.op == "&&":
            self.left.generate(visitor)
            # jump to end if first one is false
            visitor.add_jump_if_not(false_branch)
            self.right.generate(visitor)
            # jump to block if second is true
            visitor.add_jump_if(true_branch)

        # otherwise there's no short-circuiting required
        else:
            self.generate(visitor)
            visitor.add_jump_if(true_branch)
    
    def get_type(self):
        return "Bool"
    
    def check_type(self, visitor: ASTVisitor):
        return visitor.VisitComparison(self)
            
    def check_init(self, visitor: ASTVisitor, init: dict):
        return visitor.VisitComparison(self, init)

    def generate(self, visitor: ASTVisitor):
        self.left.generate(visitor)
        self.right.generate(visitor)
        return visitor.VisitComparison(self)

class IfStmtNode(ASTNode):
    def __init__(self, condition: ASTNode, block: ASTNode,
                 otherwise: ASTNode):

        self.condition = condition
        self.block = block
        self.otherwise = otherwise

    def check_type(self, visitor: ASTVisitor):
        return visitor.VisitIfStmt(self)

    def check_init(self, visitor: ASTVisitor, init: dict):
        return visitor.VisitIfStmt(self, init)

    def generate(self, visitor: ASTVisitor):
        return visitor.VisitIfStmt(self)
    
class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode,
                 block: ASTNode):

        self.condition = condition
        self.block = block

    def check_type(self, visitor: ASTVisitor):
        return visitor.VisitWhile(self)
        
    def check_init(self, visitor: ASTVisitor, init: dict):
        return visitor.VisitWhile(self, init)

    def generate(self, visitor: ASTVisitor):
        return visitor.VisitWhile(self)
                 
class BlockNode(ASTNode):
    def __init__(self, statements: ASTNode):
        self.statements = statements

    def check_type(self, visitor: ASTVisitor):
        self.statements.check_type(visitor)

    def check_init(self, visitor: ASTVisitor, init: dict):
        self.statements.check_init(visitor, init)
        
    def generate(self, visitor: ASTVisitor):
        self.statements.generate(visitor)

class ProgramNode(ASTNode):

    def __init__(self, program: ASTNode,
                 final: ASTNode):

        self.program = program
        self.final = final 

    def check_type(self, visitor: ASTVisitor):
        self.program.check_type(visitor)
        self.final.check_type(visitor)

    def check_init(self, visitor: ASTVisitor, init: dict):
        self.program.check_init(visitor, init)
        self.final.check_init(visitor, init)

    def generate(self, visitor: ASTVisitor):
        self.program.generate(visitor)
        self.final.generate(visitor)

@v_args(inline=True)    # Affects the signatures of the methods
class ASTBuilder(Transformer):

    def __init__(self):
        pass

    def prog(self, program, statement):
        return ProgramNode(program, statement)
        
    def block(self, statements):
        return BlockNode(statements)
    
    def assign_var_typ(self, name, typ, value):
        return AssignmentNode(name, value, typ)

    def assign_var(self, name, value):
        return AssignmentNode(name, value)

    def call(self, callee, function, params=[]):
        return CallNode(callee, function, params)

    def parameters(self, params, stmt):
        return [params, stmt]
    
    def whilestmt(self, comparison, block):
        return WhileNode(comparison, block)
    
    def ifstmt(self, condition, block, otherwise=None):
        return IfStmtNode(condition, block, otherwise)
    
    def unusedstmt(self, statement):
        return UnusedStmtNode(statement)
    
    def add(self, left, right):
        return BinaryOpNode("+", left, right)
    
    def sub(self, left, right):
        return BinaryOpNode("-", left, right)
        
    def mul(self, left, right):
        return BinaryOpNode("*", left, right)

    def div(self, left, right):
        return BinaryOpNode("/", left, right)

    def or_op(self, left, right):
        return ComparisonNode(left, right, "||")

    def and_op(self, left, right):
        return ComparisonNode(left, right, "&&")

    def not_op(self, expr):
        return UnaryOpNode("!", expr)

    def equal_compare(self, left, right):
        return ComparisonNode(left, right, "==")

    def notequal_compare(self, left, right):
        return ComparisonNode(left, right, "!=")

    def greater_than(self, left, right):
        return ComparisonNode(left, right, ">")

    def greater_than_eq(self, left, right):
        return ComparisonNode(left, right, ">=")

    def less_than(self, left, right):
        return ComparisonNode(left, right, "<")

    def less_than_eq(self, left, right):
        return ComparisonNode(left, right, "<=")
    
    def neg(self, expr):
        return UnaryOpNode("-", expr)
        
    def var(self, name):
        return VariableNode(name)

    def number(self, val):
        return IntLiteralNode(val)

    def str_lit(self, text):
        return StringLiteralNode(text)

    def lit_nothing(self, nothing):
        return NothingLiteralNode()

    def lit_true(self, true="true"):
        return BooleanLiteralNode(true)

    def lit_false(self, false="false"):
        return BooleanLiteralNode(false)
