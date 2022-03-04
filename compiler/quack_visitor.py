###
# Our AST Visitor pattern class
###

class ASTVisitor():
    def __init__(self):
        raise NotImplementedError()

    def VisitStartNode(self, node):
        raise NotImplementedError()

    def VisitProgram(self, node):
        raise NotImplementedError()
        
    def VisitClasses(self, node):
        raise NotImplementedError()

    def VisitSignature(self, node):
        raise NotImplementedError()

    def VisitBody(self, node):
        raise NotImplementedError()

    def VisitMethods(self, node):
        raise NotImplementedError()

    def VisitMethod(self, node):
        raise NotImplementedError()

    def VisitFormal(self, node):
        raise NotImplementedError()

    def VisitFormal(self, node):
        raise NotImplementedError()

    def VisitClass(self, node):
        raise NotImplementedError()
        
    def VisitBlock(self, node):
        raise NotImplementedError()

    def VisitReturn(self, node):
        raise NotImplementedError()

    def VisitIfStmt(self, node):
        raise NotImplementedError()

    def VisitWhile(self, node):
        raise NotImplementedError()
        
    def VisitBinary(self, node):
        raise NotImplementedError()

    def VisitUnary(self, node):
        raise NotImplementedError()

    def VisitAssignment(self, node):
        raise NotImplementedError()
        
    def VisitComparison(self, node):
        raise NotImplementedError()
        
    def VisitCall(self, node):
        raise NotImplementedError()

    def VisitUnused(self, node):
        raise NotImplementedError()
        
    def VisitVar(self, node):
        raise NotImplementedError()
        
    def VisitField(self, node):
        raise NotImplementedError()

    def VisitString(self, node):
        raise NotImplementedError()
        
    def VisitInt(self, node):
        raise NotImplementedError()

    def VisitBool(self, node):
        raise NotImplementedError()

    def VisitNothing(self, node):
        raise NotImplementedError()
        
