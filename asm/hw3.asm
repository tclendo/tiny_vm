.class hw3:Obj

.method $constructor
.local x,y,temp,z,done
load x
const 5
store x
load y
const "hello!"
store y
jump labelwhilecmp0
labelwhilebody1:
load temp
const 3
store temp
jump labelwhilecmp2
labelwhilebody3:
load temp
call Int:print
pop
const "\n"
call String:print
pop
load x
call Int:print
pop
const "\n"
call String:print
pop
load x
load x
const 1
roll 1
call Int:minus
store x
load temp
load temp
const 1
call Int:plus
store temp
labelwhilecmp2:
load temp
const 0
call Int:equals
call Bool:negate
jump_ifnot endlabelwhilecmp2
load x
const 0
call Int:equals
call Bool:negate
jump_if labelwhilebody3
endlabelwhilecmp2:
labelwhilecmp0:
load x
const 1
call Int:less
jump_if labelwhilebody1
endlabelwhilecmp0:
load z
const "what's up?"
store z
jump labelifcmp4
labelifbody5:
const "Z is the same as y!"
call String:print
pop
const "\n"
call String:print
pop
jump endlabelifcmp4
labelifcmp4:
load z
load y
call String:equals
jump_if labelifbody5
labelelse6:
jump labelifcmp7
labelifbody8:
const "Y is "
call String:print
pop
load y
call String:print
pop
const "\n"
call String:print
pop
jump endlabelifcmp7
labelifcmp7:
load y
const "no"
call String:equals
jump_if labelifbody8
labelelse9:
load done
const false
store done
jump labelifcmp10
labelifbody11:
load done
call Bool:print
pop
const "\n"
call String:print
pop
jump endlabelifcmp10
labelifcmp10:
load done
jump_ifnot labelifbody11
labelelse12:
const "done is somehow true!"
call String:print
pop
const "\n"
call String:print
pop
endlabelifcmp10:
endlabelifcmp7:
endlabelifcmp4:
jump labelifcmp13
labelifbody14:
load z
call String:print
pop
const "\n"
call String:print
pop
jump endlabelifcmp13
labelifcmp13:
load x
const 5
call Int:greater
jump_if labelifbody14
load x
const 10
call Int:less
jump_if labelifbody14
endlabelifcmp13:
return 0