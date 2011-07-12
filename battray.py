#!/usr/bin/env python
#
# vim:ts=2:sts=2:
#
# Battray 1.3 by Martin Tournoij <martin@arp242.net>
# http://arp242.net/code/battray/
#
# With additional contributions from:
# Andy Mikhaylenko <andy@neithere.net> (Linux platform)
#
# Feel free to use, modify, and redistribute as you see fit. There are no
# restrictions.
#
# Supported platforms:
# FreeBSD, OpenBSD, Linux
#
# Adding a new platform is usually very easy! Take a look at
# platforms/README.TXT
#

import getopt
import os
import signal
import subprocess
import sys

nosound = True
if sys.platform[:3] == 'win':
	try:
		import winsound
		nosound = False
	except ImportError:
		nosound = True
else:
	# Only works on Linux and FreeBSD
	try:
		import ossaudiodev
		import wave
		try:
			import thread
		except ImportError:
			import dummy_thread as thread
		_soundthread_ = []
		nosound = False
	except ImportError:
		nosound = True

# py-gtk2 2.10 or higher required
try:
	import gobject
	import gtk
except ImportError:
	print >> sys.stderr, 'Battray: Error, PyGTK 2.10 or higher is required, unable to find PyGTK.'
	print >> sys.stderr, 'Battray: PyGTK homepage http://www.pygtk.org/'
	sys.exit(1)

def Usage():
	"""
	Print help/usage info.
	Note: We do not exit
	"""

	print "  Usage: %s [-hv] [-p platform] [-d datadir] [-f configfile]" % os.path.basename(sys.argv[0])
	print "  [-i pol_interval]"
	print ""
	print "\t-h, --help\tPrint this help message and exit."
	print "\t-v, --version\tPrint version and exit."
	print "\t-d, --datadir\tDatadir to use (For icons)."
	print "\t-f, --file\tConfiguration file to use."
	print "\t-i, --interval\tPoll the status every n seconds."
	print "\t-p, --platform\tSpecify a specific platform file."
	print ""
	print "  Please see battray(1) for more documentation."

# _config is a global variable that hold the configuration. _p is for the
# platform file
_config = None
_p = None

def Init():
	"""
	Try to find and import configuration file and parse commandline arguments
	"""

	# Make sure we're using the right PyGTK version
	ver = float('%i.%i' % (gtk.ver[0], gtk.ver[1]))
	if ver <= 2.10:
		print >> sys.stderr, 'Battray: Error, PyGTK 2.10 or higher is required, found version %.2f' % ver
		print >> sys.stderr, 'Battray: PyGTK homepage http://www.pygtk.org/'
		sys.exit(1)
	
	# Parse commandline arguments.
	try:
		options, arguments = getopt.getopt(sys.argv[1:], 'hvd:f:p:i:',
			['help', 'version', 'datadir=', 'file=', 'platform=', 'interval='])
	except getopt.GetoptError:
		Usage()
		print >> sys.stderr, "\nBattray: Error,", sys.exc_info()[1]
		sys.exit(1)

	optionfile = ''
	platform = sys.platform[:-1]
	cpollinterval = None
	cdatadir = None

	for opt, arg in options:
		if opt == '-h' or opt == '--help':
			Usage()
			sys.exit(0)
		elif opt == '-v' or opt == '--version':
			print 'Battray 1.3'
			print 'Martin Tournoij <martin@arp242.net>'
			print 'http://arp242.net/code/battray/'
			sys.exit(0)
		elif opt == '-f' or opt == '--file':
			if not os.path.exists(arg):
				print >> sys.stderr, "Battray: Configuration file `%s' doesn't exists." % arg
				sys.exit(1)
			optionfile = arg
		elif opt == '-d' or opt == '--datadir':
			cdatadir = arg
		elif opt == '-i' or opt == '--interval':
			cpollinterval = arg
		elif opt == '-p' or opt == '--platform':
			platform = arg

	_config = LoadConfig(optionfile)

	# Override values from config file with commandline arguments
	if cdatadir is not None:
		_config['datadir'] = datedir

	if cpollinterval is not None:
		_config['pollinterval'] = pollinterval

	_p = LoadPlatform()

	return _config, _p

