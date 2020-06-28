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

"""
		Implements conversion routines
		  
"""

def Touch_to_Num(touch):
	"""
		returns the first TRUE in an array of boolean (buttons)
	"""
	res = -1
	for i,b in enumerate(touch):
		if b:
			res = i
			break
	return res
	


def Trend_to_Col(trend,pos,zero,neg):
	"""
		convert the trend value < 0 , 0, > 0 into one of 3 colours pos, zero, neg
	"""
	if trend < 0.0:
		col = neg
	elif trend > 0.0:
		col = pos
	else:
		col = zero
	return col
	
def Temp_to_Str(temp, unit='C',precision = 1):
	"""
		convert the temperature temp  assumed to be in deg. C to 
		a 4 or 5 character string in the desired unit format
		which can be deg C or Fahrenheit
		
		Note that when the value gets double-digit negative, the
		precision is reduced to ensure the string length is maintained
		despite the "-" sign 
	"""
	if unit.upper().startswith('C'):
		v = temp
	elif unit.upper().startswith('F'):
		v = 32.0+(temp*9.0)/5.0
	else:
		raise ValueError
	if v <= -10.0: precision = precision - 1 
	form = '{:4.'+str(precision)+'f}'
	
	return form.format(v)
	
def Hum_to_Str(hum, unit = None, precision = 0):
	"""
		convert the humidity assumed to be in % to string
	"""
	form = '{:2.'+str(precision)+'f}'
	return form.format(hum)
		

def Press_to_Str(press, unit='mb', precision = None):
	"""
		convert the pressure assumed to be in millibar to 
		a 4 or 5 character string in the desired unit format
		which can be mb, PSI, mmHg, inchHg
		
	"""
	if unit.upper().startswith('MB'):
		v = press
		form = '{:4.0f}'     # mB   
	elif unit.upper().startswith('MM'):
		v = press * 0.75006  # mB to mmHg  (Torr)
		form = '{:4.1f}'
	elif unit.upper().startswith('IN'):
		v = press * 0.02953  # mB to inchHg
		form = '{:4.2f}'
	elif unit.upper().startswith('PS'):
		v = press * 0.014504 # mB to PSI
		form = '{:4.2f}'
	else:
		raise ValueError
	return form.format(v)

def Gas_to_Str(gas, unit , precision = 0):
	"""
		convert the gas reading to string. If unit starts with '/' the value 
		is assumed to be a unitless ratio, otherwise in Ohm
	"""
	if unit.startswith('/'):
		form = '{:7.3f}'
	else:
		form = '{:7.0f}'
	return form.format(gas)
	
def PMS_to_Str(pms, unit = None, precision = 0):
	"""
		convert the pms reading to string. 
	"""
	return '{:7.0f}'.format(pms)
	
	
def Lux_to_Str(lux, unit = None, precision = 0):
	"""
		convert the Lux reading to string. 
	"""
	return '{:5.0f}'.format(lux)
	
def dbSPL_to_Str(dbSPL, unit = None, precision = 0):
	"""
		convert the dbSPL reading to string. 
	"""
	return '{:4.0f}'.format(dbSPL)
	
def Runtime_to_Str(now, unit = None, precision = 0):
	"""
		convert the now timestamp to string. 
	"""
	rt = int(now)
	d = int(rt / 86400)
	rt = rt - d*86400
	h = int(rt / 3600)
	rt = rt - h*3600
	m = int(rt / 60)
	s = rt - m*60
	return '{:2n} {:02n}:{:02n}:{:02n}'.format(d,h,m,s)

def OnOff_to_Str(b):
	"""
		hows Off if b is zero, On otherwise 
	
	"""
	if b == 0:
		res = 'Off'
	else:
		res = 'On '
	return res


	
def DelayTime_to_Str(dt):
	"""
		convert the delay time to string. 
		0          = 0ff
		1 ..   59  = seconds
	   60 ,, 3500  = minutes (full minutes only)
	  3600..       = hours (full hours only)
	"""
	if dt == 0:
		       
		res = ' off  '
	elif dt < 60:
		res = '{:2n} sec'.format(dt)
	elif dt < 3600:
		res = '{:2n} min'.format(int(dt/60))
	else:
		res = '{:2n} h  '.format(int(dt/3600))
	return res
