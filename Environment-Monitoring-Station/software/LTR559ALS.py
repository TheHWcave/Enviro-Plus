#!/usr/bin/env python3
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

import busio
from board import *
from adafruit_bus_device.i2c_device import I2CDevice

from time import sleep







class LTR559ALS:
	_als = None

	_REG_ALS_CONTR			= 0x80  # ALS operation mode control SW reset
	_REG_PS_CONTR 	 		= 0x81	# PS operation mode control 
	_REG_PS_LED 			= 0x82	# PS LED setting 
	_REG_PS_N_PULSES 		= 0x83	# PS number of pulses 
	_REG_PS_MEAS_RATE		= 0x84	# PS measurement rate in active mode 
	_REG_ALS_MEAS_RATE 		= 0x85	# ALS measurement rate in active mode 
	_REG_PART_ID 			= 0x86	# Part Number ID and Revision ID
	_REG_MANUFAC_ID 		= 0x87	# Manufacturer ID
	_REG_ALS_DATA_CH1_0 	= 0x88	# ALS measurement CH1 data, lower byte 
	_REG_ALS_DATA_CH1_1 	= 0x89	# ALS measurement CH1 data, upper byte 
	_REG_ALS_DATA_CH0_0 	= 0x8A	# ALS measurement CH0 data, lower byte 
	_REG_ALS_DATA_CH0_1 	= 0x8B	# ALS measurement CH0 data, upper byte 
	_REG_ALS_PS_STATUS 		= 0x8C	# ALS and PS new data status 
	_REG_PS_DATA_0 			= 0x8D	# PS measurement data, lower byte 
	_REG_PS_DATA_1 			= 0x8E	# PS measurement data, upper byte 
	_REG_INTERRUPT 			= 0x8F	# Interrupt settings 
	_REG_PS_THRES_UP_0 		= 0x90	# PS interrupt upper threshold, lower byte
	_REG_PS_THRES_UP_1 		= 0x91	# PS interrupt upper threshold, upper byte 
	_REG_PS_THRES_LOW_0 	= 0x92	# PS interrupt lower threshold, lower byte
	_REG_PS_THRES_LOW_1 	= 0x93	# PS interrupt lower threshold, upper byte 
	_REG_PS_OFFSET_1 		= 0x94	# PS offset, upper byte 
	_REG_PS_OFFSET_0 		= 0x95	# PS offset, lower byte 
	_REG_ALS_THRES_UP_0 	= 0x97	# ALS interrupt upper threshold, lower byte 
	_REG_ALS_THRES_UP_1 	= 0x98	# ALS interrupt upper threshold, upper byte 
	_REG_ALS_THRES_LOW_0 	= 0x99	# ALS interrupt lower threshold, lower byte
	_REG_ALS_THRES_LOW_1 	= 0x9A	# ALS interrupt lower threshold, upper byte 
	_REG_INTERRUPT_PERSIST	= 0x9E	# ALS / PS Interrupt persist setting
	
	
					#                            Lux    
					#  Gain      contr bits   min    max
	_Gain_LOOKUP	= { 1     : [0b00000000,  1.0,  64000],
						2     : [0b00000100,  0.5,  32000],
						4     : [0b00001000,  0.25, 16000],
						8     : [0b00001100,  0.125, 8000],
					   48     : [0b00011000,  0.02,  1300],
					   96     : [0b00011100,  0.01,   600]}
	_Gain_CLEAR		=            0b11100011
	
						#  Gain      contr bits   min    max
	_Status_to_Gain	= [ [1 ,  1.0,  64000],  # 0
						[2 ,  0.5,  32000],  # 1
						[4 ,  0.25, 16000],  # 2
						[8 ,  0.125, 8000],  # 3
						[0 ,  0,     0   ],  # 4 = invalid
						[0 ,  0,     0   ],  # 5 = invalid
					    [48,  0.02,  1300],  # 6
					    [96,  0.01,   600]]  # 7 

              
					#  IntTime  bits 
	_IntTime_LOOKUP	= { 0.05  : 0b00_001_000,
					    0.1   : 0b00_000_000,
					    0.15  : 0b00_100_000,
					    0.2   : 0b00_010_000,
					    0.25  : 0b00_101_000,
					    0.3   : 0b00_110_000,
					    0.35  : 0b00_111_000,
					    0.4   : 0b00_011_000}
	_IntTime_CLEAR = 			0b11_000_111
	
              
					#  ALS RATE   bits 
	_ALSRate_LOOKUP	= { 0.05  : 0b00_000_000,
					    0.1   : 0b00_000_001,
					    0.2   : 0b00_000_010,
					    0.5   : 0b00_000_011,
					    1.0   : 0b00_000_100,
					    2.0   : 0b00_000_101}
					    
	_ALSRate_CLEAR = 			0b11_111_000
	
	
	
	
	
	
	def _write_reg(self,reg, regval):
		d = bytearray(2)
		d[0] = reg
		d[1] = regval
		LTR559ALS._als.write(bytes(d))
		return None
		
	def _write_list(self,reg, regval):
		d = bytearray(1+len(regval))
		d[0] = regval
		d[1:] = regval
		LTR559ALS._als.write(bytes(regval))
		return None
		
	def _read_reg(self,reg):
		d = bytearray(1)
		LTR559ALS._als.write_then_readinto(bytes([reg]),d)
		return int(d[0])
		
	def _read_word(self,reg):
		d = bytearray(2)
		LTR559ALS._als.write_then_readinto(bytes([reg]),d)
		result = int.from_bytes(d,"little")
		return result

	
	
	def ALS_Raw(self):
		"""
			read the raw values from the ALS
		"""
		status = self._read_reg(self._REG_ALS_PS_STATUS)
		ch1  = self._read_word(self._REG_ALS_DATA_CH1_0)
		ch0  = self._read_word(self._REG_ALS_DATA_CH0_0)
		
		valid = (status & 0x80) == 0
		gv    = (status & 0x70) >> 4
		gain  = self._Status_to_Gain[gv][0]
		
		
		
		return valid, gain, ch0, ch1
	
	def _Raw_To_Lux(self, gain, ch0, ch1):
		"""
			convert raw measurement to Lux in accordance with 
			Appendix A of the datasheet 
		"""
		WINFAC =self._WinFac
		ALS_INT = 10*(self._IntTime)
		ALS_GAIN= 1.0 *gain
		result = 0
		if ch0+ch1 != 0:
			ratio = ch1/(ch0+ch1)
			if ratio < 0.45:
				result = (1.7743 * ch0 + 1.1059 * ch1) * (WINFAC/ALS_GAIN/ALS_INT)
			elif ratio < 0.64:
				result = (4.2785 * ch0 - 1.9548 * ch1) * (WINFAC/ALS_GAIN/ALS_INT)
			elif ratio < 0.85:
				result = (0.5926 * ch0 + 0.1185 * ch1) * (WINFAC/ALS_GAIN/ALS_INT)
			else:
				result = 0
		return result
	
	def Lux(self):
		"""
			returns the ambient light in LUX. 
			reports 0 if overflow (because of too high gain)
		"""
		valid, gain, ch0, ch1 = self.ALS_Raw()
		result = 0
		if valid:
			result = self._Raw_To_Lux(gain, ch0, ch1)
			self._LastValidLux = result
		return result
	
	def AutoLux(self):
		valid, gain, ch0, ch1 = self.ALS_Raw()
		result = 0
		if valid:
			# see if we can find a more sensitive gain
			# for the next measurement but use the current one for now
			newGain = 0
			result = self._Raw_To_Lux(gain, ch0, ch1)
			self._LastValidLux = result
			for g in self._Gain_LOOKUP:
				if result < self._Gain_LOOKUP[g][2]:
					newGain = g
				else:
					break
			if newGain > 0:
				self.Set_ALS_Gain(newGain)
		else:
			# use gain 1 to get new measurement (next time)
			# use the last valid measurement for now
			self.Set_ALS_Gain(1)
			result = self._LastValidLux
		return result
	
	def PS_Raw(self):
		"""
			returns proximity value in range from 0 to 2047
		"""
		ps = self._read_word(self._REG_PS_DATA_0)
		saturated = (ps & 0x8000) == 0x8000
		ps = ps & 0x07FF
		return ps
		
	def Set_ALS_Measurement_Rate(self,rate,inttime):
		"""
			set the ALS measurement rate (0.05, 0.1, 0.2, 0.5, 1, 2 seconds and
			integration time (0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4 seconds
			inttime must be less or equal to measurment time. If necessary inttime is changed 
		"""
		if rate in self._ALSRate_LOOKUP:
			if inttime in self._IntTime_LOOKUP:
				if rate < inttime:
					self._inttime = rate # make integration time equal to rate
				self._ALSRate = rate
				self._IntTime = inttime
				
				regval = self._IntTime_LOOKUP[self._IntTime] | self._ALSRate_LOOKUP[self._ALSRate]
				
				self._write_reg(self._REG_ALS_MEAS_RATE, regval) 
			else:
				raise ValueError('unsupported integration time')
		else:
			raise ValueError('unsupported measurement rate')
			
	def Set_ALS_Gain(self,gain):
		"""
			sets the gain for the ALS
			range 1,2,4,8, 48,96  
		"""
		if gain in self._Gain_LOOKUP:
			regval = self._read_reg(self._REG_ALS_CONTR)
			regval = (regval & self._Gain_CLEAR) | self._Gain_LOOKUP[gain][0]
			self._write_reg(self._REG_ALS_CONTR,regval) 
			
	
	def __init__(self,i2c, rate=0.2, inttime=0.2, winfac = 1.0, address = 0x23 ):
		""" setup the LTR559ALS with specified measurement rate and integration time
			winfac is the factor to compensate light loss due to aperture or window above the device
			1.0 = no window above = pure die
			
			i2c_address is its address on the I2C bus
			   
		"""
		if LTR559ALS._als == None:
			LTR559ALS._als = I2CDevice(i2c,address)
			
			mid = self._read_reg(self._REG_MANUFAC_ID)
			if mid == 0x05:
				pid = self._read_reg(self._REG_PART_ID)
				if pid != 0x92:
					raise ValueError('unknown part id'+hex(pid))
			else:
				raise ValueError('unknown manufacturer id'+hex(mid))
					
		
		self._write_reg(self._REG_ALS_CONTR,0x01)   # ALS active mode
		self._write_reg(self._REG_PS_CONTR,0x03)    # PS active mode

		self.Set_ALS_Measurement_Rate(rate, inttime)
		self.Set_ALS_Gain(1)
		self._WinFac = winfac
		self._LastValidLux = 0
			
		

