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

import RPi.GPIO as GPIO
import serial
from time import sleep



class PMS5003:
	PM1_SP   = 0  # PM1.0 in ug/m3 standard particle
	PM1_AE   = 1  # PM1.0 in ug/m3 atmospheric environment
	PM2_5_SP = 2  # PM2.5 in ug/m3 standard particle
	PM2_5_AE = 3  # PM2.5 in ug/m3 atmospheric environment
	PM10_SP  = 4  # PM10  in ug/m3 standard particle
	PM10_AE  = 5  # PM10  in ug/m3 atmospheric environment
	SIZE_0_3 = 6  # particles > 0.3 um in 1L air
	SIZE_0_5 = 7  # particles > 0.5 um in 1L air
	SIZE_1   = 8  # particles > 1   um in 1L air
	SIZE_2_5 = 9  # particles > 2.5 um in 1L air
	SIZE_5   =10  # particles > 5   um in 1L air
	SIZE_10  =11  # particles > 10  um in 1L air
	GOOD_MSGS=12  # number of good msgs 
	BAD_MSGS =13  # number of bad msgs
	
	
	_PMS 	 = None
	_Results = [0]*14
	_buf 	 = bytes(0)
	

	# def Dump(self,b):
		# print(str(len(b))+':',end='')
		# for x in b:
			# print('<'+hex(x).lstrip('0x').rjust(2,'0')+'>',end='')
		# print()


	def Read(self):
		"""
			needs to be called periodically to fetch and decode the messages send
			by the PMS5003. 
			
			returns an array of 14 values. The particle data returned is always the 
			last received good data. The health of the PMS5003 communication can be 
			checked by observing the good and bad message counters that are also 
			returned
		"""
		def ToInt(msg,offset):
			""" convert 2 bytes starting at OFFSET to an integer """
			return int.from_bytes(msg[offset:offset+2],"big")
			
		chunk = self._PMS.read(32)
		if len(chunk) > 0:
			self._buf = self._buf + chunk
		if len(self._buf) >= 32: 
			#
			# we now have enough data that a complete message should be
			# inside the buffer
			#
			mstart = self._buf.find('\x42\x4d'.encode())
			if (mstart >= 0) and (len(self._buf)+mstart >= 32):
				# remove the message from the buffer. Any bytes before
				# the message will be discarded, but any received behind
				# it will be kept as part of the next message
				msg = self._buf[mstart:mstart+32]
				self._buf = self._buf[mstart+32:]
				
				# check validity of the message
				cs = 0
				for n in msg[:-2]:
					cs = cs + n
				if cs != ToInt(msg,30):
					self._Results[self.BAD_MSGS] = self._Results[self.BAD_MSGS] + 1
				else:
					# good message: decode the data
					self._Results[self.GOOD_MSGS] = self._Results[self.GOOD_MSGS] + 1
					self._Results[self.PM1_SP   ] = ToInt(msg, 4)
					self._Results[self.PM2_5_SP ] = ToInt(msg, 6)
					self._Results[self.PM10_SP  ] = ToInt(msg, 8)
					self._Results[self.PM1_AE   ] = ToInt(msg,10)
					self._Results[self.PM2_5_AE ] = ToInt(msg,12)
					self._Results[self.PM10_AE  ] = ToInt(msg,14)
					self._Results[self.SIZE_0_3 ] = ToInt(msg,16)*10 # convert 0.1L to 1.0L
					self._Results[self.SIZE_0_5 ] = ToInt(msg,18)*10 # convert 0.1L to 1.0L
					self._Results[self.SIZE_1   ] = ToInt(msg,20)*10 # convert 0.1L to 1.0L
					self._Results[self.SIZE_2_5 ] = ToInt(msg,22)*10 # convert 0.1L to 1.0L
					self._Results[self.SIZE_5   ] = ToInt(msg,24)*10 # convert 0.1L to 1.0L
					self._Results[self.SIZE_10  ] = ToInt(msg,26)*10 # convert 0.1L to 1.0L
		return self._Results
		
	def Reset(self):
		"""
			Reset the PMS5003 and clear all data that might be in progress
		"""
		GPIO.output(self._pin_reset,GPIO.LOW)
		self._PMS.flushInput()
		self._buf = bytes(0)
		self._Results = [0] * 14
		sleep(0.1)
		GPIO.output(self._pin_reset,GPIO.HIGH)
		
	
	def Send_Cmd(self):
		m = bytearray(b'\0x42\0x4d\0xe2\0x00\0x00\0x01\0x71')
		self._PMS.write(m)
	    
	def __init__(self):
		""" setup the PMS5003 
			   
		"""
		if self._PMS == None:
			self._PMS = serial.Serial(port='/dev/serial0',
											baudrate=9600,
											timeout=0)
			self._pin_enable = 22
			self._pin_reset	= 27
			GPIO.setwarnings(False)
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(self._pin_enable, GPIO.OUT, initial=GPIO.HIGH)
			GPIO.setup(self._pin_reset, GPIO.OUT, initial=GPIO.HIGH)
	
		self._buf  = bytes(0)
		self.Reset()
		sleep(1.0)
		#self.Send_Cmd()
	
	
		
			
		

