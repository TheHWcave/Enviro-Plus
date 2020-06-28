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
from LTR559ALS import LTR559ALS

class SENSOR_LTR559(SENSOR_ITEM):
	"""
		Implements the LTR559 LUX and Proximity  sensor
	"""
	_LTR = None
				
	
	def Val(self):
		"""returns the raw sensor values, which are two reals
			LUX and Proximity (0..1023)
		"""
		return self.LUX.Val(),self.PROX.Val()
		

		
		
	def Poll(self,ts):
		""" Checks (polls) the sensor. """

		self.LUX.Poll(SENSOR_LTR559._LTR.AutoLux(),ts)
		self.PRX.Poll(SENSOR_LTR559._LTR.PS_Raw(),ts)
		return
		
	
		
  # Constructor
	def __init__(self,i2c, LUX,PRX):
		""" creates the object 		    
		"""
		super().__init__()
		
		if SENSOR_LTR559._LTR == None:
			
			SENSOR_LTR559._LTR = LTR559ALS(i2c,address = 0x23)

	
		self.LUX		= LUX
		self.PRX		= PRX

		
class SENSOR_LTR559_LUX(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		
 
class SENSOR_LTR559_PRX(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		
  
	


