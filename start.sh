#!/bin/sh
strace -f -e trace=network,file,process -ttt -T -o strace.log pip install --quiet tensorflow
#python3 main.py pypi tensorflow --dynamic
