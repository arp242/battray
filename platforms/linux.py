# Linux 2.x platform config. Requires acpitool.
#
# Send bug reports and suggestions to:
# Andy Mikhaylenko <andy@neithere.net>

import subprocess

__all__ = ['ac', 'charging', 'percent', 'lifetime', 'tooltip']

# XXX what if there are more batteries?
BATTERY = 'Battery #1'

def _parse(data):
	lines = data.split('\n')
	pairs = (x.split(':', 1) for x in lines if x)
	clean_pairs = ((k.strip(), v.strip()) for k, v in pairs)
	return dict(clean_pairs)

try:
	p = subprocess.Popen(['acpitool'], stdout=subprocess.PIPE)
except OSError:
	raise OSError('acpitool is required. Try "apt-get install acpitool" '
								'or whatever makes sense on your distro.')
data = p.communicate()[0]
info = _parse(data)

ac = info['AC adapter'] == 'on-line'

try:
	# "discharging, 83.18%, 00:31:28"
	b_status, b_percent, b_life = info[BATTERY].split(', ')
except ValueError:
	# "charged, 81.89%"
	b_status, b_percent = info[BATTERY].split(', ')
	lifetime = -1
else:
	h,m,s = (int(x) for x in b_life.split(':'))
	lifetime = h + 60*(m + 60*s)

charging = b_status == 'charging'
percent = float(b_percent[:-1])

tooltip = ''	#'Hi ;-)'
