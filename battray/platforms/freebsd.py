import subprocess

def sysctl(name):
	o = subprocess.Popen(['/sbin/sysctl', name], stdout=subprocess.PIPE,
		stderr=subprocess.PIPE).communicate()[0]
	(name, value) = o.split(':')
	return value.strip()

# "Old" method: use apm(8), doesn't work in amd64
#o = subprocess.Popen(['apm', '-ablt'], stdout=subprocess.PIPE).communicate()[0]
#(ac, charging, percent, lifetime) = o.split()

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

# From cpufreq(4):
# When multiple CPUs offer frequency control, they cannot be set to differ-
# ent levels and must all offer the same frequency settings.
try:
	cpufreq = sysctl('dev.cpu.0.freq')
except:
	tooltip = 'Unknown CPU frequency'
else:
	tooltip = 'CPU frequency: %sMHz' % cpufreq
