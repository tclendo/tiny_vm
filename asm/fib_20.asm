.class fib_20:Obj

.method $constructor
.local n1,n2,next,x
load n1
const 0
store n1
load n2
const 1
store n2
load next
const 0
store next
load x
const 0
store x
jump labelwhilecmp0
labelwhilebody1:
load next
load n1
load n2
call Int:plus
store next
load next
call Int:print
pop
const "\n"
call String:print
pop
load n1
load n2
store n1
load n2
load next
store n2
load x
load x
const 1
call Int:plus
store x
labelwhilecmp0:
load x
const 20
call Int:greater
jump_if labelwhilebody1
endlabelwhilecmp0:
load x
call Int:print
pop
const " fibonnaci numbers\n"
call String:print
pop
return 0