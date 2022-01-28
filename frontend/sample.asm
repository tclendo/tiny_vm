.class Sample:Obj

.method $constructor
.local i,j,cat,other,a
const 42
const 13
call Int:plus
store i
load i
const 32
roll 1
call Int:minus
store j
load j
call Int:print
const "\n"
call String:print
const "Nora"
store cat
const " can solve puzzles"
store other
load cat
load other
roll 1
call String:plus
call String:print
const "\n"
call String:print
const false
store a
load j
load j
call Int:times
store j
load j
call Int:print
const "\n"
call String:print
pop
pop
pop
pop
pop
pop
return 0