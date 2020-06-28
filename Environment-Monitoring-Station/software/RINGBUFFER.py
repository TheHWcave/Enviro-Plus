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
class RINGBUFFER:
	"""
		Implements a ring buffer
		based on an idea by Sébastien Keim in O'Reilly Python Cookbook by Alex Martelli, David Ascher
		https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s19.html
		
		modified to remove the class switching since we need a clear method as well and
		implemented a method to get ONLY the oldest element 
			
	"""
	def __init__(self,size_max):
		self.max = size_max
		self.data = []
		self.cur  = 0 
		
	def append(self,x):
		"""Append an element, overwriting the oldest"""
		if len(self.data) < self.max:
			self.data.append(x)
			self.cur = 0
		else:
			self.data[self.cur] = x
			self.cur = (self.cur + 1) % self.max
	
	def getall(self):
		""" return a list of elements in correct order"""
		if len(self.data) < self.max:
			return self.data
		else:
			return self.data[self.cur:]+self.data[:self.cur]
		
		
	def oldest(self):
		""" returns the oldest element but it is NOT removed"""
		if len(self.data) < self.max:
			if len(self.data) > 0:
				return self.data[0]
			else:
				return None
		else:
			return self.data[self.cur]
			
	def clear(self):
		""" empties the buffer of all data """
		self.data = []
		self.cur = 0
	
	
