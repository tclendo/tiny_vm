import quack_middle as qm
from quack_visitor import ASTVisitor
from quack_tables import tables

class QuackCodeGen(ASTVisitor):
    """
    QuackCodeGen is our class that handles generating code, and
    can be injected into the transformer classes so that they
    may modify this codegen class.
    """

    def __init__(self):
        # instruction stream that will be dumped at the end
        self.instructions = {}
        self.returnargs = 0
        self.filename = tables.mainfilename
        self.settab = False
        self.label = 0
        self.is_construct = False

    # TODO: Modularize walks for ASTVisitor
    # the codegen class will always generate
    # code when it walks the tree.
    
    def set_filename(self, name):
        self.filename = name
        
    def add_instruction(self, instruction):
        # add instruction to proper container based on object
        if tables.current_object in self.instructions.keys():
            if self.settab:
                self.instructions[tables.current_object].append("    ")

            self.instructions[tables.current_object].append(instruction)

        else:
            if self.settab:
                self.instructions[tables.current_object] = ["    "]
                self.instructions[tables.current_object].append(instruction)

            else:
                self.instructions[tables.current_object] = [instruction]

        self.instructions[tables.current_object].append("\n")

    def create_label(self, prefix):
        label = "label" + prefix + str(self.label)
        self.label += 1
        return label

    def add_label(self, label):
        self.settab = False
        self.add_instruction(f"{label}:")
        self.settab = True

    def add_jump(self, label):
        self.add_instruction(f"jump {label}")
        
    def add_jump_if(self, label):
        self.add_instruction(f"jump_if {label}")
        
    def add_jump_if_not(self, label):
        self.add_instruction(f"jump_ifnot {label}")

    def print_instructions(self, stream):
        if not stream:
            for obj in self.instructions:
                for instruction in self.instructions[obj]:
                    print(instruction)

        else:
            for obj in self.instructions:
                filename = "asm/" + obj + ".asm"
                with open(filename, 'w') as f:
                    for instruction in self.instructions[obj]:
                        f.write(instruction)


