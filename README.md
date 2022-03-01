# tiny_vm
A tiny virtual machine interpreter for Quack programs

## Work in progress

This is intended to become the core of an interpreter for the Winter 2022
offering of CIS 461/561 compiler construction course at University of Oregon, 
if I can ready it in time. 

## HW1 Changes

The virtual machine interpreter can execute basic calculator operations such
as add, subtract, multiply, divide, and negate, all with proper order of
operations. The basic parser lies in the frontend folder. To run programs
on the tiny_vm, follow these instructions:

	1. In the frontend folder, calc.py can be run by piping input and output from any file. To run the examples in the directory, run "python3 calc.py < input.txt > sample.asm". This will generate the assembly code for our vm.
	2. In the repository's home folder, run assemble.py on the created .asm file: "python3 assemble.py frontend/sample.asm sample.json". This will generate the object code for our vm in the form of a .json file.
	3. Make sure cmake is installed and properly configured with cjson. In the repository's home directory run "cmake ." then "make". This should generate the tiny_vm binary that you can then run. It automatically looks for the sample.json file in the same directory.

## HW2 Changes

Homework 2 saw the extension of our toy calculator to behave in certain ways like Quack does as a language. We can assign integer, string, boolean, and nothing values to variables, and we can see the pipeline in action much more than we could before. To write a program and compile it, follow these steps:

	1. In the frontend folder, there is a test.txt file that can be read by the quack_frontend.py file to generate an asm file. To generate the asm file, simply run python3 quack_frontend.py -i=hw2.qk -o=sample.asm
	2. In the repository's home folder, run 'python3 assemble.py frontend/sample.asm OBJ/Sample.json' to generate the bytecode for the virtual machine in the OBJ directory.
	3. To run the code, simply run 'make' and then 'bin/tiny_vm -L OBJ Sample' and then the VM will run your code!

## HW3 Changes

Homework 3 now has type checking and type inference, variable initialization checks, while loops, if/elif/else statements, short-circuit boolean operations, and a bunch of other cool stuff. The code has been refactored into multiple files, and there will probably be even more refactoring for the next sprint. To compile a quack program, run the following command:

	1. ./quack <filename>.qk <run>?

If you get an error saying permission denied, try running

	1. bash quack <filename> <run>?

If you add the optional 'run' parameter, it will run the code on the tiny_vm as well (as long as it exists). It will also automatically compile the proper object file name based on the name passed into the compiler.
