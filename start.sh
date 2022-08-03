#!/bin/sh
cat aaa | while read line
	do
		strace -f -e trace=network,file,process -ttt -T -o strace_$line.log pip install --quiet $line
	done
#python3 main.py pypi tensorflow --dynamic
