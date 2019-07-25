#!/usr/bin/env python
#MIT License
#
#Copyright (c) 2019 TheHWcave
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
import ads1015
from time import sleep, time, localtime,strftime,perf_counter
from BME280_new import BME280_new
from pms5003 import PMS5003, ReadTimeoutError

try:
	from smbus2 import SMBus
except ImportError:
	from smbus import SMBus


MICS6814_HEATER_PIN = 24
ads1015.I2C_ADDRESS_DEFAULT = ads1015.I2C_ADDRESS_ALTERNATE

adc = ads1015.ADS1015(i2c_addr=0x49)
adc.set_mode('single')
adc.set_programmable_gain(4.096)
adc.set_sample_rate(128)

bus = SMBus(1)
bme280 = BME280_new(i2c_dev=bus)
bme280.setup(mode='forced',
			temperature_oversampling=1,
			pressure_oversampling=1,
			humidity_oversampling=1)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(MICS6814_HEATER_PIN, GPIO.OUT)
GPIO.output(MICS6814_HEATER_PIN, 1)

pms5003 = PMS5003()
sleep(1.0)

def read_ADS(ch):
	if ch < 3:
		channel_name = 'in'+chr(48+ch)+'/gnd'
	else:
		channel_name = 'ref/gnd'
	adc.set_programmable_gain(4.096)
	Ri = 6000000
	v = adc.get_voltage(channel_name)
	if v <= 1.0: 
		adc.set_programmable_gain(1.024)
		v = adc.get_voltage(channel_name)
		Ri = 3000000
	elif v <= 2.0:
		adc.set_programmable_gain(2.048)
		v = adc.get_voltage(channel_name)
		Ri = 6000000
	return v, Ri

def read_MOS(ch):
	v, Ri = read_ADS(ch)
	return 1.0/ ((1.0/((v * 56000.0) / (3.3 - v))) - (1.0 / Ri))

def read_Temp(ch):
	v, Ri = read_ADS(ch)
	return 100.0 * (v - 0.5)
	
	

(temperature,pressure,humidity)= bme280.update_sensor()
tmp2 = read_Temp(3)
bme280.set_ambient_temperature(tmp2) 
print('1st correction: BME280 temp by {:05.2f} deg'.format(tmp2-temperature))
		
out_name = 'LOG_'+strftime('%Y%m%d%H%M%S',localtime())+'.csv'
f = open(out_name,'w')
f.write('Seconds,Tmp2, Tmp, Pres, Hum, PM1.0, PM2.5, PM10, S0.3, S0.5, S1.0, S2.5, S5, S10, Ox,Red,NH3\n')



try:
	start = perf_counter()
	while True:
		ox  = read_MOS(0) 
		red = read_MOS(1)
		NH3 = read_MOS(2)
		tmp2 = read_Temp(3)
		(temperature,pressure,humidity)= bme280.update_sensor()
		bme280.set_ambient_temperature(tmp2) 
		
		Done = False
		while not Done:
			try:
				readings = pms5003.read()
				Done = True
			except ReadTimeoutError:
				pms5003 = PMS5003()
		
		pm2p5 = readings.pm_ug_per_m3(2.5,atmospheric_environment=True)
		pm1   = readings.pm_ug_per_m3(1.0,atmospheric_environment=True)
		pm10  = readings.pm_ug_per_m3(None,atmospheric_environment=True)
		
		s0p3 = readings.pm_per_1l_air(0.3)
		s0p5 = readings.pm_per_1l_air(0.5)
		s1p0 = readings.pm_per_1l_air(1.0)
		s2p5 = readings.pm_per_1l_air(2.5)
		s5   = readings.pm_per_1l_air(5)
		s10  = readings.pm_per_1l_air(10)
		
		now = perf_counter() - start
		f.write('{:06.1f},'.format(now))
		f.write('{:05.2f},'.format(tmp2))
		f.write('{:05.2f},'.format(temperature))
		f.write('{:05.2f},'.format(pressure))
		f.write('{:05.2f},'.format(humidity))
		f.write('{:03d},'.format(pm1))
		f.write('{:03d},'.format(pm2p5))
		f.write('{:03d},'.format(pm10))
		f.write('{:5d},'.format(s0p3))
		f.write('{:5d},'.format(s0p5))
		f.write('{:5d},'.format(s1p0))
		f.write('{:5d},'.format(s2p5))
		f.write('{:5d},'.format(s5))
		f.write('{:5d},'.format(s10))
		f.write('{:10.2f},'.format(ox))
		f.write('{:10.2f},'.format(red))
		f.write('{:10.2f}\n'.format(NH3))
		
		print('time stamp          {: >10.1f} Sec'.format(now))
		print('ext temperature     {: >10.2f} degC'.format(tmp2))
		print('BME280 temperature  {: >10.2f} degC'.format(temperature))
		print('BME280 pressure     {: >10.1f} mbar'.format(pressure))
		print('BME280 humitity     {: >10.2f}%'.format(humidity))
		print('Oxidizing           {: >10.0f} Ohm'.format(ox))
		print('Reducing            {: >10.0f} Ohm'.format(red))
		print('Ammonia             {: >10.0f} Ohm'.format(NH3))
		print('PM1.0               {: >10d} ug/m3'.format(pm1))
		print('PM2.5               {: >10d} ug/m3'.format(pm2p5))
		print('PM10                {: >10d} ug/m3'.format(pm10))
		print('particles >0.3um    {: >10d}'.format(s0p3))
		print('particles >0.5um    {: >10d}'.format(s0p5))
		print('particles >1.0um    {: >10d}'.format(s1p0))
		print('particles >2.5um    {: >10d}'.format(s2p5))
		print('particles >5um      {: >10d}'.format(s5))
		print('particles >10um     {: >10d}'.format(s10))
		print('\n\n\n')
		
		
		
		sleep(1.0)
except KeyboardInterrupt:
	f.close()
	GPIO.output(MICS6814_HEATER_PIN, 0)
	pass
