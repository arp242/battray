Battray is a fairly simply tray icon to show your laptop’s battery status.
It's simple, easy, fairly environment-independent, and ‘just works’ without
tons of (Gnome|KDE|..) dependencies. [Here’s a screenshot][2].

You can also configure it to play annoying sounds if your battery is getting low,
dim the screen when you switch from AC to battery, etc.

Installation
============
Battray requires py-gtk2, on Linux it also required acpitool. At the moment it
runs on FreeBSD, OpenBSD, and Linux. [Adding a new platform is usually very
easy][1]

To install Battray, run `./setup.py install`, at the moment you can’t run it
directly from the source directory.

Files & directories installed:

- `$PREFIX/bin/battray`
- `$PREFIX/man/man1/battray.1`
- `$PREFIX/lib/python/site-packages/battray/`
- `$PREFIX/share/battray/`


Linux & sound
-------------
I find it truly flabbergasting that in 15+ years of mucking about, Linux *still*
can't manage to produce a sound system which just fucking works.  
Battray uses OSS to make sound, which may or may work out of the box. Ubuntu
seems to require [special tricks](https://help.ubuntu.com/community/alsa-oss).


FreeBSD package
---------------
Available in the ports collection as [sysutils/battray](http://www.freshports.org/sysutils/battray/)

Configuration
=============
The default settings should be good for most people, but Battray is pretty
flexible and can do more.  
The default configuration is at `$PREFIX/share/battray/battrayrc_default.py`,
copy it to `~/.battrayrc.py` and edit it, there are a few comments to get you
started.  
For the full documentation, look at the manpage.

ChangeLog
=========
Version 1.6, not yet released
--------------------
- Support both Python 2 & 3
- Bugfix: Don't panic if there's no battery present (again...)

Version 1.5, 20120711
---------------------
- Bugfix: Fix FreeBSD CURRENT/10
- Bugfix: Don't panic if there's no battery present (FreeBSD)
- Bugfix: Properly deal with unknown percentage/lifetime values
- Feature: Add `playonce()` and `reset_playonce()` functions
- Update default config
- Update docs

Version 1.4, 20110926
---------------------
- Play sounds in a better way (Separate thread, not separate process)
- Update a few docs

Version 1.3, 20110724

- **Configuration files from previous versions are not compatible**
- Add Linux support (Submitted by Andy Mikhaylenko).
- Better configuration file/platform file importing.
- We now play a wav file with OSS instead of (trying to) use the PC speaker. Most laptops emulate a PC speaker, but the exact implementation varies from vendor to vendor and is the usual mess we've come to expect of these simple things :-(
- Add installer.
- Fix FreeBSD/amd64

Version 1.2, 20091022
---------------------
- New configuration file syntax, which is much more flexible.
- Add simple Makefile for easier installation & deinstallation.
- Add manpage.
- Various minor improvements

Version 1.1, 20090906
---------------------
- Battery icon is now green/yellow/red depending on battery life remaining.
- Battray will now warn you if battery level is below a certain percentage (See warn and warnMethod options in config.py).
- Reload configuration on SIGHUP.
- Added instructions on how to add platform.
- Add new icon to indicate error (Instead of no icon loaded at all).
- Fix FreeBSD platform, thanks to Eponasoft @ FreeBSD forums for reporting & testing.
- Some improvements on the OpenBSD platform.

Version 1.0, 20090816
---------------------
- Initial release.

[1]: https://bitbucket.org/Carpetsmoker/battray/src/db6f2319bb8de35440845902a849c67798ef7fce/battray/platforms/README.TXT?at=default
[2]: https://bitbucket.org/Carpetsmoker/battray/raw/ce21d3ebca4df6ef4c13687ebf6c72f45e9e6390/doc/screenshot.png
