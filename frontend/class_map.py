default_class_map = {
    "Obj": {
        "superclass": "$",
        "field_list": {},
        "method_returns": {
            "$constructor": "Obj",
            "string": "String",
            "print": "Nothing",
            "equals": "Boolean"
        },
        "method_args": {
            "$constructor": [],
            "string": [],
            "print": [],
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
            "plus": "Int",
            "minus": "Int",
            "times": "Int",
            "divide": "Int",
            "negate": "Int",
            "equals": "Boolean",
            "more": "Boolean",
            "less": "Boolean",
            "atleast": "Boolean",
            "atmost": "Boolean"
        },
        "method_args": {
            "$constructor": ["TODO"],
            "string": [],
            "print": [],
            "plus": ["Int"],
            "minus": ["Int"],
            "times": ["Int"],
            "divide": ["Int"],
            "negate": [],
            "equals": ["Obj"],
            "less": ["Obj"],
            "more": ["Obj"],
            "atmost": ["Obj"],
            "atleast": ["Obj"]
        }
    },
    "Boolean": {
        "superclass": "Obj",
        "field_list": {},
        "method_returns": {
            "$constructor": "Boolean",
            "string": "String",
            "print": "Nothing",
            "equals": "Boolean",
            "negate": "Boolean"
        },
        "method_args": {
            "$constructor": [],
            "string": [],
            "print": [],
            "equals": ["Obj"],
            "negate": []
        }
    },
    "String": {
        "superclass": "Obj",
        "field_list": [],
        "method_returns": {
            "$constructor": "String",
            "string": "String",
            "print": "Nothing",
            "equals": "Boolean",
            "less": "Boolean",
            "more": "Boolean",
            "atleast": "Boolean",
            "atmost": "Boolean",
            "plus": "String"
        },
        "method_args": {
            "$constructor": [],
            "string": [],
            "print": [],
            "equals": ["Obj"],
            "less": ["Obj"],
            "more": ["Obj"],
            "atleast": ["Obj"],
            "atmost": ["Obj"],
            "plus": ["String"]
        }
    }
}
