.class iftest:Obj

.method $constructor
.local x,y
load x
const 4
store x
jump labelifcmp0
labelifbody1:
load y
const 1
store y
load y
call Int:print
pop
load x
const 10
store x
jump endlabelifcmp0
labelifcmp0:
load x
const 5
call Int:less
jump_if labelifbody1
labelelse2:
jump labelifcmp3
labelifbody4:
load y
const 5
store y
load x
const "hello"
store x
jump endlabelifcmp3
labelifcmp3:
load x
const 3
call Int:greater
jump_if labelifbody4
labelelse5:
load x
call Int:print
pop
endlabelifcmp3:
endlabelifcmp0:
load y
call Int:print
pop
load x
call Obj:print
pop
return 0