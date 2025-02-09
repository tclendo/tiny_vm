import quack_middle as qm
from quack_visitor import ASTVisitor
from quack_tables import tables

class QuackTypeChecker(ASTVisitor):

    def __init__(self):
        self.modified: set = set({})
        self.previous: set = set({})

    def reset(self):
        self.previous = self.modified.copy()
        self.modified.clear()

    def did_modify(self, modified):
        self.modified.add(modified) 

    def made_changes(self):
        return self.modified != self.previous
        
    def VisitWhile(self, node: qm.WhileNode):
        condition_type = node.condition.check_type(self)
        if condition_type != "Bool":
            raise TypeError(f"{condition_type} is not 'Bool'")

        node.block.check_type(self)

        return "Obj"

    def VisitIfStmt(self, node: qm.IfStmtNode):
        condition_type = node.condition.check_type(self)
        if condition_type != "Bool":
            raise TypeError(f"{condition_type} is not 'Bool'")

        if node.otherwise is not None:
            node.otherwise.check_type(self)

        node.block.check_type(self)
        
        return "Obj"

    def VisitComparison(self, node: qm.ComparisonNode):
        l_type = node.left.check_type(self)
        r_type = node.right.check_type(self)
        if node.op == "||":
            if l_type != "Bool":
                raise TypeError(f"{l_type} is not 'Bool'")
            if r_type != "Bool":
                raise TypeError(f"{r_type} is not 'Bool'")

        elif node.op == "&&":
            if l_type != "Bool":
                raise TypeError(f"{l_type} is not 'Bool'")
            if r_type != "Bool":
                raise TypeError(f"{r_type} is not 'Bool'")

        else:
            tables.check_binop(l_type, r_type, node.op)
            
        return "Bool"

    def VisitAssignment(self, node: qm.AssignmentNode):
        try:
            l_type = node.left.check_type(self)
        except NameError:
            l_type = node.typ
            node.left.set_type(l_type)

        r_type = node.right.check_type(self)

        # if l_type is none, the variable hasn't been
        # assigned a type yet. Let's do that here
        if l_type == None:
            self.did_modify(l_type)
            node.left.set_type(r_type)
            node.set_type(r_type)

        # if at any point the variable and the rhs
        # are different types, we find the most
        # specific common class
        elif l_type != r_type:
            self.did_modify(l_type)
            new_type = tables.get_common_class(l_type, r_type)
            node.left.set_type(new_type)
            return new_type
            
        return l_type

    def VisitCall(self, node: qm.CallNode):
        # We do various checks in the VisitCall method,
        # such as making sure the parameters are correct
        # but we will return the funtion signature

        # First, check that the callee type has this function
        # TODO: streamline error handling here?
        # This returns function signature, but will throw error
        # if the function doesn't exist for this class
        callee_type = node.callee.check_type(self)
        func_signature = tables.get_signature(callee_type, node.function)

        # then check parameter types are correct
        param_types = []
        for element in node.params:
            param_types.append(element.get_type())
            # param_types.append(tables.get_type(element))

        tables.check_parameters(callee_type, param_types, node.function)
        
        return func_signature
    
    def VisitBinary(self, node: qm.BinaryOpNode):
        l_type = node.left.check_type(self)
        r_type = node.right.check_type(self)
        # TODO: type checking here to traverse type tree
        tables.check_binop(l_type, r_type, node.op)

        node.typ = l_type
        return l_type

    def VisitUnary(self, node: qm.UnaryOpNode):
        child_type = node.child.check_type(self)
        if node.op == "!":
            if child_type != "Bool":
                raise TypeError(f"{child_type} is not 'Bool' for not comparison")

        node.typ = child_type
        return child_type

typechecker = QuackTypeChecker()

