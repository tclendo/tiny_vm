.class hw3:Obj

.method $constructor
.local x,y,z,a
load x
const 5
store x
load y
const "hello!"
store y
jump labelwhilecmp0
labelwhilebody1:
load y
call String:print
pop
load x
call Int:print
pop
load x
load x
const 1
roll 1
call Int:minus
store x
labelwhilecmp0:
load x
const 1
call Int:less
jump_if labelwhilebody1
endlabelwhilecmp0:
load x
call Int:print
pop
load z
const 10
store z
jump labelifcmp2
labelifbody3:
const "Z is the same as y!\n"
call String:print
pop
jump endlabelifcmp2
labelifcmp2:
load z
load y
call Int:equals
jump_if labelifbody3
labelelse4:
load a
const 10
store a
load a
call Int:print
pop
endlabelifcmp2:
load z
call Int:print
pop
return 0