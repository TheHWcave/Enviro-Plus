#!/usr/bin/python
#MIT License
#
#Copyright (c) 2020 TheHWcave
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#
from SENSOR_ITEM import SENSOR_ITEM
import queue
import numpy as np
import math
import sounddevice as sd


class SENSOR_MEMS(SENSOR_ITEM):
	"""
		Implements the MEMS SPH0645LM4H microphone sensor
	"""
	
	_stream  = None
	_q       = queue.Queue()
	_noise	 = 0
	_FSdbSPL = 120

			
	def Poll(self,ts):
		""" Checks (polls) the sensor. """
		
		def PCM_to_dbSPL(pcm):
			res = 0.0
			if pcm > 0:
				dbFS = 20*math.log10(pcm/0x1ffff)
				res = self._FSdbSPL +dbFS	
			return res
		
		try:
			self._raw = SENSOR_MEMS._q.get_nowait() 
			if self._noise != 0:
				NVal = PCM_to_dbSPL(self._raw - self._noise)
			else:
				NVal = self._raw
		except queue.Empty:
			NVal = 0.0

		self.ItemRVal = NVal
		self.Stats.AddSample(NVal,ts)
		return
		
			
	def Configure(self,noise=0):
		""" Configures the sensor: 
			If noise is set to a non-zero value, it is subtracted from the raw PCM
			signal before converting it to dbSPL 
			if it is zero, the sensor returns the raw PCM instead
			any change in the noise value clears the statistics 
		 """
		if noise != self._noise:
			self.Stats.Clear()
		self._noise = noise
		
	def _audio_callback(indata, frames, time, status):
		"""This is called (from a separate thread) for each audio block."""
		if status:
			print(status, file=sys.stderr)
		if any(indata):
			vmax = abs(np.amax(indata) / 0x4000)
			vmin = abs(np.amin(indata) / 0x4000)
			v = vmax if vmax > vmin else vmin
			SENSOR_MEMS._q.put(v)
	
		
  # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		self._raw = 0
		
		if SENSOR_MEMS._stream == None:
			SENSOR_MEMS._stream = sd.InputStream(device=0,
												channels=1,
												dtype='int32',
												samplerate=16000,
												blocksize=16000,
												callback=SENSOR_MEMS._audio_callback)
			SENSOR_MEMS._stream.start()
	
# Destructor
	def __del__(self):
		if SENSOR_MEMS._stream != None:
			SENSOR_MEMS._stream.stop()
    
