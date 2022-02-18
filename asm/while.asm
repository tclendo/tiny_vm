.class while:Obj

.method $constructor
.local x,y
load x
const 10
store x
jump labelwhilecmp0
labelwhilebody1:
load y
const 0
store y
jump labelwhilecmp2
labelwhilebody3:
load y
load y
const 1
call Int:plus
store y
load y
call Nothing:print
pop
labelwhilecmp2:
load y
const 3
call Int:greater
jump_if labelwhilebody3
endlabelwhilecmp2:
load x
load x
const 1
roll 1
call Int:minus
store x
load x
call Nothing:print
pop
labelwhilecmp0:
load x
const 1
call Int:greater
jump_ifnot labelwhilebody1
endlabelwhilecmp0:
return 0