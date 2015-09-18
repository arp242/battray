#
# http://code.arp242.net/battray
#
# Copyright © 2008-2015 Martin Tournoij <martin@arp242.net>
# See below for full copyright
#

import logging, os, sys

from . import platforms, sound
__all__ = ['platforms', 'sound']


def find_config(configfile=None, datadir=None):
	xdg_config_home = '{}/battray'.format(os.getenv('XDG_CONFIG_HOME') or os.path.expanduser('~/.config'))
	xdg_datadirs = (os.getenv('XDG_DATA_DIRS') or '/usr/local/share:/usr/share').split(':')

	default_config = None

	if datadir is not None:
		f = '{}/battray/battrayrc.py'.format(datadir)
		if os.path.exists(f):
			default_config = f

	for xdg_datadir in xdg_datadirs:
		if datadir is None:
			d = '{}/battray'.format(xdg_datadir)
			if os.path.exists(d):
				datadir = d

		if default_config is None:
			f = '{}/battray/battrayrc.py'.format(xdg_datadir)
			if os.path.exists(f):
				default_config = f

	# XDG failed; try to load from cwd
	mydir = os.path.dirname(os.path.realpath(sys.argv[0]))
	if default_config is None:
		f = '{}/data/battrayrc.py'.format(mydir)
		if os.path.exists(f): default_config = f

	if configfile is None:
		f = '{}/battrayrc.py'.format(xdg_config_home)
		if os.path.exists(f):
			configfile = f
		else:
			configfile = default_config

	if configfile is None:
		raise Exception("Can't find config file")

	if datadir is None:
		d = '{}/data'.format(mydir)
		if os.path.exists(d): datadir = d

	if datadir is None:
		raise Exception("Can't find data dir")

	logging.info('Using {}'.format(configfile))
	return configfile, datadir, default_config


def set_proctitle(title):
	try:
		# This is probably the best way to do this, but I don't want to force an
		# external dependency on this C module...
		import setproctitle
		setproctitle.setproctitle(title)
	except ImportError:
		import ctypes, ctypes.util

		libc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('c'))
		title_bytes = title.encode(sys.getdefaultencoding(), 'replace')
		buf = ctypes.create_string_buffer(title_bytes)

		# BSD, maybe also OSX?
		try:
			libc.setproctitle(ctypes.create_string_buffer(b"-%s"), buf)
			return
		except AttributeError:
			pass

		# Linux
		try:
			libc.prctl(15, buf, 0, 0, 0)
			return
		except AttributeError:
			pass


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
