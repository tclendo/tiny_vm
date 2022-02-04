class QuackCodeGen:
    """
    QuackCodeGen is our class that handles generating code, and
    can be injected into the transformer classes so that they
    may modify this codegen class.
    """

    def __init__(self):
        # instruction stream that will be dumped at the end
        self.vars = {}
        self.instructions = []
        self.pusharg = 0
        self.filename = ""

    def set_filename(self, name):
        self.filename = name
        
    def set_var(self, var, val):
        self.vars[var] = val
        
    def get_var(self, var):
        return self.vars[var]
    
    def add_instruction(self, instruction, arg):
        self.instructions.append(instruction)
        self.pusharg += arg

    def print_instructions(self, stream):
        if not stream:
            print(".class {}:Obj".format(self.filename))
            print()
            print(".method $constructor")
            print(f".local {','.join(self.vars.keys())}")
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
                f.write(".local {}".format(','.join(self.vars.keys())))
                f.write('\n')
                # print(f".local {','.join(self.vars.keys())}")
                for instruction in self.instructions:
                    f.write(instruction)
                    f.write('\n')

                while self.pusharg > 0:
                    f.write("pop\n")
                    self.pusharg -= 1

                f.write("return 0")

codegen = QuackCodeGen()
