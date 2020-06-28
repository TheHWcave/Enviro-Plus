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

class PICK_ITEM:
	"""
		Implements a simple pick list 
		
		
			  
	"""

		
	@property
	def Next(self):
		"""
			returns the next item from the list, wrap around if neeeded
		"""
		self._idx = (self._idx + 1) % len(self._itemlist)
		return self._itemlist[self._idx]

	@property
	def Prev(self):
		"""
			returns the previous item from the list, wrap around if neeeded
		"""
		if self._idx > 0:
			self._idx = self._idx - 1
		else:
			self._idx = len(self._itemlist)
		return self._itemlist[self._idx]

		
	@property
	def Current(self):
		"""
			returns the current item from the list
		"""
		return self._itemlist[self._idx]
		
	def Set(self,val):
		"""
			allows selecting the item by value (which must be
			in the list already)
		"""
		found = False
		for i,n in enumerate(self._itemlist):
			if n == val:
				self._idx = i
				found = True
				break
		if not found:
			raise ValueError
			
  # Constructor
	def __init__(self,itemlist):
		""" creates the object
		"""
		self._itemlist = itemlist
		self._idx	   = 0
		
	
	
    
