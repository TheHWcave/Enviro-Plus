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
from PMS5003 import PMS5003



class SENSOR_PMS5003(SENSOR_ITEM):
	"""
		Implements the PMS5003 particle matter sensor
	"""
	_pms = None
	_readings = None
	


	def Val(self):
		"""returns the raw sensor values, which are  
			PM1, PM2.5, PM10 in ug/m3  
			S0.3,S0.5,S1,S2.5,S5,S10 in particles per litre air
		"""
		return self.PM1,self.PM2_5,self.PM10,self.S0_3,self.S0_5,self.S1,self.S2_5,self.S5,self.S10
		

		
		
	def Poll(self,ts):
		""" Checks (polls) the sensor. """
		self._readings = SENSOR_PMS5003._pms.Read()
		
		# use atmospheric environment
		self.PM1.Poll(self._readings[PMS5003.PM1_AE],ts)
		self.PM2_5.Poll(self._readings[PMS5003.PM2_5_AE],ts)
		self.PM10.Poll(self._readings[PMS5003.PM10_AE],ts)
		
		self.S0_3.Poll(self._readings[PMS5003.SIZE_0_3],ts)
		self.S0_5.Poll(self._readings[PMS5003.SIZE_0_5],ts)
		self.S1.Poll(self._readings[PMS5003.SIZE_1],ts)
		self.S2_5.Poll(self._readings[PMS5003.SIZE_2_5],ts)
		self.S5.Poll(self._readings[PMS5003.SIZE_5],ts)
		self.S10.Poll(self._readings[PMS5003.SIZE_10],ts)
	
	
		return
		
	
		
  # Constructor
	def __init__(self, PM1, PM2_5,PM10,S0_3,S0_5,S1,S2_5,S5,S10):
		""" creates the object 		    
		"""
		super().__init__()
		
		if SENSOR_PMS5003._pms == None:
			SENSOR_PMS5003._pms = PMS5003()
		self.PM1		= PM1
		self.PM2_5		= PM2_5
		self.PM10		= PM10
		self.S0_3		= S0_3
		self.S0_5		= S0_5
		self.S1			= S1
		self.S2_5		= S2_5
		self.S5			= S5
		self.S10		= S10


		
class SENSOR_PMS5003_PM1(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		
	 

class SENSOR_PMS5003_PM2_5(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		
		
class SENSOR_PMS5003_PM10(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		
	 
	
class SENSOR_PMS5003_S0_3(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		
	 

class SENSOR_PMS5003_S0_5(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		
	 

class SENSOR_PMS5003_S1(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		

class SENSOR_PMS5003_S2_5(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		


class SENSOR_PMS5003_S5(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		
		
class SENSOR_PMS5003_S10(SENSOR_ITEM):
	 # Constructor
	def __init__(self):
		""" creates the object 		    
		"""
		super().__init__()
		
