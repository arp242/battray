#!/usr/bin/env python

import glob
import subprocess
import sys

from distutils.core import setup

setup(
	name = 'battray',
	version = '1.6',
	author = 'Martin Tournoij',
	author_email = 'martin@arp242.net',
	url = 'http://code.arp242.net/battray',
	description = '',
	download_url = '',
	classifiers = '',
	platforms = '',
	license = '',
	packages = ['battray', 'battray/platforms'],
	scripts = ['bin/battray'],
	data_files = [
		('share/battray', ['data/alert.wav']),
		('share/battray/icons', glob.glob('data/icons/*')),
		('man/man1', ['doc/battray.1']),
	],
)
