#!/bin/sh
strace -f -e trace=network,file,process -ttt -T -o /tmp/strace.log pip3 install --quiet tensorflow
cat /tmp/strace.log | grep EXDEV
#python3 main.py pypi tensorflow --dynamic