### These methods are for recursively generating code
### from the ASTNodes
    def VisitStartNode(self, node: qm.StartNode):
        # create all of the different classes
        if node.classes != None:
            node.classes.generate(self)

        tables.set_current_object(tables.mainfilename)
        # create the constructor for our global program
        self.settab = False
        self.add_instruction(f".class {tables.mainfilename}:Obj")
        self.add_instruction(".method $constructor")
        self.add_instruction(".local {}".format(','.join(tables.get_variables())))
        self.settab = True
        self.add_instruction("enter")

        # generate the whole program
        node.program.generate(self)
        self.add_instruction("return 0")

    def VisitSignature(self, node: qm.SignatureNode):
        # generate class name
        self.settab = False
        self.add_instruction(f".class {node.name}:{node.ext}")

        # generate field declarations for the class
        if tables.get_fields(node.name) != {}:
            for element in tables.get_fields(node.name):
                self.add_instruction(f".field {element}")

        self.add_instruction(f".method $constructor")
        self.is_construct = True

        # generate the formal arguments
        if node.formals != []:
            x = [form.ident for form in node.formals]
            self.returnargs = len(x)
            self.add_instruction(".args {}".format(",".join(x)))

        # generate local variable declarations
        args = tables.get_arguments()
        variables = tables.get_variables()
        locs = []
        for element in variables:
            if element not in args:
                locs.append(element)

        if locs != []:
            self.add_instruction(".local {}".format(','.join(locs)))
            
        self.settab = True

    def VisitConstruct(self, node: qm.ConstructNode):
        self.add_instruction(f"new {node.ident}")
        self.add_instruction(f"call {node.ident}:$constructor")
        
    def VisitField(self, node: qm.FieldNode):
        if node.left == "this":
            self.add_instruction("load $")
            self.add_instruction(f"load_field $:{node.ident}")
        else:
            self.add_instruction(f"load_field {node.left.get_type()}:{node.ident}")

    def VisitBody(self, node: qm.BodyNode):
        self.add_instruction("enter")
        # generate constructor program
        node.program.generate(self)
        if self.is_construct:
            self.add_instruction("load $")
            self.is_construct = False
        self.add_instruction(f"return {self.returnargs}")
        self.returnargs = 0

        # generate the methods
        node.methods.generate(self)

    def VisitMethod(self, node: qm.MethodNode):
        # add the method name
        self.settab = False
        self.add_instruction(f".method {node.ident}")
        # add the method args
        if node.formals != []:
            x = [form.ident for form in node.formals]
            self.returnargs = len(x)
            self.add_instruction(".args {}".format(",".join(x)))

        args = tables.get_arguments()
        variables = tables.get_variables()
        locs = []
        for element in variables:
            if element not in args:
                locs.append(element)

        if locs != []:
            self.add_instruction(".local {}".format(','.join(locs)))
            
        # enter the function
        self.settab = True
        self.add_instruction("enter")

        # generate the block
        node.block.generate(self)
        self.add_instruction(f"return {self.returnargs}")
        self.returnargs = 0

    def VisitIfStmt(self, node: qm.IfStmtNode):
        # first, compare for the if node
        compare = self.create_label("ifcmp")
        self.add_jump(compare)
        body = self.create_label("ifbody")
        self.add_label(body)
        node.block.generate(self)
        end = "end" + compare
        self.add_jump(end)
        self.add_label(compare)
        if node.otherwise is None:
            node.condition.c_eval(self, body, end)
        
        # if there is an else node, jump to the else start
        else:
            els = self.create_label("else")
            node.condition.c_eval(self, body, els)
            self.add_label(els)
            node.otherwise.generate(self)

        # end of the if statement
        self.add_label(end)
        
    def VisitWhile(self, node: qm.WhileNode):
        # make the label
        compare = self.create_label("whilecmp")
        # generate a branch to the label
        self.add_jump(compare)
        # create the label for the while body
        body = self.create_label("whilebody")
        # generate the label
        self.add_label(body)
        # generate the block
        end = "end" + compare
        node.block.generate(self)
        # generate the label
        self.add_label(compare)
        # generate the condition
        node.condition.c_eval(self, body, end)
        # generate the end label
        self.add_label(end)
        
    def VisitBinary(self, node: qm.BinaryOpNode):
        if node.op == '-':
            self.add_instruction(f"roll 1")
            self.add_instruction(f"call {node.get_type()}:minus")
        elif node.op == '/':
            self.add_instruction(f"roll 1")
            self.add_instruction(f"call {node.get_type()}:divide")

        elif node.op == '+':
            self.add_instruction(f"roll 1")
            self.add_instruction(f"call {node.get_type()}:plus")

        elif node.op == '*':
            self.add_instruction(f"roll 1")
            self.add_instruction(f"call {node.get_type()}:times")

    def VisitUnary(self, node: qm.UnaryOpNode):
        if node.op == '-':
            self.add_instruction(f"call {node.get_type()}:negate")

    def VisitReturn(self, node: qm.ReturnStmtNode):
        node.statement.generate(self)
        
    def VisitAssignment(self, node: qm.AssignmentNode):
        if isinstance(node.left, qm.VariableNode):
            node.left.generate(self)
            node.right.generate(self)
            self.add_instruction(f"store {node.left.var}")
        else:
            node.right.generate(self)
            self.add_instruction(f"load $")
            self.add_instruction(f"store_field $:{node.left.ident}")

    def VisitComparison(self, node: qm.ComparisonNode):
        if node.op == '==':
            self.add_instruction(f"call {node.left.get_type()}:equals")

        elif node.op == '!=':
            self.add_instruction(f"call {node.left.get_type()}:equals")
            self.add_instruction(f"call Bool:negate")

        # since the machine is stack-oriented, we can either roll the 2 values
        # into their proper place for comparison, or we can just invert their
        # boolean operations. Since 1 > 2 will have 2 as the reciever object
        # on the stack, it will actually perform 2 > 1 if we do not also
        # invert the operation
        elif node.op == ">":
            self.add_instruction(f"call {node.left.get_type()}:less")

        elif node.op == ">=":
            self.add_instruction(f"call {node.left.get_type()}:less_eq")
            
        elif node.op == "<":
            self.add_instruction(f"call {node.left.get_type()}:greater")

        elif node.op == "<=":
            self.add_instruction(f"call {node.left.get_type()}:greater_eq")

        elif node.op == "||":
            node.c_eval(self)
        
    def VisitCall(self, node: qm.CallNode):
        typ = node.callee.get_type()
        func = node.function

        # check arguments and roll properly so that the object is on the top
        # of the stack.
        if tables.get_parameters(typ, func) == []:
            self.add_instruction(f"call {node.callee.get_type()}:{node.function}")

        else:
            self.add_instruction(f"roll {len(tables.get_parameters(typ, func))}")
            self.add_instruction(f"call {node.callee.get_type()}:{node.function}")

    def VisitUnused(self, node: qm.UnusedStmtNode):
        # an unused stmt just needs to pop an item off
        # the stack
        # OKAY APPARENTLY WE DON'T ???
        # self.add_instruction("pop")
        pass

    def VisitVar(self, node: qm.VariableNode):
        self.add_instruction(f"load {node.var}")

    def VisitString(self, node: qm.StringLiteralNode):
        self.add_instruction(f"const {node.val}")
        
    def VisitInt(self, node: qm.IntLiteralNode):
        self.add_instruction(f"const {node.val}")

    def VisitBool(self, node: qm.BooleanLiteralNode):
        self.add_instruction(f"const {node.val}")

    def VisitNothing(self, node: qm.NothingLiteralNode):
        self.add_instruction(f"const {node.val}")

codegen = QuackCodeGen()
