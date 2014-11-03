#
# http://code.arp242.net/battray
#
# Copyright © 2008-2014 Martin Tournoij <martin@arp242.net>
# See below for full copyright
#
# Return False on error
# Or return tuple with:
# ac:        Connected to AC? Boolean, None if unknown.
# charging:  Are we charging the battery? Boolean, None if unknown.
# percent:   Battery power remaining in percent (0-100), integer, -1 if unknown.
# lifetime:  Battery time remaining in minutes, integer, -1 if unknown.
#

import sys

def find():
	platform = ''
	for char in sys.platform:
		if char in '1234567890': break
		platform += char

	fun = globals().get(platform, None)
	if fun is None:
		print('Error: unable to get platform for %s' % platform)
		sys.exit(1)

	return fun


def freebsd():
	""" FreeBSD, should work at least for 8 and newer """
	import subprocess

	o = subprocess.Popen(['acpiconf', '-i0'], stdout=subprocess.PIPE).communicate()[0]

	for line in o.split('\n'):
		if line.find(':') == -1:
			continue
		(key, value) = line.split(':', 1)
		
		if key.strip() == 'Remaining capacity':
			percent = int(value.strip().replace('%', ''))
		elif key.strip() == 'Remaining time':
			if value.strip() == 'unknown':
				lifetime = -1
			else:
				lifetime = value.strip().replace(':', '.')
				lifetime = int(int(lifetime[0]) * 60 + int(lifetime[2]) * 10)
		elif key.strip() == 'State':
			if value.strip() == 'charging':
				charging = True
			else:
				charging = False
		elif key.strip() == 'Present rate':
			if value.strip() == '0 mW' or value.strip().endswith('(0 mW)'):
				ac = True
			else:
				ac = False
		elif key.strip() == 'State' and value.strip() == 'not present':
			ac = None

	if charging:
		ac = True

	return (ac, charging, percent, lifetime)


def openbsd():
	""" OpenBSD; should work with all versions since 4 (possibly earlier) """

	import subprocess

	ac = charging = None
	percent = lifetime = 999

	def sysctl(name):
		o = subprocess.Popen(['/sbin/sysctl', name], stdout=subprocess.PIPE,
			stderr=subprocess.PIPE).communicate()[0].decode()
		(name, value) = o.split('=')
		return value

	o = subprocess.Popen(['/usr/sbin/apm', '-alm'], stdout=subprocess.PIPE).communicate()[0]
	(percent, lifetime, ac) = o.decode().split()

	if ac == '0':
		ac = False
	elif ac == '1':
		ac = True
	else:
		ac = None

	# apm output is not always reliable ...
	if sysctl('hw.sensors.acpibat0.raw0')[:1] == '2':
		charging = True
	else:
		charging = False

	percent = int(percent)
	if lifetime == 'unknown':
		lifetime = -1
	else:
		lifetime = float(lifetime) * 60

	return (ac, charging, percent, lifetime)


def linux():
	"""	 Linux, being Linux, has several incompatible ways of doing this. """

	for linux_sucks in ['linux_acpi', 'linux_acpitool', 'linux_upower']:
		result = globals().get(linux_sucks)()
		if result != False: return result
	return False


def linux_acpi():
	""" Linux with acpi; this is an interface to /sys/, and maybe it's better if
	we access that directly, but I can't figure this out since proper documentation
	is near-nonexistent, and what does exist, is shit. I have better things to
	do with my life, so just use acpi """

	import subprocess

	try:
		p = subprocess.Popen(['acpi'], stdout=subprocess.PIPE)
	except OSError:
		return False

	data = p.communicate()[0].decode().split(',')

	if 'Discharging' in data[0]:
		ac = False
		charging = False
	elif 'Charging' in data[0]:
		ac = True
		charging = True
	elif 'Full' in data[0]:
		ac = True
		charging = False

	percent = int(data[1].strip()[:-1])
	lifetime = -1
	if charging:
		lifetime = -1 # TODO
	elif ac == False:
		lifetime = list(map(int, data[2][:8].split(':')))
		lifetime = lifetime[0] * 60 + lifetime[1]

	return (ac, charging, percent, lifetime)


def linux_acpitool():
	""" Linux with acpitool """
	import subprocess

	try:
		p = subprocess.Popen(['acpitool'], stdout=subprocess.PIPE)
	except OSError:
		return False

	data = p.communicate()[0].decode()

	for line in data.split('\n'):
		if line == '': continue
		k, v = line.strip().split(':', 1)

		k = k.strip().lower()
		v = v.strip().lower()

		if k.startswith('battery #1'):
			charging, percent, lifetime = v.split(',')
			if charging == 'charging': charging = True
			else: charging = False

			percent = float(percent[:-1])

			h, m, s = [ int(i) for i in lifetime.split(':') ]
			lifetime = h * 60 + m
			if lifetime == 0: lifetime = -1
		elif k == 'ac adapter':
			if v == 'off-line':
				ac = False
				charging = False
			elif v == 'online':
				ac = True


def linux_upower():
	""" Linux with UPower """
	try:
		# http://upower.freedesktop.org/docs/Device.html
		import dbus
	except ImportError:
		return False

	bus = dbus.SystemBus()
	upower = bus.get_object('org.freedesktop.UPower', '/org/freedesktop/UPower/devices/battery_BAT0')
	iface = dbus.Interface(upower, 'org.freedesktop.DBus.Properties')
	info = iface.GetAll('org.freedesktop.UPower.Device')

	if __name__ == '__main__':
		import pprint

		l = []
		for k, v in dict(info).iteritems():
			l.append('%s -> %s' % (k, v))
		l.sort()
		for i in l: print(i)

	percent = float(info['Percentage'])
	state = int(info['State'])
	charging = False
	if state == 1:
		ac = True
		charging = True
	elif state == 2:
		ac = False
	elif state == 4:
		ac = True
	else:
		ac = None

	lifetime = int(info['TimeToEmpty']) / 60

	return (ac, charging, percent, lifetime)


# The MIT License (MIT)
#
# Copyright © 2008-2014 Martin Tournoij
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