def LoadConfig(optionfile=''):
	"""
	Try to load the configuration file
	"""

	global _config

	# Load configuration file
	configlocation = (
		os.path.expanduser(optionfile),
		os.path.expanduser('~/.battray/battrayrc.py'),
		os.path.expanduser('~/.battrayrc.py'),
		'/usr/local/etc/battrayrc.py',
		'/usr/local/etc/battray/battrayrc.py',
		'/etc/battrayrc.py',
		'/etc/battray/mbatrayrc.py',
		'/usr/local/share/battray/battrayrc.py',
		'/usr/local/share/examples/battray/battrayrc.py',
		'/usr/share/battray/battrayrc.py',
		'./battrayrc.py'
	)

	foundfile = False
	for config in configlocation:
		if os.path.exists(config):
			foundfile = True
			sys.path.append(os.path.dirname(config))
			try:
				exec open(config, 'r').read()
				_config = {
					'datadir': datadir,
					'pollinterval': pollinterval,
					'icon': icon,
					'color': color,
					'blink': blink,
					'play': play,
					'run': run,
				}
			except:
				print >> sys.stderr, "Battray: Unable to load configuration file `%s'" % config
				print >> sys.stderr, sys.exc_info()[1]
				sys.exit(1)
			break

	# We need a config file!
	if not foundfile:
		print >> sys.stderr, 'Battray: Unable to find configuration file, looking in:'
		for c in configlocation:
			print >> sys.stderr, '\t' + c
		sys.exit(1)

	# Just in case someone added quotes
	_config['pollinterval'] = int(_config['pollinterval'])

	# Sanity checking
	if not os.path.exists(_config['datadir']):
		print >> sys.stderr, "Battray: Datadir `%s' doesn't exist." % _config['datadir']
		sys.exit(1)

	return _config

def LoadPlatform():
	"""
	Load/import platform information
	"""

	# Get platform information
	platform = sys.platform[:-1]
	platformfile = '%s/platforms/%s' % (_config['datadir'], platform)
	if platformfile[:3] == '.py':
		platformfile = platform[:-3]

	sys.path.append(os.path.dirname(platformfile))

	try:
		_p = __import__(os.path.basename(platformfile))
	except ImportError:
		print >> sys.stderr, "Battray: Unable to get information for platform `%s'\n%s" % (
			platform, sys.exc_info()[1])
		sys.exit(1)
	
	return _p

def CheckBatt(tray, data = None):
	"""
	Check battery status & update tray.
	"""

	reload(_p)

	try:
		SetIcon(tray, _p.ac, _p.charging, _p.percent, _p.lifetime, _p.tooltip)
	except AttributeError:
		SetIcon(tray, _p.ac, _p.charging, _p.percent, _p.lifetime)
	
	return True # Keep this!

def CheckBattFromMenu(widget, tray):
	CheckBatt(tray)

def SetIcon(tray, ac, charging, percent, lifetime, tooltip=''):
	"""
	Set icon & tooltip.
	"""

	text = []

	# Make some pretty tooltip text and determine icon.
	if ac == None:
		text.append('Cannot get battery status.\n')
	elif ac:
		text.append('Connected to AC power.\n')
	elif not ac:
		text.append('Running on battery.\n')
	
	if percent == 255:
		text.append('Cannot get battery percentage status.\n')
	else:
		text.append('%i percent battery power remaining.\n' % percent)
	
	if charging:
		pass
	elif lifetime == 255:
		text.append('Unknown lifetime remaining.\n')
	else:
		t = lifetime / 3600.0
		text.append('Approximately %.1f hours remaining.\n' % t)

	if charging == None:
		# Just skip
		pass
	elif charging == True:
		text.append('Charging battery.')
	else:
		text.append('Not charging battery.')

	icon = gtk.gdk.pixbuf_new_from_file('%s/icons/%s' % (_config['datadir'],
		_config['icon']))
	# Fill battery icon with background to indicate status. Skip everything
	# that's black to preserve the plus sign.
	# XXX Disable this, this feature requires py-numpy, which pulls in gcc4.4
	# :-(
	#if not ac or charging:
	#	fill = gtk.gdk.pixbuf_new_from_file('%s/icons/%s' % (
	#		_config['datadir'], _config['icon']))
	#	pixelArray = icon.get_pixels_array()
	#	# 24 pixels wide
	#	fillAmount = int(round(percent / 4))
	#
	#	col = 2
	#	while col <= fillAmount + 2:
	#		row = 10
	#		while row <= 21:
	#			# Black pixel
	#			if pixelArray[row][col][3] == 255:
	#				row += 1
	#				continue
	#			
	#			fill.copy_area(0, 0, 1, 1, icon, col, row)
	#			row += 1
	#		col += 1

	# Warn the user if battery is low
	if _config['blink']:
		tray.set_blinking(True)
	else:
		tray.set_blinking(False)

	try:
		text += '\n' + _p.tooltip
	except AttributeError:
		pass

	# We are ready to set the icon & tooltip
	tray.set_from_pixbuf(icon)
	s = ''
	s = s.join(text)
	tray.set_tooltip(s)

