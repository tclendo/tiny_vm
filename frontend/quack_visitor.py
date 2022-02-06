import quack_middle
###
# Our AST Visitor pattern class
###

class ASTVisitor():
    def __init__(self):

    def visit_unary(self, node: UnaryOpNode):
        print("UnaryOpNode")

    def visit_binary(self, node: BinaryOpNode):
        print("BinaryOpNode")

    def visit_assignment(self, node: AssignmentNode):
        print("AssignmentNode")
        
    def visit_call(self, node: CallNode):
        print("CallNode")

    def visit_var(self, node: VariableNode):
        print("VariableNode")

    def visit_string(self, node: StringLiteralNode):
        print("StringLiteralNode")
        
    def visit_int(self, node: IntLiteralNode):
        print("IntLiteralNode")

    def visit_bool(self, node: BooleanLiteralNode):
        print("BooleanLiteralNode")

    def visit_nothing(self, node: NothingLiteralNode):
        print("NothingLiteralNode")
