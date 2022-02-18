default_class_map = {
    "Obj": {
        "superclass": "Obj",
        "field_list": {},
        "method_returns": {
            "$constructor": "Obj",
            "string": "String",
            "print": "Nothing",
            "equals": "Bool"
        },
        "method_args": {
            "$constructor": ["Obj"],
            "string": ["Obj"],
            "print": ["Obj"],
            "equals": ["Obj"]
        }
    },
    "Int": {
        "superclass": "Obj",
        "field_list": {},
        "method_returns": {
            "$constructor": "Int",
            "string": "String",
            "print": "Nothing",
            "equals": "Bool",
            "less": "Bool",
            "greater": "Bool",
            "less_eq": "Bool",
            "greater_eq": "Bool",
            "negate": "Int",
            "plus": "Int",
            "minus": "Int",
            "times": "Int",
            "divide": "Int",
        },
        "method_args": {
            "$constructor": [],
            "string": [],
            "print": [],
            "equals": ["Obj"],
            "less": ["Obj"],
            "greater": ["Obj"],
            "less_eq": ["Obj"],
            "greater_eq": ["Obj"],
            "negate": ["Int"],
            "plus": ["Int"],
            "minus": ["Int"],
            "times": ["Int"],
            "divide": ["Int"],
        }
    },
    "Bool": {
        "superclass": "Obj",
        "field_list": {},
        "method_returns": {
            "$constructor": "Bool",
            "string": "String",
            "print": "Nothing",
            "equals": "Bool",
            "negate": "Bool"
        },
        "method_args": {
            "$constructor": [],
            "string": [],
            "print": [],
            "equals": ["Obj"],
            "negate": ["Bool"]
        }
    },
    "String": {
        "superclass": "Obj",
        "field_list": {},
        "method_returns": {
            "$constructor": "String",
            "string": "String",
            "print": "Nothing",
            "equals": "Bool",
            "less": "Bool",
            "plus": "String"
        },
        "method_args": {
            "$constructor": [],
            "string": [],
            "print": [],
            "equals": ["Obj"],
            "less": ["Obj"],
            "plus": ["String"]
        }
    },
    "Nothing" : {
        "superclass": "Obj",
        "field_list": {},
        "method_returns": {
            "$constructor": "Nothing",
            "string": "String",
            "print": "String",
            "equals": "String"
        },
        "method_args": {
            "$constructor": [],
            "string": [],
            "print": [],
            "equals": []
        }
    }
}
