import quack_middle as qm
from quack_visitor import ASTVisitor
from quack_tables import tables

class QuackInitializationCheck(ASTVisitor):

    def __init__(self):
        pass

    def VisitWhile(self, node: qm.WhileNode, init: set):
        node.condition.check_init(self, init)
        node.block.check_init(self, init.copy())

    def VisitIfStmt(self, node: qm.IfStmtNode, init: set):
        node.condition.check_init(self, init)
        block_copy = init.copy()
        node.block.check_init(self, block_copy)
        if node.otherwise is not None:
            otherwise_copy = init.copy()
            node.otherwise.check_init(self, otherwise_copy)
            new_vars = block_copy.intersection(otherwise_copy)
            for element in new_vars:
                init.add(element)

    def VisitAssignment(self, node: qm.AssignmentNode, init: set):
        if isinstance(node.right, qm.VariableNode):
            if node.left.var not in init:
                raise ValueError(f"{node.left.var} not initialized before use")

        else:
            node.right.check_init(self, init)

        init.add(node.left.var)

    def VisitCall(self, node: qm.CallNode, init: set):
        if isinstance(node.callee, qm.VariableNode):
            if node.callee.var not in init:
                raise ValueError(f"{node.callee.var} not initialized before use")

    def VisitUnary(self, node: qm.UnaryOpNode, init: set):
        if isinstance(node.child, qm.VariableNode):
            if node.child.var not in init:
                raise ValueError(f"{node.left.var} not initialized before use")

        else:
            node.child.check_init(self, init)

    def VisitBinary(self, node: qm.BinaryOpNode, init: set):
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

    def VisitComparison(self, node: qm.ComparisonNode, init: set):
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

    def VisitMethod(self, node: qm.MethodNode, init: set):
        with_formals = init
        for element in node.formals:
            with_formals.add(element.ident)

        node.block.check_init(self, with_formals)

    def VisitBody(self, node: qm.BodyNode, init: set):
        pass
        
initialization_check = QuackInitializationCheck()
