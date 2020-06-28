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
import adafruit_bme280  



class SENSOR_BME280(SENSOR_ITEM):
	"""
		Implements the BME280 pressure and humitity sensor
	"""
	
	
	


	def Val(self):
		"""returns the raw sensor values, which are three real with the 
			temperature in deg C
			pressure in mBar
			Humidity in %
		"""
		return self.NValTemp,self.NValPress,self.NValHum
		

		
		
	def Poll(self,ts):
		""" Checks (polls) the sensor. """
		self.NValTemp  = self._bme280.temperature
		self.NValHum   = self._bme280.humidity
		self.NValPress = self._bme280.pressure
		
		self.Press.Poll(self.NValPress,ts)
		self.Hum.Poll(self.NValHum,ts)
		self.Temp.Poll(self.NValTemp,ts)

		return
		
	
		
  # Constructor
	def __init__(self,i2c, Press,Hum,Temp):
		""" creates the object 		    
		"""
		super().__init__()
		
		self._bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c,address =0x76)

		self.Press = Press
		self.Hum   = Hum
		self.Temp  = Temp
		
		self.NValTemp	= None
		self.NValPress	= None
		self.NValHum	= None
		
		
class SENSOR_BME280_PRESSURE(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		

class SENSOR_BME280_HUMIDITY(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()


class SENSOR_BME280_BME_TEMP(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
