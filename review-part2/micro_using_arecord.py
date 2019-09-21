#!/usr/bin/env python

import os
import wave
import numpy as np

CMD = 'arecord -D dmic_sv -c2 -r 44100 -f S32_LE -t wav -V mono -d 5 /tmp/recording/rec.wav'
					
Done = False
while not Done:
	try:
		os.system(CMD)
		w = wave.open('/tmp/recording/rec.wav','rb')
		p = w.getparams()
		framerate = w.getframerate()
		samplewidth= w.getsampwidth()
		nframes = w.getnframes()
		#
		# read all the wav file data into sdata (array of bytes)
		sdata   = w.readframes(nframes)
		# convert to 32-bit signed integer array
		idata2ch = np.frombuffer(bytes(sdata),'<i4')
		# split into left and right channel 
		left   = idata2ch[0::2].astype(float)
		#right  = idata2ch[1::2].astype(float)
		# ignore right channel, calculate & print average, min and max values of left channel
		average = np.sum(left) /  left.size
		vmax = np.amax(left)
		vmin = np.amin(left)
		print('\n min {:+8.2f}  max {:+8.2f}  ave {:+8.2f}'.format(vmin,vmax,average))
		w.close()
	except KeyboardInterrupt:
		quit()
 



