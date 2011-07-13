#!/usr/bin/env python

import glob
from distutils.core import setup

setup(
	name = 'battray',
	version = '1.3',
	author = 'Martin Tournoij',
	author_email = 'martin@arp242.net',
	url = 'http://arp242.net/code/battray/',
	scripts = glob.glob('bin/*'),
)
