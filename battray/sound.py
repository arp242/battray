#
# http://code.arp242.net/battray
#
# Copyright © 2008-2014 Martin Tournoij <martin@arp242.net>
# See below for full copyright
#

try:
	import wave
except ImportError:
	print('Unable to load wave module; no sound support')

# Try to load alsa first, since OSS doesn't seem to work very well on Linux
try:
	import alsaaudio
except ImportError:
	try:
		import ossaudiodev
	except ImportError:
		print('Unable to load alsaaudio or ossaudiodev module; no sound support')


def play(soundfile):
	""" Play a sound; soundfile must be .wav format """

	wav = wave.open(soundfile, 'rb')

	if globals().get('alsaaudio'):
		_alsaplay(wav)
	elif globals().get('ossaudiodev'):
		_ossplay(dev, wat)


def _ossplay(wav):
	""" Play a sound with OSS, for FreeBSD & OpenBSD """
	(nc, sw, fr, nf, comptype, compname) = wav.getparams()

	try:
		dev = ossaudiodev.open('/dev/dsp', 'w')
	except IOError:
		print('Unable to open /dev/dsp')
		print(sys.exc_info()[1])
		return

	try:
		from ossaudiodev import AFMT_S16_NE
	except ImportError:
		if byteorder == 'little': AFMT_S16_NE = ossaudiodev.AFMT_S16_LE
		else: AFMT_S16_NE = ossaudiodev.AFMT_S16_BE

	dev.setparameters(AFMT_S16_NE, nc, fr)
	data = wav.readframes(nf)
	s.close()
	dev.write(data)
	dev.close()


def _alsaplay(f):
	""" Play a sound with ALSA, for Linux """

	dev = alsaaudio.PCM(card='default')

	dev.setchannels(f.getnchannels())
	dev.setrate(f.getframerate())

	if f.getsampwidth() == 1:
		dev.setformat(alsaaudio.PCM_FORMAT_U8)
	elif f.getsampwidth() == 2:
		dev.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	elif f.getsampwidth() == 3:
		dev.setformat(alsaaudio.PCM_FORMAT_S24_LE)
	elif f.getsampwidth() == 4:
		dev.setformat(alsaaudio.PCM_FORMAT_S32_LE)
	else:
		print('Unsupported format')
		return

	dev.setperiodsize(320)
	data = f.readframes(320)
	while data:
		dev.write(data)
		data = f.readframes(320)


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
