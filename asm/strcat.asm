.class strcat:Obj

.method $constructor
.local 
const "This is first\n"
const "This is second\n"
roll 1
call String:plus
call String:print
return 0