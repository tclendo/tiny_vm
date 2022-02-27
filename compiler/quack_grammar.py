quack_grammar = """
?start: classes? program

?classes: class
| classes class -> classes

?class: signature body -> clas

?signature: "class" IDENT "(" formals ")" -> signature
| "class" IDENT "(" formals ")" "extends" IDENT -> signature_ext

?formals: formal
| formals "," formal -> formals

?formal: IDENT ":" type -> formal

?body: program methods -> body

?methods: method
| methods method -> methods

?method: "def" IDENT "(" formals ")" ":" type block -> method

?program: stmt
| program stmt -> prog

?stmt: assignment ";"
| r_expr ";" -> unusedstmt 
| "while" condition block -> whilestmt
| "if" condition block otherwise? -> ifstmt

?otherwise: "else" block
| "elif" condition block otherwise? -> ifstmt

?type: IDENT

?assignment: l_expr ":" type "=" r_expr -> assign_var_typ
| l_expr "=" r_expr -> assign_var

?block: "{" program "}"

?condition: r_expr

?l_expr: IDENT -> var

?r_expr: not 

?params: l_expr
| params "," l_expr -> parameters

?not: or
| "not" comparison -> not_op

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

?product: access 
| product "*" atom  -> mul
| product "/" atom  -> div

?access: atom
| access "." IDENT -> field
| access "." IDENT "(" params? ")" -> call

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

EOL: /(\\n|\\r)/
IDENT: /[_a-zA-Z][_a-zA-A0-9]*/
COMMENT: "/*" /(.|\\n|\\r)+/ "*/"
| "//" /(.)+/ EOL

%import common.WS_INLINE
%ignore WS_INLINE
%ignore EOL
%ignore COMMENT
"""
