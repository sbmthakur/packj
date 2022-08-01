#!/usr/bin/python

#
# Based on https://github.com/dirtyharrycallahan/pystrace
#

import sys

from strace import *
from strace_utils import *

import json
import os,sys

#
# strace usage: strace -f -ttt -T -o strace.log <cmd>
#
from syscalls import syscall_table

summary = {}

def parse(input_file):
    infile = open(input_file, "r")
    strace_stream = StraceInputStream(infile)

    for entry in strace_stream:
        
        #breakpoint()
        ts = entry.timestamp
        name = entry.syscall_name

        try:
            return_value = int(entry.return_value)
        except:
            #print(f"Invalid return value: {entry.return_value}")

            # permit syscalls that do not depend on return_value
            if 'exit' in name:
                return_value = entry.return_value
            else:
                continue
        
        if name in ['newfstatat', 'EXIT']:
            continue

        num_args = len(entry.syscall_arguments)
        args = []

        for idx in range(num_args):
            arg = array_safe_get(entry.syscall_arguments, idx)
            args.append(arg)

        args_str = ','.join(args)

        syscall_info = syscall_table.get(name.upper(), None)
        if not syscall_info:
            continue

        parser = syscall_info.get("parser", None) 
        category = syscall_info.get("category", None)
        if parser and category:
            data = parser(ts, name, args_str, args, return_value)
            if not data:
                continue
            if category not in summary:
                summary[category] = []
            summary[category].append(data)    

    infile.close()
    strace_stream.close()

    with open('./summary.json', mode='w') as f:
        f.write(json.dumps(summary, indent=4))

if __name__ == "__main__":
    input_file = sys.argv[1]
    parse(input_file)
