from class_map import default_class_map

class Tables():
    '''
    Keep track of all the default types, classes, and methods.
    Also update data as tree traversals occur.
    '''
    def __init__(self):
        # dictionary for variable types
        self.variables = {}
        # dictionary for objects and their methods
        self.objects = default_class_map

    def set_type(self, item, typ):
        self.variables[item] = typ
        
    def get_type(self, item):
        try:
            return self.variables[item]

        except:
            raise NameError(f"Variable {item} not found in table.")

    def get_variables(self):
        return self.variables

    def set_variables(self, var_dict: dict):
        for element in var_dict.keys():
            self.variables[element] = var_dict[element]

    def get_variable_list(self) -> list:
        # used for codegen to generate .local{variables}
        return ([x for x in self.variables.keys()])

    def set_signature(self, func, typ):
        pass

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
