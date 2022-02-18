#!/bin/bash

python3 frontend/quack_frontend.py -i=src/$1.qk -o=asm/$1.asm -c=$1;
echo "Compiled $1.qk -> $1.asm";
python3 assemble.py asm/$1.asm OBJ/$1.json;
echo "Assembled $1.asm -> $1.json";
echo "Done";
