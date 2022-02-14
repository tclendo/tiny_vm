from quack_middle import tables, ASTVisitor, ASTNode

class QuackCodeGen(ASTVisitor):
    """
    QuackCodeGen is our class that handles generating code, and
    can be injected into the transformer classes so that they
    may modify this codegen class.
    """

    def __init__(self, tables):
        # instruction stream that will be dumped at the end
        self.tables = tables
        self.instructions = []
        self.pusharg = 0
        self.filename = ""
        self.label = 0

    # TODO: Modularize walks for ASTVisitor
    # the codegen class will always generate
    # code when it walks the tree.
    
    def set_filename(self, name):
        self.filename = name
        
    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def create_label(self, prefix):
        label = "label" + prefix + str(self.label)
        self.label += 1
        return label

    def add_label(self, label):
        self.add_instruction(f"{label}:")

    def add_jump(self, label):
        self.add_instruction(f"jump {label}")
        
    def add_jump_if(self, label):
        self.add_instruction(f"jump_if {label}")
        
    def add_jump_if_not(self, label):
        self.add_instruction(f"jump_ifnot {label}")

    def print_instructions(self, stream):
        if not stream:
            print(".class {}:Obj".format(self.filename))
            print()
            print(".method $constructor")
            print(".local {}".format(','.join(self.tables.get_variables())))
            for element in self.instructions:
                print(element)

            while self.pusharg > 0:
                print("pop")
                self.pusharg -= 1

            print("return 0\n")

        else:
            with open(stream, 'w') as f:
                f.write(".class {}:Obj\n".format(self.filename))
                f.write("\n")
                f.write(".method $constructor\n")
                f.write(".local {}".format(','.join(self.tables.get_variables())))
                f.write('\n')
                # print(f".local {','.join(self.vars.keys())}")
                for instruction in self.instructions:
                    f.write(instruction)
                    f.write('\n')

                while self.pusharg > 0:
                    f.write("pop\n")
                    self.pusharg -= 1

                f.write("return 0")


### These methods are for recursively generating code
### from the ASTNodes 

    def generate_unary(self, node):
        if node.op == '-':
            self.add_instruction(f"call {node.get_type()}:negate")

    def generate_while(self, node):
        compare = self.create_label("whilecmp")
        self.add_jump(compare)
        body = self.create_label("whilebody")
        self.add_label(body)
        node.block.generate(self)
        self.add_label(compare)
        node.condition.generate(self)
        self.add_jump_if(body)
        self.add_label("end" + compare)
        
    def generate_binary(self, node):
        if node.op == '-':
            self.add_instruction(f"roll 1")
            self.add_instruction(f"call {node.get_type()}:minus")
        elif node.op == '/':
            self.add_instruction(f"roll 1")
            self.add_instruction(f"call {node.get_type()}:divide")

        elif node.op == '+':
            self.add_instruction(f"call {node.get_type()}:plus")

        elif node.op == '*':
            self.add_instruction(f"call {node.get_type()}:times")

            
    def generate_assignment(self, node):
        self.add_instruction(f"store {node.left.var}")

    def generate_comparison(self, node):
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
        
    def generate_call(self, node):
        self.add_instruction(f"call {node.get_type()}:{node.function}")

    def generate_unused(self, node):
        # an unused stmt just needs to pop an item off
        # the stack
        self.add_instruction("pop")
        
    def generate_var(self, node):
        self.add_instruction(f"load {node.var}")

    def generate_string(self, node):
        self.add_instruction(f"const {node.val}")
        
    def generate_int(self, node):
        self.add_instruction(f"const {node.val}")

    def generate_bool(self, node):
        self.add_instruction(f"const {node.val}")

    def generate_nothing(self, node):
        self.add_instruction(f"const {node.val}")

codegen = QuackCodeGen(tables)
