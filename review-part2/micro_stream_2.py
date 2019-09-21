#!/usr/bin/env python
import pyaudio
import numpy as np

RATE  = 22000
CHUNK = 5500
CHANNEL=1
audio = pyaudio.PyAudio()

print('++++++++ default host api info +++++++')
info = audio.get_default_host_api_info()

stream = audio.open(format=pyaudio.paInt32, 
					input_device_index = info['defaultInputDevice'],
					channels = CHANNEL,
					rate = RATE,
					input = True,
					frames_per_buffer=CHUNK)

MSec = 0
Sum = 0.0
Cnt = 0
Done = False
while not Done:
	try:
		sdata = stream.read(CHUNK)
		if MSec >=2000:
			fdata = np.frombuffer(bytes(sdata),'<i4').astype(float)
			if MSec <= 3000:
				Sum = Sum + np.sum(fdata)
				Cnt = Cnt + fdata.size
				average = Sum /  Cnt
				print('average: '+ str(average))
			else:
				vmax = np.amax(fdata) - average
				vmin = np.amin(fdata) - average
				rmax = (vmax / float(0x7FFFFFFF)) * 50.0
				rmin = (vmin / float(0x7FFFFFFF)) * 50.0
				print('  {:+5.2f} {:+5.2f} :'.format(rmin,rmax),end='')
				for n in range(20):
					c = '.'
					if rmax >= n/20: c= '#'
					print(c,end='')
				print('\r',end='')
		MSec = MSec + 250

	except KeyboardInterrupt:
		print()
		stream.stop_stream()
		stream.close()
		audio.terminate()
		quit()
 



