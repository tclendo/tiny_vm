import quack_middle as qm
from quack_visitor import ASTVisitor
from quack_tables import tables

class QuackInitializationCheck(ASTVisitor):

    def __init__(self):
        pass

    def VisitWhile(self, node: qm.WhileNode, init):
        node.condition.check_init(self, init)
        node.block.check_init(self, init.copy())

    def VisitIfStmt(self, node: qm.IfStmtNode, init):
        pass

    def VisitAssignment(self, node: qm.AssignmentNode, init):
        if isinstance(node.right, qm.VariableNode):
            if node.left.var not in init:
                raise ValueError(f"{node.left.var} not initialized before use")

        else:
            node.right.check_init(self, init)

        init[node.left.var] = True

    def VisitCall(self, node: qm.CallNode, init):
        if isinstance(node.callee, qm.VariableNode):
            if node.callee.var not in init:
                raise ValueError(f"{node.left.var} not initialized before use")

    def VisitUnary(self, node: qm.UnaryOpNode, init):
        if isinstance(node.child, qm.VariableNode):
            if node.left.var not in init:
                raise ValueError(f"{node.left.var} not initialized before use")

        else:
            node.child.check_init(self, init)

    def VisitBinary(self, node: qm.BinaryOpNode, init):
        if isinstance(node.left, qm.VariableNode):
            if node.left.var not in init:
                raise ValueError(f"{node.left.var} not initialized before use")

        else:
            node.left.check_init(self, init)

        if isinstance(node.right, qm.VariableNode):
            if node.right.var not in init:
                raise ValueError(f"{node.right.var} not initialized before use")

        else:
            node.right.check_init(self, init)

    def VisitComparison(self, node: qm.ComparisonNode, init):
        if isinstance(node.left, qm.VariableNode):
            if node.left.var not in init:
                raise ValueError(f"{node.left.var} not initialized before use")

        else:
            node.left.check_init(self, init)

        if isinstance(node.right, qm.VariableNode):
            if node.right.var not in init:
                raise ValueError(f"{node.right.var} not initialized before use")

        else:
            node.right.check_init(self, init)

initialization_check = QuackInitializationCheck()
