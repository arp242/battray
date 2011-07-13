#!/usr/bin/env python
#
# Sound from:
# http://www.freesound.org/samplesViewSingle.php?id=122989
#

import sys

# Only works on Linux and FreeBSD
try:
	import ossaudiodev
	import wave
except ImportError:
	sys.exit(1)

def PlaySound(soundfile):
	"""
	Play a sound.
	"""

	s = wave.open(soundfile, 'rb')
	(nc, sw, fr, nf, comptype, compname) = s.getparams()
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

if __name__ == '__main__':
	PlaySound(sys.argv[1])
