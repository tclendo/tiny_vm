from class_map import default_class_map

class Tables():
    '''
    Keep track of all the default types, classes, and methods.
    Also update data as tree traversals occur.
    '''
    def __init__(self):
        # dictionary for variable types
        self.variables = {}
        self.arguments = {}
        # dictionary for objects and their methods
        self.objects = default_class_map
        self.using_methods = []
        # current object for type checking and updating
        # the class hierarchy information for user-added
        # classes
        self.current_object = None

        self.mainfilename = ""

    def set_main(self, name):
        self.mainfilename = name
        self.variables[self.mainfilename] = {}
        self.arguments[self.mainfilename] = {}
        self.current_object = self.mainfilename
        
    def set_current_object(self, name: str):
        self.current_object = name
        if name not in self.variables.keys():
            self.variables[name] = {}
        if name not in self.arguments.keys():
            self.arguments[name] = {}

    def set_type(self, item, typ):
        self.variables[self.current_object][item] = typ
        
    def get_type(self, item):
        try:
            return self.variables[self.current_object][item]

        except:
            raise NameError(f"In class \"{self.current_object}\": Variable \"{item}\" not found in table.")

    def get_variables(self):
        return self.variables[self.current_object].keys()

    def get_arguments(self):
        return self.arguments[self.current_object].keys()

    def add_argument(self, arg, typ):
        self.arguments[self.current_object][arg] = typ
    
    def set_variables(self, var_dict: dict):
        for element in var_dict.keys():
            self.variables[element] = var_dict[element]

    def get_variable_list(self) -> list:
        # used for codegen to generate .local{variables}
        return ([x for x in self.variables.keys()])

    def add_object(self, name: str, ext: str):
        # when adding an object, we need to copy everything over
        # from the class it extends in the same order as well
        if name not in self.objects.keys():
            self.using_methods.append(name)

        self.objects[name] = {
            "superclass": ext,
            "field_list": set(self.objects[ext]["field_list"]),
            "method_returns": self.objects[ext]["method_returns"],
            "method_args": self.objects[ext]["method_args"]}

        # also add this class to the variable namespace
        # dictionary
        self.variables[name] = {}

    def add_method(self, name: str, formals: list, typ: str):
        self.objects[self.current_object]["method_returns"][name] = typ
        self.objects[self.current_object]["method_args"][name] = formals

    def get_signature(self, typ, func):
        try:
            return self.objects[typ]["method_returns"][func]

        except:
            raise KeyError(f"{typ}:{func} not defined")

    def check_parameters(self, typ, params: list, func):
        size = len(params)
        db_args = self.objects[typ]["method_args"][func]
        if size == len(db_args):
            for i in range(0, size):
                if params[i] != db_args[i]:
                    raise TypeError(f"Parameter types differ: {params[i]} : {db_args[i]}")
        else:
            # If it's 0, it's not specified, so compiler doesn't know
            if len(db_args) != 0:
                raise ValueError(f"Incorrect parameter amounts: was {size} expected {len(db_args)}")

    def set_arguments(self, clas, func, params):
        self.params[clas][func] = params

    def get_parameters(self, clas, func):
        return self.objects[clas]["method_args"][func]

    def set_field(self, field):
        self.objects[self.current_object]["field_list"].add(field)

    def get_fields(self, clas):
        return self.objects[clas]["field_list"]
                              
    def check_binop(self, l_type, r_type, op):
        method = None
        if op == "+":
            method = "plus"
        elif op == "-":
            method = "minus"
        elif op == "*":
            method = "times"
        elif op == "/":
            method = "divide"
        elif op == "==":
            method = "equals"
        elif op == "!=":
            # same arg types, so it's fine
            method = "equals"
        elif op == ">":
            method = "greater"
        elif op == ">=":
            method = "greater_eq"
        elif op == "<":
            method = "less"
        elif op == "<=":
            method = "less_eq"
        else:
            raise ValueError("No binary operation exists for this")

        args = self.objects[l_type]["method_args"][method]
        if len(args) != 0:
            # there's only 1 argument, so see if the types are equal
            if r_type != args[0]:
                raise TypeError(f"Parameter types differ: {r_type} : {args[0]}")
            
            
    def get_class_map(self):
        return self.objects
        
    def get_common_class(self, first, second):
        f = first
        s = second
        while f != s:
            # get the ancestor class for each
            f_anc = self.objects[f]["superclass"]
            s_anc = self.objects[s]["superclass"]
            if f_anc == s:
                return s
            elif s_anc == f:
                return f
            f = f_anc
            s = s_anc

            # i don't think this is needed, but just in case
            if f == "Obj":
                return f
            if s == "Obj":
                return s

        return f
            
tables = Tables()