def PopupMenu(widget, button, lifetime, data = None):
	if button == 3:
		if data:
			data.show_all()
			data.popup(None, None, None, 3, lifetime)

def Quit(widget, data = None):
	if data:
		data.set_visible(False)
	gtk.main_quit()
 
def AboutDialog(widget, data = None):
	about = gtk.AboutDialog()
	about.set_authors(['Martin Tournoij <martin@arp242.net>', 'Andy Mikhaylenko <andy@neithere.net>'])
	about.set_version('1.3')
	about.set_website('http://arp242.net/code/batttray/')
	about.set_comments('Simple program that displays a tray icon to inform you on your notebooks battery status.')
	about.run()
	about.destroy()

def ReloadConfig(signum, stack):
	print 'Battray: Caught SIGHUP, reloading platform information.'
	reload(_p)

def PlaySound(soundfile):
	"""
	Play a sound.
	We expect this to be run inside a new thread, started with something like:
	_soundthread_.append(thread.start_new_thread(PlaySound, (soundfile,)))
	"""

	s = wave.open(soundfile, 'rb')
	(nc,sw,fr,nf,comptype, compname) = s.getparams( )
	dsp = ossaudiodev.open('/dev/dsp', 'w')

	try:
		from ossaudiodev import AFMT_S16_NE
	except ImportError:
		if byteorder == "little":
			AFMT_S16_NE = ossaudiodev.AFMT_S16_LE
		else:
			AFMT_S16_NE = ossaudiodev.AFMT_S16_BE

	dsp.setparameters(AFMT_S16_NE, nc, fr)
	data = s.readframes(nf)
	s.close()
	dsp.write(data)
	dsp.close()
	_soundthread_.remove(thread.get_ident())
	thread.exit()

def run(cmd):
	print cmd; return

	try:
		o = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True).communicate()[0]
	except OSError:
		print >> sys.stderr, "Battray: Something went wrong executing `%s'\n%s" % (
			cmd, sys.exc_info()[1])

def color(color):
	print color

def play(sound):
	print sound; return

	if _config['nosound']:
		return
	
	if len(_soundthread_) < 1:
		if os.path.exists(cmd[4:].strip()):
			snd = cmd[4:].strip()
		else:
			snd = '%s/%s' % (_config['datadir'], cmd[4:].strip())
			_soundthread_.append(thread.start_new_thread(PlaySound, (snd,)))

if __name__ == '__main__':
	_config, _p = Init()

	if nosound:
		_config['nosound'] = True
	else:
		_config['nosound'] = False

	# Reload config on kill -HUP
	signal.signal(signal.SIGHUP, ReloadConfig)

	# Tray icon
	tray = gtk.StatusIcon()
	tray.connect('activate', CheckBatt)
	tray.set_visible(True)
	CheckBatt(tray)

	# The popup menu
	menu = gtk.Menu()
	
	item = gtk.MenuItem('Refresh status')
	item.connect('activate', CheckBattFromMenu, tray)
	menu.append(item)

	item = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
	item.connect('activate', AboutDialog)
	menu.append(item)

	item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
	item.connect('activate', Quit, tray)
	menu.append(item)

	tray.connect('popup-menu', PopupMenu, menu)
	gobject.timeout_add(_config['pollinterval'] * 1000, CheckBatt, tray)

	try:
		gtk.main()
	except KeyboardInterrupt:
		print ''
		sys.exit(0)
