.class Test:Obj
.field x
.method $constructor
.args x
    enter
    load $
    load_field $:x
    load x
    load x
    load $
    store_field $:x
    load $
    return 1
.method Number
.args num
    enter
    load $
    load_field $:x
    load num
    load num
    load $
    store_field $:x
    load $
    load_field $:x
    return 1
