#
# http://code.arp242.net/battray
#
# Copyright © 2008-2015 Martin Tournoij <martin@arp242.net>
# See below for full copyright
#

import logging, sys, wave


def play(soundfile, method=None):
	""" Play a sound; soundfile must be .wav format """

	logging.info('Playing {}'.format(soundfile))
	if not soundfile.endswith('.wav'): soundfile += '.wav'

	wav = wave.open(soundfile, 'rb')

	try:
		if method is not None:
			method(wav)
		else:
			for method in [_ossplay, _alsaplay]:
				if method(wav) != False:
					break
			else:
				logging.warning('Unable to play sound')
	finally:
		wav.close()


def _ossplay(wav):
	""" Play a sound with OSS, for FreeBSD & OpenBSD """
	
	try:
		import ossaudiodev
	except ImportError:
		logging.info("_ossplay: Unable to load ossaudiodev module")
		return False

	(nc, sw, fr, nf, comptype, compname) = wav.getparams()

	try:
		dev = ossaudiodev.open('/dev/dsp', 'w')
	except IOError:
		logging.info("_ossplay: Unable to open /dev/dsp; `{}'".format((sys.exc_info()[1])))
		return False

	try:
		from ossaudiodev import AFMT_S16_NE
	except ImportError:
		if byteorder == 'little': AFMT_S16_NE = ossaudiodev.AFMT_S16_LE
		else: AFMT_S16_NE = ossaudiodev.AFMT_S16_BE

	try:
		dev.setparameters(AFMT_S16_NE, nc, fr)
		data = wav.readframes(nf)
		s.close()
		dev.write(data)
	finally:
		dev.close()


def _alsaplay(f):
	""" Play a sound with ALSA, for Linux """

	try:
		import alsaaudio
	except ImportError:
		logging.info("_alsaaudio: Unable to load alsaaudio module")
		return False

	dev = alsaaudio.PCM()
	try:
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

		dev.setperiodsize(320)
		data = f.readframes(320)
		while data:
			dev.write(data)
			data = f.readframes(320)
	finally:
		dev.close()


# The MIT License (MIT)
#
# Copyright © 2008-2015 Martin Tournoij
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
