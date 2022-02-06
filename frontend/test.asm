.class test:Obj

.method $constructor
.local x,y,z,a,b
load x
const 3
store x
load y
load x
load x
call Int:times
store y
load z
const true
store z
load a
const "hello, world!"
store a
load y
call Int:print
load b
const "Ugh, "
load a
call String:plus
store b
pop
pop
pop
pop
pop
pop
return 0