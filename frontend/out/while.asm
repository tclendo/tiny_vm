.class while:Obj

.method $constructor
.local x,z,y
load x
const 10
store x
load z
const 5
store z
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
call Int:print
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
load z
load z
const 1
roll 1
call Int:minus
store z
load x
call Int:print
pop
load z
call Int:print
pop
labelwhilecmp0:
load x
const 1
call Int:greater_eq
jump_ifnot labelwhilebody1
endlabelwhilecmp0:
return 0