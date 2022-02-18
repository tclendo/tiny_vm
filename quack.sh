#!/bin/bash

python3 compiler/quack_frontend.py -i=src/$1.qk -o=asm/$1.asm -c=$1;

if [ $? == 0 ]
then
	echo "Compiled $1.qk -> $1.asm";
	python3 assemble.py asm/$1.asm OBJ/$1.json;
	if [ $? == 0 ]
	then
		echo "Assembled $1.asm -> $1.json";
		echo "Done";
	else
		echo "Error assembling. Aborted";
	fi
else
	echo "Error compiling. Aborted";
fi

