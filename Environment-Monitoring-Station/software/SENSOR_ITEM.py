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

from datetime import datetime,timedelta 
from STAT_ITEM import STAT_ITEM



class SENSOR_ITEM:
	"""
		Implements the common interface for all sensors.
	 
		
		Sensors have the following methods:
			- Val		= return the raw sensor value
			- Stats 	= returns the sensor's statistics 
			- Poll	 	= polls the sensor to get a new value
			- Configure = allows configuration (if needed)
			
	"""
	


	def Val(self):
		"""returns the sensor value"""
		return self.ItemRVal
	
	def Stats(self):
		"""return the statistics"""
		return self.Stats
		
	def Configure(self):
		""" Configures the sensor """
		pass
		
	def Poll(self,v,ts):
		""" Checks (polls) the sensor. """
		self.ItemRVal = v
		self.Stats.AddSample(v,ts)
		return
		
	
		
  # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		
		self.ItemRVal 	= None	# raw value
		self.ItemNew 	= False	# True = new 
		self.Stats		= STAT_ITEM(alpha = 0.002)
    
