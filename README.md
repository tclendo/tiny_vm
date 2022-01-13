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
