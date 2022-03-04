.class simpleint:Obj

.method $constructor
.local x,y
load x
const 1
store x
load y
load x
load x
roll 1
call Int:plus
store y
load y
call Int:print
return 0