#!/usr/bin/env python

from __future__ import print_function

import sys

# sys.version_info[0] is the major version number. sys.version_info[1] is minor
if sys.version_info[0] != 3:
	print('\n*** WARNING *** Please use Python 3! Exiting.')
	exit(1)

if __name__ == '__main__':
	try:
		from options import Options
		opts = Options(sys.argv[1:])
		assert opts, 'Failed to parse cmdline args!'

		args = opts.args()
		assert args, 'Failed to get cmdline args!'

		if cmd == 'deps':
			handle_deps(args, extra_args)
		# audit request
		elif args.cmd == 'audit':
			from audit import main
			main(args)

		# sandbox install
		elif args.cmd == 'sandbox':
			from install import main
			main(args)

	except Exception as e:
		print(str(e))
		exit(1)
