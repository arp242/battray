ac = charging = None
percent = lifetime = 999

try:
	# http://upower.freedesktop.org/docs/Device.html
	import dbus

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

	tooltip = []
	for line in open('/proc/cpuinfo', 'r').readlines():
		if line.startswith('cpu MHz'):
			tooltip.append('%s MHz' % int(float(line.split(':')[1].strip())))

	tooltip = 'CPU frequency: %s' % ' / '.join(tooltip)


except ImportError:
	import subprocess

	try:
		p = subprocess.Popen(['acpitool'], stdout=subprocess.PIPE)
	except OSError:
		raise OSError('You need either Python dbus bindings (recommended) or acpitoo ')

	data = p.communicate()[0]

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
