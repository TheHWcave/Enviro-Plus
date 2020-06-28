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

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

import RPi.GPIO as GPIO



class SENSOR_MICS6814(SENSOR_ITEM):
	"""
		Implements the MICS6814 GAS  sensor
	"""
	
	
	_MICS6814_HEATER_PIN = 24

	_ads : None
	_GAIN_to_VALUE = {2/3 : [6.144, 10_000_000],
					    1 : [4.096,  6_000_000],
					    2 : [2.048,  6_000_000],
					    4 : [1.024,  3_000_000],
					    8 : [0.512,100_000_000],
					   16 : [0.256,100_000_000]}
					   
	_VALUE_to_GAIN = {0.256: [16, 100_000_000],
				      0.512: [ 8, 100_000_000],
				      1.024: [ 4,   3_000_000],
				      2.048: [ 2,   6_000_000],
				      4.096: [ 1,   6_000_000],
				      6.144: [2/3, 10_000_000]}
					      

	def Val(self):
		"""returns the raw sensor values, which are three real 
			OX, RED, NH3 
			resistance in ohms
		"""
		return self.OX.Val(),self.RED.Val(),self.NH3.Val()
		

		
		
	def Poll(self,ts):
		""" Checks (polls) the sensor. """
		def AutoVolts(ch):
			self._ads.gain = self._VALUE_to_GAIN[4.096][0]
			v  = self._input[ch].voltage
			Ri = self._VALUE_to_GAIN[4.096][1]
			if abs(v) < 0.25:
				self._ads.gain = self._VALUE_to_GAIN[0.256][0]
				Ri = self._VALUE_to_GAIN[0.256][1]
				v = self._input[ch].voltage
			elif abs(v) < 0.5:
				self._ads.gain = self._VALUE_to_GAIN[0.512][0]
				Ri = self._VALUE_to_GAIN[0.512][1]
				v = self._input[ch].voltage	
			elif abs(v) < 1.0:
				self._ads.gain = self._VALUE_to_GAIN[1.024][0]
				Ri = self._VALUE_to_GAIN[1.024][1]
				v = self._input[ch].voltage	
			elif abs(v) < 2:
				self._ads.gain = self._VALUE_to_GAIN[2.048][0]
				Ri = self._VALUE_to_GAIN[2.048][1]
				v = self._input[ch].voltage	
			return v,Ri
		
		def read_MOS(ch):
			v, Ri = AutoVolts(ch)
			return 1.0/ ((1.0/((v * 56000.0) / (3.3 - v))) - (1.0 / Ri))

		self._OX.Poll(read_MOS(0),ts)
		self._RED.Poll(read_MOS(1),ts)
		self._NH3.Poll(read_MOS(2),ts)

		return
		
	
		
  # Constructor
	def __init__(self,i2c, OX,RED,NH3):
		""" creates the object 		    
		"""
		super().__init__()
		
		# Create the ADC object using the I2C bus
		self._ads = ADS.ADS1015(i2c,address =0x49)
		self._ads.mode =  Mode.CONTINUOUS
		self._input = [AnalogIn(self._ads,0),
					   AnalogIn(self._ads,1),
					   AnalogIn(self._ads,2),
					   AnalogIn(self._ads,3)]

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self._MICS6814_HEATER_PIN, GPIO.OUT)
		GPIO.output(self._MICS6814_HEATER_PIN, 1)

		self._OX	= OX
		self._RED	= RED
		self._NH3 	= NH3



# Destructor
	def __del__(self):
		GPIO.setup(self._MICS6814_HEATER_PIN, GPIO.OUT)
		GPIO.output(self._MICS6814_HEATER_PIN, 0)
		
class SENSOR_MICS6814_OX(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		self._R0  = None

		
	def Configure(self,R0 = None):
		""" Configures the sensor: 
			If R0 is set to a positive non-zero ohm value, the sensor delivers a dimensionless ratio 
			otherwise it returns the raw sensor value in Ohms. 
			Changing from ratio to ohm or back also resets the statistics
		 """
		if R0 == None:
			if self._R0 != None:  # switch to ohms
				self._R0 = None
				self.Stats.Clear()
		elif R0 > 0:
			if self._R0 == None: # switch to ratio 
				self.Stats.Clear()
			self._R0 = R0
				

    
	def Poll(self,v,ts):
		""" Checks (polls) the sensor. """
		if self._R0 != None:
			nv = v / self._R0
		else:
			nv = v
		self.ItemRVal = nv
		self.Stats.AddSample(nv,ts)
		return
	
class SENSOR_MICS6814_RED(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		self._R0  = None

	def Configure(self,R0 = None):
		""" Configures the sensor: 
			If R0 is set to a positive non-zero ohm value, the sensor delivers a dimensionless ratio 
			otherwise it returns the raw sensor value in Ohms. 
			Changing from ratio to ohm or back also resets the statistics
		 """
		if R0 == None:
			if self._R0 != None:  # switch to ohms
				self._R0 = None
				self.Stats.Clear()
		elif R0 > 0:
			if self._R0 == None: # switch to ratio 
				self.Stats.Clear()
			self._R0 = R0

	def Poll(self,v,ts):
		""" Checks (polls) the sensor. """
		if self._R0 != None:
			nv = v / self._R0
		else:
			nv = v
		self.ItemRVal = nv
		self.Stats.AddSample(nv,ts)
		return

class SENSOR_MICS6814_NH3(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		self._R0	= None

	def Configure(self,R0 = None):
		""" Configures the sensor: 
			If R0 is set to a positive non-zero ohm value, the sensor delivers a dimensionless ratio 
			otherwise it returns the raw sensor value in Ohms. 
			Changing from ratio to ohm or back also resets the statistics
		 """
		if R0 == None:
			if self._R0 != None:  # switch to ohms
				self._R0 = None
				self.Stats.Clear()
		elif R0 > 0:
			if self._R0 == None: # switch to ratio 
				self.Stats.Clear()
			self._R0 = R0

	def Poll(self,v,ts):
		""" Checks (polls) the sensor. """
		if self._R0 != None:
			nv = v / self._R0
		else:
			nv = v
		self.ItemRVal = nv
		self.Stats.AddSample(nv,ts)
		return
