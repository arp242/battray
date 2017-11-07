#!/usr/bin/env python3

import glob, os, shutil, sys

from setuptools import setup

if sys.version_info[0] < 3:
    print('Error: you need Python 3 to run battray')
    sys.exit(1)

if not os.path.exists('build/_scripts'):
    os.makedirs('build/_scripts')
shutil.copyfile('battray.py', 'build/_scripts/battray')

setup(
    name = 'battray',
    version = '2.2',
    author = 'Martin Tournoij',
    author_email = 'martin@arp242.net',
    url = 'http://arp242.net/code/battray',
    license = 'MIT',
    packages = ['battray'],
    description = 'simple tray icon to show your laptop’s battery status.',
    long_description = '''Battray is a fairly simple tray icon to show your laptop’s battery status.
It's simple, easy, fairly environment-independent, and ‘just works’ without
tons of {Gnome,KDE,..} dependencies.

You can also configure it to play annoying sounds if your battery is getting low,
dim the screen when you switch from AC to battery, etc.''',

    scripts = ['build/_scripts/battray'],
    data_files = [
        ('share/battray', glob.glob('data/*'))
    ],

    install_requires=['pygobject'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
