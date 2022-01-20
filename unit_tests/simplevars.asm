.class Vars:Obj

.method $constructor
.local 	x,y
	const 3
	store x
	const "expect x = 3: "
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
	call Int:times
	store y
	const "expect y = 9: "
	call String:print
	pop
	load y
	call Int:print
	pop
	const "\n"
	call String:print
	pop
	return 0
	
