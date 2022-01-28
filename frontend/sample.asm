.class Sample:Obj

.method $constructor
.local x
const 3
store x
load x
load x
call Int:times
store x
load x
call Int:print
pop
return 0