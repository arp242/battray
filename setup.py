#!/usr/bin/env python3

import glob, os, shutil, sys

from distutils.core import setup

if sys.version_info[0] < 3:
	print('Error: you need Python 3 to run batray')
	sys.exit(1)


if not os.path.exists('build/_scripts'):
	os.makedirs('build/_scripts')
shutil.copyfile('battray.py', 'build/_scripts/battray')

setup(
	name = 'battray',
	version = '2.2',
	author = 'Martin Tournoij',
	author_email = 'martin@arp242.net',
	url = 'http://code.arp242.net/battray',
	license = 'MIT',
	packages = ['battray'],
	scripts = ['build/_scripts/battray'],
	data_files = [
		('share/battray', glob.glob('data/*'))
	],
)
