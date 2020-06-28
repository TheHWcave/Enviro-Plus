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

from board import *
from adafruit_bus_device.i2c_device import I2CDevice
from time import sleep


MPR121_TOUCH_STATUS		= 0x00	# 2 x 8 bit registers
MPR121_OOR0				= 0x02	# 2 x 8 bit registers
MPR121_EFD0LB			= 0x04	# 12 x 2 x 8 bit  (LSB then MSB) for 0..11 electrodes
MPR121_E0BV				= 0x1E	# 12 x 8 bit for 0..11 electrodes
MPR121_EPROXBV 			= 0x2A	# 1 x 8 bit 

MPR121_MHDR				= 0x2B	# 1 x 8 bit 
MPR121_NHDR				= 0x2C	# 1 x 8 bit 
MPR121_NCLR				= 0x2D	# 1 x 8 bit 
MPR121_FDLR				= 0x2E	# 1 x 8 bit 
MPR121_MHDF				= 0x2F	# 1 x 8 bit 
MPR121_NHDF				= 0x30	# 1 x 8 bit 
MPR121_NCLF				= 0x31	# 1 x 8 bit 
MPR121_FDLF				= 0x32	# 1 x 8 bit 
MPR121_NHDT				= 0x33	# 1 x 8 bit 
MPR121_NCLT				= 0x34	# 1 x 8 bit 
MPR121_FDLT				= 0x35	# 1 x 8 bit 

MPR121_MHDPROXR			= 0x36	# 1 x 8 bit 
MPR121_NHDPROXR			= 0x37	# 1 x 8 bit 
MPR121_NCLPROXR			= 0x38	# 1 x 8 bit 
MPR121_FDLPROXR			= 0x39	# 1 x 8 bit 
MPR121_MHDPROXF			= 0x3A	# 1 x 8 bit 
MPR121_NHDPROXF			= 0x3B	# 1 x 8 bit 
MPR121_NCLPROXF			= 0x3C	# 1 x 8 bit 
MPR121_FDLPROXF			= 0x3D	# 1 x 8 bit 
MPR121_NHDPROXT			= 0x3E	# 1 x 8 bit 
MPR121_NCLPROXT			= 0x3F	# 1 x 8 bit 
MPR121_FDLPROXT			= 0x40	# 1 x 8 bit 

MPR121_E0TTH			= 0x41	# 12 x 2 x 8 bit  (Touch then Release) for 0..11 electrodes
MPR121_EPROXTTH			= 0x59	# 2 x 8 bit  (Touch then Release) 
MPR121_DRDT				= 0x5B	# 1 x 8 bit  
MPR121_CDC				= 0x5C	# 1 x 8 bit  
MPR121_CDT				= 0x5D	# 1 x 8 bit  
MPR121_ECR				= 0x5E	# 1 x 8 bit  
MPR121_CDC0				= 0x5F	# 12 x 8 bit  for 0..11 electrodes
MPR121_CDCPROX			= 0x6B	# 1 x 8 bit
MPR121_CDT0				= 0x6C	# 6 x 8 bit  for 0..11 electrodes (2 electrodes per register)
MPR121_CDTPROX			= 0x72	# 1 x 8 bit 

MPR121_GPIO_CTRL0 		= 0x73	# 1 x 8 bit  
MPR121_GPIO_CTRL1 		= 0x74	# 1 x 8 bit  
MPR121_GPIO_DATA	 	= 0x75	# 1 x 8 bit  
MPR121_GPIO_DIRECTION 	= 0x76	# 1 x 8 bit  
MPR121_GPIO_ENABLE 		= 0x77	# 1 x 8 bit  
MPR121_GPIO_DATASET 	= 0x78	# 1 x 8 bit  
MPR121_GPIO_DATACLEAR	= 0x79	# 1 x 8 bit  
MPR121_GPIO_DATATOGGLE	= 0x7A	# 1 x 8 bit  

