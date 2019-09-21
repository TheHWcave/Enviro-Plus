#!/usr/bin/env python

import pyaudio
import numpy as np
	
RATE  = 44100
CHUNK = 44100
CHANNEL=1
audio = pyaudio.PyAudio()

print('++++++++ default host api info +++++++')
info = audio.get_default_host_api_info()
print(info)
print('++++++++ default input device info +++++++')
print(audio.get_default_input_device_info())
print('++++++++ device count +++++++')
print(audio.get_device_count())
print('++++++++ host api count +++++++')
print(audio.get_host_api_count())

for n in range(audio.get_host_api_count()):
	print('==== host api count:'+str(n))
	print(audio.get_host_api_info_by_index(n))
for n in range(audio.get_device_count()):
	print('==== host api 0 device count:'+str(n))
	print(audio.get_device_info_by_host_api_device_index(0,n)) 


stream = audio.open(format=pyaudio.paInt32, 
					input_device_index = 4,
					channels = CHANNEL,
					rate = RATE,
					input = True,
					frames_per_buffer=CHUNK)

Seconds = 0
Done = False
while not Done:
	try:
		sdata = stream.read(CHUNK)
		if Seconds >=2:
			fdata = np.frombuffer(bytes(sdata),'<i4').astype(float)
			if Seconds == 2:
				average = np.sum(fdata) /  fdata.size
				print(average)
			else:
				vmax = np.amax(fdata) - average
				vmin = np.amin(fdata) - average
				rmax = vmax / float(0x7FFFFFFF)
				rmin = vmin / float(0x7FFFFFFF)
				print('  {:+5.2f} {:+5.2f} :'.format(rmax,rmin),end='')
				for n in range(10):
					c = '.'
					if rmax >= n/10: c= '#'
					print(c,end='')
				print('\r',end='')
		Seconds = Seconds + 1


	except KeyboardInterrupt:
		print()
		stream.stop_stream()
		stream.close()
		audio.terminate()
		quit()
 



