#!/usr/bin/env python3
# encoding: utf-8
#
# http://code.arp242.net/battray
#
# Copyright © 2008-2015 Martin Tournoij <martin@arp242.net>
# See below for full copyright
#

from __future__ import print_function
import argparse, logging, signal, sys
from gi.repository import Gtk

if sys.version_info[0] < 3:
	print('Error: you need Python 3 to run batray')
	sys.exit(1)

import battray


if __name__ == '__main__':
	battray.set_proctitle('battray')
	parser = argparse.ArgumentParser()

	parser.add_argument('-v', '--verbose', action='store_true',
		help='enable verbose messages')
	parser.add_argument('-p', '--platform', action='store',
		help='''Platform name, a list of platforms can be found in \
		`battray/platforms.py`; by default this is automatically detected''')
	parser.add_argument('-i', '--interval', action='store', type=int,
		help='Polling interval in seconds; defaults to 15')
	parser.add_argument('-c', '--configfile', action='store',
			help='''Config file to use''')
	parser.add_argument('-d', '--datadir', action='store',
			help='''Data dir to use for image, sounds, etc.''')
	args = vars(parser.parse_args())
	
	if args['verbose']: logging.basicConfig(level=logging.DEBUG)
	del args['verbose']

	battray.Battray(**args)

	try:
		# Make SIGINT (^C) work; http://stackoverflow.com/a/16486080/660921
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		Gtk.main()
	except KeyboardInterrupt:
		print('')
		sys.exit(0)


# The MIT License (MIT)
#
# Copyright © 2008-2015 Martin Tournoij
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# The software is provided "as is", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. In no event shall the
# authors or copyright holders be liable for any claim, damages or other
# liability, whether in an action of contract, tort or otherwise, arising
# from, out of or in connection with the software or the use or other dealings
# in the software.
