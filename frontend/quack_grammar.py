quack_grammar = """
?start: program

?program: stmt
| program stmt -> prog

?stmt: assignment ";"
| r_expr ";" 
| "while" condition block
| "if" condition block elifs? else?

?elifs: elif
| elifs elif

?elif: "elif" condition block

?else: "else" block

?type: IDENT

?assignment: l_expr ":" type "=" r_expr -> assign_var_typ
| l_expr "=" r_expr -> assign_var

?block: "{" program "}"

?condition: r_expr

?l_expr: IDENT -> var

?params: l_expr
| params "," l_expr -> parameters

?r_expr: or
| r_expr "." IDENT "(" params? ")" -> call

?or: and
| or "or" and -> or_op

?and: equality
| and "and" equality -> and_op

?equality: comparison
| equality "==" comparison -> equal_compare
| equality "!=" comparison -> notequal_compare

?comparison: sum
| comparison ">" sum -> greater_than
| comparison ">=" sum -> greater_than_eq
| comparison "<" sum -> less_than
| comparison "<=" sum -> less_than_eq

?sum: product
| sum "+" product   -> add
| sum "-" product   -> sub

?product: atom
| product "*" atom  -> mul
| product "/" atom  -> div

?atom: NUMBER      -> number
| STRING -> str_lit
| "-" atom         -> neg
| l_expr
| "(" sum ")"
| bool
| "Nothing" -> lit_nothing

?bool: "true" -> lit_true
| "false" -> lit_false

%import common.ESCAPED_STRING -> STRING
%import common.NUMBER

EOL: /\\n/
IDENT: /[_a-zA-Z][_a-zA-A0-9]*/

%import common.WS_INLINE
%ignore WS_INLINE
%ignore EOL
"""
