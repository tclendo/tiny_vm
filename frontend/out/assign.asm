.class assign:Obj

.method $constructor
.local x
load x
const 1
store x
load x
call Int:print
load x
load x
const 1
call Int:plus
store x
load x
call Int:print
pop
pop
pop
pop
return 0