MPR121_AUTO_CTRL0		= 0x7B	# 1 x 8 bit  
MPR121_AUTO_CTRL1		= 0x7C	# 1 x 8 bit  
MPR121_AUTO_USL			= 0x7D	# 1 x 8 bit  
MPR121_AUTO_LSL			= 0x7E	# 1 x 8 bit  
MPR121_AUTO_TL			= 0x7F	# 1 x 8 bit  
MPR121_SRST				= 0x80	# 1 x 8 bit

class MPR121:
	_mpr121 = None


		
	def _write_list(self,reg, regval):
		d = bytearray(1+len(regval))
		d[0] = reg
		d[1:] = regval
		MPR121._mpr121.write(bytes(d))
		return None
		
	def _read_reg(self,reg):
		d = bytearray(1)
		MPR121._mpr121.write_then_readinto(bytes([reg]),d)
		return d[0]
		
			
	def _read_list(self,reg,size):
		d = bytearray(size)
		MPR121._mpr121.write_then_readinto(bytes([reg]),d)
		return d

	
	def _save_writereg(self,reg, regval):
		if (reg == MPR121_ECR) or (
			(reg >= MPR121_GPIO_CTRL0) and (reg <= MPR121_GPIO_DATATOGGLE)):
			self._write_list(reg,regval)  # can write directly 
		else:
			oldECR = self._read_reg(MPR121_ECR)
			if oldECR != 0x00:
				MPR121._mpr121.write(bytes([MPR121_ECR,0x00])) # stop MPR121
			self._write_list(reg,regval)
			if oldECR != 0x00:
				MPR121._mpr121.write(bytes([MPR121_ECR,oldECR])) # restore (start) MPR121
		return None
		
	
	
		
		
	def Touched(self):
		"""
			Returns the touch status of all 13 electrodes as a binary number
			
		"""
		v = self._read_list(MPR121_TOUCH_STATUS,2)
		r = (v[1] << 8) | v[0]
		return r
		
	def Filtered(self):
		"""
			Returns the touch status of all 13 electrodes as a binary number, 
			followed by a list of filtered electrode capacitance values
			for all 13 electrodes
			
		"""
		v = self._read_list(MPR121_TOUCH_STATUS,30)
		ts = (v[1] << 8) | v[0]
		#oor = (v[3] << 8) | v[2]
		ef = [0]*13
		for e in range(13):
			ef[e] = (v[5+2*e] << 8) | v[4+2*e]
		return ts,ef
		
	def ReadThresholds(self):
		"""
			Returns the threshold settings as a list for 13 electrodes
			each setting is a pair: touch threshold and release threshold
			touch must always be > release 
			
		"""
		return self._read_list(MPR121_E0TTH,26)
	
	def ReadFilterSettings(self):
		"""
			Returns the filter settings for electrodes
			The values are: 
			MHDR, NHDR, NCLR, FDLR, MHDF, NHDF,NCLF, FDLF, NHDT, NCLT, FDLT
			
		"""
		return self._read_list(MPR121_MHDR,11)
		
	def ReadConfig(self):
		"""
			Returns 4 configuration registers: 
			- DRDT (debounce touch & release)
			- Filter/Global CDC config 1
			- Filter/Global CDC config 2
			- Electrode config
		"""
		return self._read_list(MPR121_DRDT,4)
		
	def ReadAutoConfig(self):
		"""
			Returns 5 auto configuration registers: 
			- Autoconfig control 0 
			- Autoconfig control 1
			- Autoconfig USL
			- Autoconfig LSL
			- Autoconfig Target Level
		"""
		return self._read_list(MPR121_AUTO_CTRL0,5)
		
	def ReadOOR(self):
		"""
			Returns auto configuration out-of-range status: 
			- should be all zero if successful 
		"""
		v = self._read_list(MPR121_OOR0,2)
		oor = (v[1] << 8) | v[0]
		return oor
		
		
	def SetTouchReleaseThreshold(self, el,t,r):
		"""
			Set the touch and release thresholds for a specific 
			electrode 
				el  = electrode 0.. 12
				t   = touch threshold  0..255
				r   = release threshold 0..255 
				
				note: t should always be greater than r
		"""
		if (el >= 0) and (el <=12):
			th = [t & 0xff,r & 0xff]
			self._save_writereg(MPR121_E0TTH+2*el,th)
	
		
	def SetProxMode(self, mode):
		"""
			Set the proximity mode (virtual 13th electrode) 
			mode:   0 = disabled
					1 = use EL0 to EL1   for proximity 
					2 = use EL0 to EL3   for proximity
					3 = use EL0 to EL11  for proximity
		"""
		ELEPROX_EN = (mode & 3) << 4
		ECR = self._read_reg(MPR121_ECR)
		ECR = (ECR & 0xCF)        # clear old prox. mode
		ECR = (ECR | ELEPROX_EN)  # set new prox. mode
		MPR121._mpr121.write(bytes([MPR121_ECR,0x00])) # stop chip
		MPR121._mpr121.write(bytes([MPR121_ECR,ECR ])) # update & start chip
		
		
	def AutoConfig(self, VDD = 3.3):
		"""
			Run autoconfig. This is done automatically during init. It 
			should not be necesary to call it again
		"""
		USL  = int(((VDD - 0.7) * 256) / VDD)       # upper autoconf. limit, see equation 8 in AN3889
		TL   = int(((VDD - 0.7) * 256 * 0.9) / VDD) # target baseline, see AN3889
		LSL  = int(((VDD - 0.7) * 256 * 0.65) / VDD) # lower autoconf. limit, see AN3889
		
		self._save_writereg(MPR121_SRST,[0x63])	# soft reset MPR121 just in case
		sleep(0.01)
		self._save_writereg(MPR121_ECR,[0x00]) 	# stop MPR121
		
			 	 #      0     1     2     3     4     5     6     7     8     9    10    11    PROX
		thresholds = [12, 6,12, 6,12, 6,12, 6,12, 6,12, 6,12, 6,12, 6,12, 6,12, 6,12, 6,12, 6,12, 6]
		
		self._save_writereg(MPR121_E0TTH,thresholds) 
		
		
		filtering = [0x01,  # MHDR (max half delta rising)
					 0x01,  # NHDR (noise half delta rising)
					 0x0E,  # NCLR (noise count limit rising) 
					 0x00,  # FDLR (filter delay count limit rising) 
					 0x01,  # MHDF (max half delta falling)
					 0x05,  # NHDF (noise half delta falling)
					 0x01,  # NCLF (noise count limit falling) 
					 0x00,  # FDLF (filter delay count limit falling) 
					 0x00,  # MHDT (max half delta touched)
					 0x00,  # NHDT (noise half delta touched)
					 0x00] #,  # NCLT (noise count limit touched) 
					 #0x00]  # FDLT (filter delay count limit touched) 
		self._save_writereg(MPR121_MHDR,filtering) 
		self._save_writereg(MPR121_MHDPROXR,filtering) 
	
		self._save_writereg(MPR121_DRDT,[0x00]) # debounce
		
		self._save_writereg(MPR121_CDC,[0x10]) # charge current = 16 uA
		self._save_writereg(MPR121_CDT,[0x20]) # 0.5 uS encoding, 1ms period
		
		self._save_writereg(MPR121_AUTO_USL,[USL]) 	# 202 for VDD 3.3V
		self._save_writereg(MPR121_AUTO_TL ,[TL]) 	# 182 for VDD 3.3V
		self._save_writereg(MPR121_AUTO_LSL,[LSL]) 	# 131 for VDD 3.3V
		self._save_writereg(MPR121_AUTO_CTRL0,[0x0b]) 	#  set autoconf
		
		self._save_writereg(MPR121_ECR,[0x8F]) 	# start MPR121
		
		return


	def __init__(self,i2c, VDD = 3.3, address = 0x5a):
		""" setup the MPR121 as a singelton with defaults
			   VDD is the supply voltage for the MPR121 chip
			   i2c_address is its address on the I2C bus
			   
		"""
		if MPR121._mpr121 == None:
			MPR121._mpr121 = I2CDevice(i2c,address)
			
		self.AutoConfig(VDD)
			
		

