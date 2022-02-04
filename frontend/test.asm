.class test:Obj

.method $constructor
.local x,y,z,a,b
const 3
store x
load x
load x
call Int:times
store y
const true
store z
const "hello, world!"
store a
load y
call Int:print
const "Ugh, "
load a
roll 1
call String:plus
store b
pop
return 0