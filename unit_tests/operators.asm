# Sample assembly code
# (augment as the assember and loader are built out)
.class Sample:Obj

.method $constructor
	const "A string\n"
	call  String:print
	pop
	const 1
	const 2
	call Int:plus
	const 3
	call Int:equals
	call Bool:print
	pop
	const "\n"
	call String:print
	pop
	const 1
	const 3
	call Int:minus
	const 2
	call Int:equals
	call Bool:print
	pop
	const "\n"
	call String:print
	pop
	const 3
	const 3
	call Int:times
	const 9
	call Int:equals
	call Bool:print
	pop
	const "\n"
	call String:print
	const 1
	const 5
	call Int:divide
	const 5
	call Int:equals
	call Bool:print
	pop
	const "\n"
	call String:print
	pop
	return 0
