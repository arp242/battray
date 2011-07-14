#!/usr/bin/env python
#

import sys

# Only works on Linux and FreeBSD
try:
	import ossaudiodev
except ImportError:
	print 'Unable to load ossaudiodev module'
	print sys.exc_info()[1]
	sys.exit(1)

try:
	import wave
except ImportError:
	print 'Unable to load wave module'
	print sys.exc_info()[1]
	sys.exit(1)

def PlaySound(soundfile):
	"""
	Play a sound.
	"""

	s = wave.open(soundfile, 'rb')
	(nc, sw, fr, nf, comptype, compname) = s.getparams()

	try:
		dsp = ossaudiodev.open('/dev/dsp', 'w')
	except IOError:
		print 'Unable to open /dev/dsp'
		print sys.exc_info()[1]
		sys.exit(1)

	try:
		from ossaudiodev import AFMT_S16_NE
	except ImportError:
		if byteorder == 'little':
			AFMT_S16_NE = ossaudiodev.AFMT_S16_LE
		else:
			AFMT_S16_NE = ossaudiodev.AFMT_S16_BE

	dsp.setparameters(AFMT_S16_NE, nc, fr)
	data = s.readframes(nf)
	s.close()
	dsp.write(data)
	dsp.close()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print '  Usage: %s file.wav' % sys.argv[0]
		sys.exit(1)

	PlaySound(sys.argv[1])
