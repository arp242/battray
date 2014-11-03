#!/usr/bin/env python

import glob, os, shutil

from distutils.core import setup

if not os.path.exists('build/_scripts'):
	os.makedirs('build/_scripts')
shutil.copyfile('battray.py', 'build/_scripts/battray')

setup(
	name = 'battray',
	version = '2.0',
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
