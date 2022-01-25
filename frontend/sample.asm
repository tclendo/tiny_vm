.class Sample:Obj

.method $constructor
.local x,y,z
const 3
store x
load x
load x
call Int:times
store y
load y
const 5
roll 1
call Int:minus
store z
pop
return 0
