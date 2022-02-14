#!/bin/bash

python3 frontend/quack_frontend.py -i=frontend/src/$1.qk -o=frontend/out/$1.asm;
echo "Compiled $1.qk -> $1.asm";
python3 assemble.py frontend/out/$1.asm OBJ/$1.json;
echo "Assembled $1.asm -> $1.json";
echo "Done";
