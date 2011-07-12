# From apm(8):
# -a Display the external charger (A/C status).  0 means disconnected, 1
# means connected, 2 means backup power source, and 255 means unknown.
#
# -b Display the battery status.  0 means high, 1 means low, 2 means
# critical, 3 means charging, 4 means absent, and 255 means unknown.
#
# -l Display the estimated battery lifetime (in percent).
#
# -m Display the estimated battery lifetime (in minutes).
#

import subprocess

def sysctl(name):
	o = subprocess.Popen(['/sbin/sysctl', name], stdout=subprocess.PIPE,
		stderr=subprocess.PIPE).communicate()[0]
	(name, value) = o.split('=')
	return value

o = subprocess.Popen(['/usr/sbin/apm', '-alm'], stdout=subprocess.PIPE).communicate()[0]
(percent, lifetime, ac) = o.split()

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

# Add apm(8)/apmd(8) status on CPU throttling
o = subprocess.Popen(['/usr/sbin/apm'], stdout=subprocess.PIPE).communicate()[0]
tooltip = o.split('\n')[2]
