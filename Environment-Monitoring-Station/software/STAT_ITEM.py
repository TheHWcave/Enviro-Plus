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
from RINGBUFFER import RINGBUFFER



class STAT_ITEM:
	"""
		Implements the statistics package for a data item 
		
		
			  
	"""
	
	def Vnow(self):
		""" returns current value """
		return self.vnow
		
	def Vave(self):
		""" returns average """
		return self.vave
	
	def Nsamples(self):
		""" returns number of samples"""
		return self.nsamples
	
	def Trend(self,period = 'h'):
		""" returns trend: >0 = up, <0 down for the selected
			period  h = last hour, d = last day, w = last week """

		if period.lower() == 'd':
			old = self.trendd.oldest()
		elif period.lower() == 'w':
			old = self.trendw.oldest()
		else: 
			old = self.trendh.oldest()
		if old != None:
			result = self.vave - old
		else:
			result = 0
		return result

	
	
	
	def Vmax(self):
		""" returns maximum value"""
		return self.vmax
		
	def TSmax(self):
		""" returns time stamp of maximum value"""
		return self.tsmax

		
	def Vmin(self):
		""" returns minimum value"""
		return self.vmin
		
	def TSmin(self):
		""" returns time stamp of minimum value"""
		return self.tsmin

	def ResetMinMax(self):
		""" resets min max only """
		self.vmax 		= self.vnow
		self.tsmax		= self.now
		self.vmin 		= self.vnow
		self.tsmin		= self.now
		return
	

	
	def Clear(self):
		""" clears all statistics """
		self.vnow		= None
		self.vmax 		= None
		self.tsmax		= None
		self.vmin 		= None
		self.tsmin		= None
		self.vave		= None
		self.now		= None
		self.nsamples	= 0
		self.trendh.clear()
		self.trendd.clear()
		self.trendw.clear()
		return
		

	
	def AddSample(self,v,ts,restart=False):
		""" adds a new sample v taken at time ts. 
			if restart is set to True, the previous values are cleared first
		"""
		if restart:	self.Clear()
		self.vnow = v
		if self.nsamples == 0:
			self.vmax     = v
			self.tsmax    = ts
			self.vmin     = v
			self.tsmin    = ts
			self.vave     = v
			self.nsamples = 1
			self.now      = ts
			self.trendh.append(v)
			self.trendd.append(v)
			self.trendw.append(v)
		else:
			if self.vmax < v: 
				self.vmax  = v
				self.tsmax = ts
			if self.vmin > v: 
				self.vmin  = v
				self.tsmin = ts
			
			self.vave = self.alpha*v + (1 - self.alpha)*self.vave
			self.nsamples = self.nsamples + 1
				
						
			if self.nsamples % 60 == 0: 
				self.trendh.append(self.vave) # add 1 item every minute
		
			if self.nsamples % 3600 == 0:  # add 1 item every hour
				self.trendd.append(self.trendh.oldest())
			
			if self.nsamples % (3600*24) == 0: # add 1 item every day
				self.trendw.append(self.trendd.oldest())

		return
		
		
  # Constructor
	def __init__(self,alpha):
		""" creates the object
		"""
		self.alpha		= alpha
		self.trendh		= RINGBUFFER(60) # 1 item every minute for 60 minutes
		self.trendd		= RINGBUFFER(24) # 1 item every hour for 24 hours
		self.trendw		= RINGBUFFER(7)  # 1 item every day for 7 days
		self.Clear()
		
	
	
    
