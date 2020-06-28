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
import board
import busio
import RPi.GPIO as GPIO
from time import sleep, time, localtime,strftime,perf_counter
import ST7735
from PIL import Image, ImageDraw, ImageFont
from Conv import *
import json


# import adafruit_mpr121 
from MPR121 import MPR121    # comment out to use the Adafruit MPR121 instead

from SENSOR_MCP9808 import SENSOR_MCP9808
from SENSOR_BME280 import SENSOR_BME280, SENSOR_BME280_PRESSURE, SENSOR_BME280_HUMIDITY, SENSOR_BME280_BME_TEMP
from SENSOR_MICS6814 import SENSOR_MICS6814, SENSOR_MICS6814_OX, SENSOR_MICS6814_RED, SENSOR_MICS6814_NH3
from SENSOR_LTR559 import SENSOR_LTR559, SENSOR_LTR559_LUX, SENSOR_LTR559_PRX
from SENSOR_MEMS import SENSOR_MEMS
from SENSOR_PMS5003 import (SENSOR_PMS5003, SENSOR_PMS5003_PM1,SENSOR_PMS5003_PM2_5,SENSOR_PMS5003_PM10,
						   SENSOR_PMS5003_S0_3,SENSOR_PMS5003_S0_5,SENSOR_PMS5003_S1,SENSOR_PMS5003_S2_5,SENSOR_PMS5003_S5,SENSOR_PMS5003_S10)

from STAT_ITEM import STAT_ITEM
from PICK_ITEM import PICK_ITEM

import sys,os,subprocess
HOMEDIR 	= '/home/pi/EnviroStation/'
i2c = busio.I2C(board.SCL, board.SDA)

BEEPER = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BEEPER, GPIO.OUT, initial=GPIO.LOW)

# Create LCD class instance.
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=90,
    spi_speed_hz=10000000
)

#mpr121 = adafruit_mpr121.MPR121(i2c,address =0x5a)
mpr121 = MPR121(i2c,address =0x5a)  # this is for the self-made driver
mpr121.SetProxMode(3)               # and so is this

font52 = ImageFont.truetype(HOMEDIR+"ttf/UbuntuMono-Regular.ttf", 52)
font40 = ImageFont.truetype(HOMEDIR+"ttf/UbuntuMono-Regular.ttf", 40)
font26 = ImageFont.truetype(HOMEDIR+"ttf/UbuntuMono-Regular.ttf", 26)
font20 = ImageFont.truetype(HOMEDIR+"ttf/UbuntuMono-Regular.ttf", 20)
font16 = ImageFont.truetype(HOMEDIR+"ttf/UbuntuMono-Regular.ttf", 16)

RED   	= (255,  0,  0)
GREEN  	= (  0,255,  0)
BLUE 	= (  0,  0,255)
YELLOW	= (255,255,  0)
CYAN	= (  0,255,255)
MAGENTA	= (255,  0,255)
SILVER	= (192,192,192)
GREY  	= (128,128,128)
MAROON	= (128,  0,  0)
OLIVE	= (128,128,  0)
DGREEN	= (  0,128,  0)
PURPLE	= (128,  0,128)
TEAL	= (  0,128,128)
DBLUE	= (  0,  0,128)
BLACK 	= (  0,  0,  0)
WHITE 	= (255,255,255)

STAND	= 0
TREND	= 1
now		= 0.0

WIDTH = disp.width
HEIGHT = disp.height

img = Image.new('RGB', (WIDTH, HEIGHT), color=BLACK)
ImageDraw.Draw(img).rectangle([0,0,159,79],BLACK,None,0)

def Write(txt,start,font,col,maxlen=None):
		""" write the string in txt to the image at position start using the 
			specified font and foreground colour
			if maxlen is None, it erases as much as the string needs 
			if maxlen is specified, it erases up to the specified length
		"""
		t = txt
		if maxlen != None:
			t = t.ljust(maxlen)
		size_x, size_y = ImageDraw.Draw(img).textsize(t, font)
		box = [start[0],start[1],start[0]+size_x,start[1]+size_y]
		ImageDraw.Draw(img).rectangle(box,BLACK,None,0)
		ImageDraw.Draw(img).text((start[0],start[1]),txt,font=font, fill=col)



Sens_TEMP 	 	  	= SENSOR_MCP9808(i2c)

Sens_PRESS 			= SENSOR_BME280_PRESSURE()
Sens_HUM 			= SENSOR_BME280_HUMIDITY()
Sens_BME_TEMP 		= SENSOR_BME280_BME_TEMP()
Sens_BME 			= SENSOR_BME280(i2c, Sens_PRESS,Sens_HUM, Sens_BME_TEMP)

Sens_GAS_OX  		= SENSOR_MICS6814_OX()
Sens_GAS_RED 		= SENSOR_MICS6814_OX()
Sens_GAS_NH3 		= SENSOR_MICS6814_OX()
Sens_GAS	 		= SENSOR_MICS6814(i2c, Sens_GAS_OX,Sens_GAS_RED,Sens_GAS_NH3)

Sens_PMS_PM1  		= SENSOR_PMS5003_PM1()
Sens_PMS_PM2_5 		= SENSOR_PMS5003_PM2_5()
Sens_PMS_PM10  		= SENSOR_PMS5003_PM10()
Sens_PMS_S0_3 		= SENSOR_PMS5003_S0_3()
Sens_PMS_S0_5  		= SENSOR_PMS5003_S0_5()
Sens_PMS_S1    		= SENSOR_PMS5003_S1()
Sens_PMS_S2_5  		= SENSOR_PMS5003_S2_5()
Sens_PMS_S5    		= SENSOR_PMS5003_S5()
Sens_PMS_S10   		= SENSOR_PMS5003_S10()
Sens_PMS	   		= SENSOR_PMS5003(Sens_PMS_PM1,Sens_PMS_PM2_5,Sens_PMS_PM10,
							  Sens_PMS_S0_3,Sens_PMS_S0_5,Sens_PMS_S1,Sens_PMS_S2_5,Sens_PMS_S5,Sens_PMS_S10)

Sens_OPT_LUX 		= SENSOR_LTR559_LUX()
Sens_OPT_PRX 		= SENSOR_LTR559_PRX()
Sens_OPT			= SENSOR_LTR559(i2c, Sens_OPT_LUX,Sens_OPT_PRX)

Sens_SPL			= SENSOR_MEMS()



# to index the configuration record


					# 76543210
					# xxxxxxxx  
					#     ^^^^
					#     |||+- Trend : 0 = Trend off, 1 = Trend display
					#     ||+-- AVE   : 0 = average off, 1 = average display
					#     |+--- RECVAL: 0 = value not recorded, 1= value recorded
					#     +---- RECAVE: 0 = average not recorded, 1= average recorded
DCONF_OPT_TREND		= 0x01  
DCONF_OPT_AVE		= 0x02
DCONF_OPT_RECVAL	= 0x04
DCONF_OPT_RECAVE	= 0x08

DCONF_OPT			= 0		# column index into configuration record for the display options
DCONF_NAME			= 1		# column index into configuration record for the display name
DCONF_HIS			= 2		# column index into configuration record for the trend history depth
DCONF_UNIT			= 3		# column index into configuration record for the unit selected

# row index into the configuration record. One entry for each sensor
DCONF_TEMP			= 0
DCONF_PRESS			= 1
DCONF_HUM			= 2
DCONF_GAS_OX		= 3
DCONF_GAS_RED		= 4
DCONF_GAS_NH3		= 5
DCONF_PM1			= 6
DCONF_PM2_5			= 7
DCONF_PM10			= 8
DCONF_TIME			= 9
DCONF_S0_3			= 10
DCONF_S1			= 11
DCONF_S2_5			= 12
DCONF_S10			= 13
DCONF_LUX			= 14
DCONF_SPL			= 15


# the configuration record for every sensor
#
#              DCONF_    DCONF_ DCONF_  DCONF_
#              OPT       NAME   HIS     UNIT 
Dconf		= [[0,		'T[C]'	,'h'	,'C'],     # DCONF_TEMP
			   [0,		'P[mB]'	,'h'	,'mb  '],  # DCONF_PRESS
			   [0,		'Hum%'	,'h'	,'%'],     # DCONF_HUM
			   [0,		'OX'	,'h'	,'/OX'],   # DCONF_GAS_OX
			   [0,		'RED'	,'h'	,'/RED'],  # DCONF_GAS_RED
			   [0,		'NH3'	,'h'	,'/NH3'],  # DCONF_GAS_NH3
			   [0,		'PM1'	,'h'	,'PM1'],   # DCONF_PM1
			   [0,		'PM2.5'	,'h'	,'PM2.5'], # DCONF_PM2_5
			   [0,		'PM10'	,'h'	,'PM10'],  # DCONF_PM10
			   [0,		'Time'	,'h'	,'Time'],  # DCONF_TIME
			   [0,		'S0.3'	,'h'	,'S0.3'],  # DCONF_S0_3
			   [0,		'S1'	,'h'	,'S1'],    # DCONF_S1
			   [0,		'S2.5'	,'h'	,'S2.5'],  # DCONF_S2_5
			   [0,		'S10'	,'h'	,'S10'],   # DCONF_S10
			   [0,		'Lux'	,'h'	,'Lux'],   # DCONF_LUX
			   [0,		'Sound'	,'h'	,'dbSPL']] # DCONF_SPL

# list of all sensor group codes. Note the first 8 are identical to 
# the button codes. If that is no longer the case in the future, the 
# button and sensor look-up tables need to be separated.
#
SEN_TEMP	= 0
SEN_WEATH	= 1
SEN_GAS		= 2
SEN_PMS_PM	= 3
SEN_TIME	= 4
SEN_LUX		= 5
SEN_SPL		= 6
SEN_PMS_S	= 7

# list of all button codes. Note that the first 8 are identical to 
# the sensor groups. If that is no longer the case in the future, the 
# button and sensor look-up tables need to be separated. 
#
BUT_TEMP 	= 0
BUT_WEATH 	= 1
BUT_GAS		= 2
BUT_PMS_PM	= 3
BUT_TIME	= 4
BUT_LUX		= 5
BUT_SPL		= 6
BUT_PMS_S	= 7
BUT_SHIFT	= 8
BUT_MENU	= 9
BUT_CYC_NXT = 10
BUT_REC_PRV	= 11


# look-up table to associate a button code to up to 4 configuration 
# entries. This is only meant for button codes corresponding to a sensor
# group and SEN_TO_CONF exploits this as well (see below) 
#
# the number of conf eentries in this list corresponds to the actual
# sensors in each sensor group

BUT_TO_CONF = {BUT_TEMP: [DCONF_TEMP,-1,-1,-1],
			   BUT_WEATH:[DCONF_PRESS,DCONF_HUM,-1,-1],
			   BUT_GAS: [DCONF_GAS_OX,DCONF_GAS_RED,DCONF_GAS_NH3,-1],
			   BUT_PMS_PM: [DCONF_PM1,DCONF_PM2_5,DCONF_PM10,-1],
			   BUT_TIME: [DCONF_TIME,-1,-1,-1],
			   BUT_LUX: [DCONF_LUX,-1,-1,-1],
			   BUT_SPL: [DCONF_SPL,-1,-1,-1],
			   BUT_PMS_S: [DCONF_S0_3,DCONF_S1, DCONF_S2_5, DCONF_S10]}
			   
# since the first 8 button codes have the same meaning and values as the 
# sensor groups, we can use the same lookup table. If, in the future that 
# is no longer true, SEN_TO_CONF will need its own definition here but 
# at least the rest of the code does not need to change

SEN_TO_CONF	= BUT_TO_CONF

#
# look-up table to associate a sensor group to a name 
#
SEN_TO_NAME	= {SEN_TEMP  : 'Temp',
		       SEN_WEATH : 'T+H+B',
			   SEN_GAS	 : 'Gas',
			   SEN_PMS_PM: 'PM PM',
			   SEN_TIME	 : 'Time',
			   SEN_LUX	 : 'Light',
			   SEN_SPL	 : 'Sound',
			   SEN_PMS_S : 'PM S'}


#
# look-up table to find the sensor belonging to a configuration entry
#
CONF_TO_SENS={DCONF_TEMP	: Sens_TEMP,
			  DCONF_PRESS   : Sens_PRESS,
			  DCONF_HUM		: Sens_HUM,
			  DCONF_GAS_OX  : Sens_GAS_OX,
			  DCONF_GAS_RED	: Sens_GAS_RED,
			  DCONF_GAS_NH3	: Sens_GAS_NH3,
			  DCONF_PM1		: Sens_PMS_PM1,
			  DCONF_PM2_5	: Sens_PMS_PM2_5,
			  DCONF_PM10	: Sens_PMS_PM10,
			  DCONF_TIME	: None,
			  DCONF_S0_3	: Sens_PMS_S0_3,
			  DCONF_S1		: Sens_PMS_S1,
			  DCONF_S2_5	: Sens_PMS_S2_5,
			  DCONF_S10		: Sens_PMS_S10,
			  DCONF_LUX		: Sens_OPT_LUX,
			  DCONF_SPL		: Sens_SPL}
   
DISP_SENS = 0 # index to the sensor object
DISP_CONF = 1 # index to the configuration object
DISP_CONV = 2 # index to the conversion function for values
DISP_VFNT = 3 # index to the font for showing the value
DISP_VPOS = 4 # index to the display x/y coordinates for showing the value
DISP_VPRE = 5 # index to the precision used for value conversion
DISP_UFNT = 6 # index to the font for showing the unit
DISP_UPOS = 7 # index to the display x/y coordinates for showing the unit

#                                                               DISP_   DISP_  DISP_ DISP_   DISP_               
#                DISP_SENS      DISP_CONF       DISP_CONV	    VFNT    VPOS   VPRE  UFNT    UPOS  
Sensor_Disp = [[[Sens_TEMP, 	DCONF_TEMP, 	Temp_to_Str,	font52,[  0, 0],2, font20, [  0, 52]]],		# Temperature
			   [[Sens_TEMP, 	DCONF_TEMP, 	Temp_to_Str,	font40,[  0, 0],1, font20, [ 80, 20]],		# Temperature + Humidity + Pressure
				[Sens_HUM,  	DCONF_HUM,  	Hum_to_Str, 	font40,[100, 0],0, font20, [140, 20]],    
				[Sens_PRESS,	DCONF_PRESS,	Press_to_Str,	font40,[  0,40],0, font20, [100, 60]]],
			   [[Sens_GAS_OX,	DCONF_GAS_OX, 	Gas_to_Str,		font26,[ 60, 0],0, font26, [  0,  0]],		# GAS
				[Sens_GAS_RED,	DCONF_GAS_RED, 	Gas_to_Str,		font26,[ 60,26],0, font26, [  0, 26]],
				[Sens_GAS_NH3,	DCONF_GAS_NH3, 	Gas_to_Str,		font26,[ 60,52],0, font26, [  0, 52]]],
			   [[Sens_PMS_PM1,	DCONF_PM1,	 	PMS_to_Str,		font26,[ 52, 0],0, font26, [  0,  0]],		# PM in ug/m3
				[Sens_PMS_PM2_5,DCONF_PM2_5, 	PMS_to_Str,		font26,[ 52,26],0, font26, [  0, 26]],
				[Sens_PMS_PM10,	DCONF_PM10, 	PMS_to_Str,		font26,[ 52,52],0, font26, [  0, 52]]],
			   [[None,			DCONF_TIME,	 	None,			font26,[  0, 0],0, font26, [  0, 26]]],		# time and runtime
			   [[Sens_OPT_LUX,	DCONF_LUX,	 	Lux_to_Str,		font40,[  0, 0],0, font40, [  0, 40]]],		# Lux
			   [[Sens_SPL,		DCONF_SPL,	 	dbSPL_to_Str,	font40,[  0, 0],0, font40, [  0, 40]]],		# dbSPL
			   [[Sens_PMS_S0_3,	DCONF_S0_3,	 	PMS_to_Str,		font20,[ 50, 0],0, font20, [  0,  0]],		# PM in um/L
				[Sens_PMS_S1,	DCONF_S1,	 	PMS_to_Str,		font20,[ 50,20],0, font20, [  0, 20]],
				[Sens_PMS_S2_5,	DCONF_S2_5, 	PMS_to_Str,		font20,[ 50,40],0, font20, [  0, 40]],
				[Sens_PMS_S10,	DCONF_S10, 		PMS_to_Str,		font20,[ 50,60],0, font20, [  0, 60]]]
				]

TEMP_Pick	 = PICK_ITEM(['C','F'])
PRESS_Pick	 = PICK_ITEM(['mb  ','mmHg','inHg','PSI '])
SPL_Pick	 = PICK_ITEM(['dbSPL','PCM  '])
HIS_Pick	 = PICK_ITEM(['h','d','w'])

SHOW_VAL = 0
SHOW_MIN = 1
SHOW_MAX = 2
Show_TEMP_Pick   = PICK_ITEM([SHOW_VAL,SHOW_MIN,SHOW_MAX])
Show_WEATH_Pick  = PICK_ITEM([SHOW_VAL,SHOW_MIN,SHOW_MAX])
Show_GAS_Pick    = PICK_ITEM([SHOW_VAL,SHOW_MIN,SHOW_MAX])
Show_PMS_PM_Pick = PICK_ITEM([SHOW_VAL,SHOW_MIN,SHOW_MAX])
Show_TIME_Pick   = PICK_ITEM([SHOW_VAL,SHOW_MIN,SHOW_MAX])
Show_LUX_Pick    = PICK_ITEM([SHOW_VAL,SHOW_MIN,SHOW_MAX])
Show_SPL_Pick    = PICK_ITEM([SHOW_VAL,SHOW_MIN,SHOW_MAX])
Show_PMS_S       = PICK_ITEM([SHOW_VAL,SHOW_MIN,SHOW_MAX])
Show_Opt_Pick = [Show_TEMP_Pick,  
                 Show_WEATH_Pick, 
                 Show_GAS_Pick,   
                 Show_PMS_PM_Pick,
                 Show_TIME_Pick,  
                 Show_LUX_Pick,   
                 Show_SPL_Pick,   
                 Show_PMS_S ]




MENU_NONE 	= 0
MENU_UNIT 	= 1
MENU_AVE  	= 2
MENU_TREND	= 3
MENU_HIS  	= 4
MENU_RECVAL = 5
MENU_RECAVE = 6
MENU_RECTIM = 7
MENU_SLEEPT = 8
MENU_SAVE 	= 9
MENU_LOAD 	= 10
MENU_LAST	= 10
MenuSel     = MENU_NONE


CalGAS_R0 	= [25000,250000,250000]
CalSPL_NOISE= 6666

RECTIME_CHOICES = [1,10,30,60,300,600,900,3600]
RecTimeIx	= 0  # index to RECTIME_CHOICE 

SLEEPTIME_CHOICES = [0,30,60,300]
SleepTimeIx	= 3  # index to SLEEPTIME_CHOICE

CycleTime   = 10 # seconds



def SaveSetup():
	"""
		a very simple dump of the configuration data using json
	"""
	fo = open(HOMEDIR+'SETUP.TXT','w')
	setup = [CalGAS_R0,
			 CalSPL_NOISE,
			 RecTimeIx,
			 SleepTimeIx,
			 Dconf]
	fo.write(json.dumps(setup))
	fo.close()
	
def LoadSetup():
	"""
		Load the configuration from file and set the configuration 
		accordingly
	
	"""
	global Dconf
	global CalGAS_R0
	global CalSPL_NOISE
	global RecTimeIx
	global SleepTimeIx
	
	Success = False
	try:
		with open(HOMEDIR+'SETUP.TXT','r') as fi:
			for line in fi:
				setup = json.loads(line)
				Success = True
	except FileNotFoundError:
		print('error loading setup',file=sys.stderr)

	if Success:
		CalGAS_R0 	 = setup[0]
		CalSPL_NOISE = setup[1]
		RecTimeIx	 = setup[2]
		SleepTimeIx	 = setup[3]
		Dconf 	  	 = setup[4]

	# the R0 values for the 3 Gas sensors are loaded and the
	# unit is automatically switched back to / = ratio  
	# to use them.

	Sens_GAS_OX.Configure(R0=CalGAS_R0[0])
	Sens_GAS_RED.Configure(R0=CalGAS_R0[1])
	Sens_GAS_NH3.Configure(R0=CalGAS_R0[2])
	Dconf[DCONF_GAS_OX][DCONF_UNIT]  = '/OX'
	Dconf[DCONF_GAS_RED][DCONF_UNIT] = '/RED'
	Dconf[DCONF_GAS_NH3][DCONF_UNIT] = '/NH3'
	
	
	
	# the noise floor level is loaded and the unit is 
	# automatically switched back to dbSPL to use it
	#
	Sens_SPL.Configure(noise =CalSPL_NOISE)
	Dconf[DCONF_SPL][DCONF_UNIT] = 'dbSPL'
	SPL_Pick.Set('dbSPL')
	
	# for all other unit selections, need to set the pick lists 
	# to whatever was last used and is now restored. 
	TEMP_Pick.Set(Dconf[DCONF_TEMP][DCONF_UNIT])
	PRESS_Pick.Set(Dconf[DCONF_PRESS][DCONF_UNIT])
	
	# restore picklist for trend history based on whatever was last
	# used and is now restored
	for d in Dconf:
		HIS_Pick.Set(d[DCONF_HIS])
	
	
	return Success


def ShowSensor(sel):
	"""
		sel contains the selected sensor group (index into Sensor_Disp) 
		except for SEN_TIME, which isn't really a proper sensor, everything
		is configured in Sensor_Disp, including how many lines are written and 
		the font. 
	"""
	for item in Sensor_Disp[sel]:
		sens = item[DISP_SENS]
		conf = Dconf[item[DISP_CONF]]
		conv = item[DISP_CONV]
		vfnt = item[DISP_VFNT]
		vpos = item[DISP_VPOS]
		vpre = item[DISP_VPRE]
		ufnt = item[DISP_UFNT]
		upos = item[DISP_UPOS]
		if sel == SEN_TIME:
			#
			# Time is treated special because there is no Sensor Item attached
			# to it
			#
			Write(strftime('  %H:%M:%S',localtime()),vpos,vfnt,WHITE)
			Write(Runtime_to_Str(now),upos,ufnt,WHITE)
			if isLogging:
				Write('recording',[0, 52],font26,RED)
			else:
				Write('not rec.',[0, 52],font26,WHITE)
			
		else:
			#
			# all (actual) sensors can be treated generically 
			# 
			# they all show a value and a unit 
			#
			# the flags are checked to determine:
			# 	* if the value should be the real-time value, the average, 
			#     the minimum or the maximum
			#	* the colour of the value and unit
			#
			if Show_Opt_Pick[sel].Current == SHOW_MIN:
				vcol = BLUE
				ucol = BLUE
				vstr = vstr = conv(sens.Stats.Vmin(),unit = conf[DCONF_UNIT], precision = vpre)
			elif Show_Opt_Pick[sel].Current == SHOW_MAX:
				vcol = RED
				ucol = RED
				vstr = vstr = conv(sens.Stats.Vmax(),unit = conf[DCONF_UNIT], precision = vpre)
			else:
				# determine value colour based on trend setting and trend 
				if (conf[DCONF_OPT] & DCONF_OPT_TREND)== DCONF_OPT_TREND:
					vcol = Trend_to_Col(sens.Stats.Trend(conf[DCONF_HIS]),RED,WHITE,BLUE) 
				else:
					vcol = WHITE
				# unit colour and value string based on average setting
				if (conf[DCONF_OPT] & DCONF_OPT_AVE) == DCONF_OPT_AVE:
					vstr = conv(sens.Stats.Vave(),unit = conf[DCONF_UNIT], precision = vpre)
					ucol = GREEN
				else:
					vstr = conv(sens.Val(),unit = conf[DCONF_UNIT], precision = vpre)
					ucol = WHITE
			Write(vstr,vpos,vfnt,vcol)
			Write(conf[DCONF_UNIT],upos,ufnt,ucol)
				
def Menu(MSel, SSel, touch):
	"""
		Handles the Menu. The current submenu is in MSel, the 
		selected sensor in SSel and touch contains which button has 
		been pressed. 
		
		Note. This function is only called when a button has been pressed 
		and MSel is not MENU_NONE
		
	"""
	def ConfBitChange(p1,p2,SSel,mask,OnCol=WHITE):
		"""
			Handles the submenus for Average, Trend, RecVal and RecAve.
			
			The treatment for these is basically identical except for 
			the prompt and the configuration bit mask.
		"""
		res = False
		Write(p1,[0, 0],font20,WHITE)
		Write(p2,[0,20],font20,WHITE)
		cx = SEN_TO_CONF[SSel]
		sname = SEN_TO_NAME[SSel]
		Write('{:<5s}'.format(sname+':'),[0,52],font26,WHITE)
		if (Dconf[cx[0]][DCONF_OPT] & mask) == mask:
			Write(' on',[94,52],font26,OnCol)
		else:
			Write('off',[94,52],font26,WHITE)
		if touch[BUT_SHIFT]:
			Dconf[cx[0]][DCONF_OPT] = Dconf[cx[0]][DCONF_OPT] ^ mask
			if (Dconf[cx[0]][DCONF_OPT] & mask) == mask:
				Write(' on',[94,52],font26,OnCol)
			else:
				Write('off',[94,52],font26,WHITE)
			# copy new config setting to all related items
			for c in cx[1:]:
				if c >= 0:
					Dconf[c][DCONF_OPT] = Dconf[cx[0]][DCONF_OPT]
			res = True
		return res
			
	
	global RecTimeIx
	global SleepTimeIx
	
	Done = False
	# the while loop and the DONE flag are needed to "paint" the next 
	# or prev menu.
	# The function is only called when a button is pressed, so
	# when a submenu is finished, the screen would remain dark until 
	# the next button is pressed. The one extra iteration at the end
	# of dealing with the previous button prevents that. 
	while not Done:
		if MSel == MENU_UNIT:
		# The UNIT submenu 
		# 
		# changing of units is only supported for
		#    Temperature    SEN_TEMP
		#    Baro Pressure  SEN_WEATH
		#    Gas            SEN_GAS  (to allow fining R0)
		#    Sound          SEN_SPL  (to allow finding the noise floor)
		#
				   #1234567890123456
			Write('UNIT: touch sens ',[0, 0],font20,WHITE)
			Write('use SHIFT to set ',[0,20],font20,WHITE)
			if SSel == SEN_TEMP:
				Write(SEN_TO_NAME[SSel]+':'+Dconf[DCONF_TEMP][DCONF_UNIT],[0,52],font26,WHITE)
				if touch[BUT_SHIFT]: 
					Dconf[DCONF_TEMP][DCONF_UNIT] = TEMP_Pick.Next
					Write(SEN_TO_NAME[SSel]+':'+Dconf[DCONF_TEMP][DCONF_UNIT],[0,52],font26,WHITE)
					Done = True
			elif SSel == SEN_WEATH:
				Write(SEN_TO_NAME[SSel]+':'+Dconf[DCONF_PRESS][DCONF_UNIT],[0,52],font26,WHITE)
				if touch[BUT_SHIFT]: 
					Dconf[DCONF_PRESS][DCONF_UNIT] = PRESS_Pick.Next
					Write(SEN_TO_NAME[SSel]+':'+Dconf[DCONF_PRESS][DCONF_UNIT],[0,52],font26,WHITE)
					Done = True
			elif SSel == SEN_GAS:
				Write(SEN_TO_NAME[SSel]+':'+Dconf[DCONF_GAS_OX][DCONF_UNIT][0],[0,52],font26,WHITE)
				if touch[BUT_SHIFT]: 
					if Dconf[DCONF_GAS_OX][DCONF_UNIT] == '/OX':
						Dconf[DCONF_GAS_OX][DCONF_UNIT]  = 'ΩOX'
						Dconf[DCONF_GAS_RED][DCONF_UNIT] = 'ΩRED'
						Dconf[DCONF_GAS_NH3][DCONF_UNIT] = 'ΩNH3'
						Sens_GAS_OX.Configure(R0=None)
						Sens_GAS_RED.Configure(R0=None)
						Sens_GAS_NH3.Configure(R0=None)
					else:
						Dconf[DCONF_GAS_OX][DCONF_UNIT]  = '/OX'
						Dconf[DCONF_GAS_RED][DCONF_UNIT] = '/RED'
						Dconf[DCONF_GAS_NH3][DCONF_UNIT] = '/NH3'
						Sens_GAS_OX.Configure(R0=CalGAS_R0[0])
						Sens_GAS_RED.Configure(R0=CalGAS_R0[1])
						Sens_GAS_NH3.Configure(R0=CalGAS_R0[2])
					Write(SEN_TO_NAME[SSel]+':'+Dconf[DCONF_GAS_OX][DCONF_UNIT][0],[0,52],font26,WHITE)
					Done = True
			elif SSel == SEN_SPL: 
				Write(SEN_TO_NAME[SSel]+':'+Dconf[DCONF_SPL][DCONF_UNIT],[0,52],font26,WHITE)
				if touch[BUT_SHIFT]:
					Dconf[DCONF_SPL][DCONF_UNIT] = SPL_Pick.Next
					if Dconf[DCONF_SPL][DCONF_UNIT] == 'dbSPL':
						Sens_SPL.Configure(noise =CalSPL_NOISE)
					else:
						Sens_SPL.Configure(noise =0)
					Write(SEN_TO_NAME[SSel]+':'+Dconf[DCONF_SPL][DCONF_UNIT],[0,52],font26,WHITE)
					Done = True
			elif SSel == SEN_TIME or SSel == SEN_PMS_PM or SSel == SEN_PMS_S or SSel == SEN_LUX:
				Write('no opt',[0,52],font26,WHITE)
		elif MSel == MENU_AVE:
		# 
		# The AVERAGE submenu 
		# 
		# handled by ConfBitChange 
		#
			Done = ConfBitChange('AVER.:sel sensor','use SHIFT to set',SSel,DCONF_OPT_AVE,GREEN)
		elif MSel == MENU_TREND:
		# 
		# The TREND submenu 
		# 
		# handled by ConfBitChange 
		#
			Done = ConfBitChange('TREND:sel sensor','use SHIFT to set',SSel,DCONF_OPT_TREND,BLUE)
		elif MSel == MENU_HIS:
		# 
		# The TREND History submenu 
		# 
		#
				  #1234567890123456
			Write('T-HIS:touch sens',[0, 0],font20,WHITE)
			Write('use SHIFT to set',[0,20],font20,WHITE)
			cx = SEN_TO_CONF[SSel]
			sname = SEN_TO_NAME[SSel]
			Write(SEN_TO_NAME[SSel]+':'+Dconf[cx[0]][DCONF_HIS],[0,52],font26,WHITE)
			if touch[BUT_SHIFT]: 
				Dconf[cx[0]][DCONF_HIS] = HIS_Pick.Next
				Write(SEN_TO_NAME[SSel]+':'+Dconf[cx[0]][DCONF_HIS],[0,52],font26,WHITE)
				# copy new config setting to all related items
				for c in cx[1:]:
					if c >= 0:
						Dconf[c][DCONF_HIS] = Dconf[cx[0]][DCONF_HIS]
				
				Done = True
		elif MSel == MENU_RECVAL:
		# 
		# The REC VAL submenu  (selecting which values (realtime) should be recorded / logged) 
		# 
		# handled by ConfBitChange 
		#
			Done = ConfBitChange('REC Val:sel sens','use SHIFT to set',SSel,DCONF_OPT_RECVAL)
		elif MSel == MENU_RECAVE:
		# 
		# The REC AVE submenu  (selecting which average values should be recorded / logged) 
		# 
		# handled by ConfBitChange 
		#
			Done = ConfBitChange('REC Ave:sel sens','use SHIFT to set',SSel,DCONF_OPT_RECAVE,GREEN)
		elif MSel == MENU_RECTIM:
		# 
		# The REC TIME submenu  (selecting how often recording should take place)
		# 
		#
				  #1234567890123456
			Write('REC Time: touch',[0, 0],font20,WHITE)
			Write('SHIFT to change',[0,20],font20,WHITE)
			Write(DelayTime_to_Str(RECTIME_CHOICES[RecTimeIx]),[0,40],font40,WHITE)
			if touch[BUT_SHIFT]:
				RecTimeIx = (RecTimeIx + 1) % len(RECTIME_CHOICES)
				Write(DelayTime_to_Str(RECTIME_CHOICES[RecTimeIx]),[0,40],font40,WHITE)
				Done = True
		elif MSel == MENU_SLEEPT:
		# 
		# The SLEEP TIME submenu  (selecting if and when the display should be blanked)
		# 
		#
				  #1234567890123456
			Write('SleepTime: touch',[0, 0],font20,WHITE)
			Write('SHIFT to change ',[0,20],font20,WHITE)
			Write(DelayTime_to_Str(SLEEPTIME_CHOICES[SleepTimeIx]),[0,40],font40,WHITE)
			if touch[BUT_SHIFT]:
				SleepTimeIx = (SleepTimeIx + 1) % len(SLEEPTIME_CHOICES)
				Write(DelayTime_to_Str(SLEEPTIME_CHOICES[SleepTimeIx]),[0,40],font40,WHITE)
				Done = True
		elif MSel == MENU_SAVE:
		# 
		# The SAVE submenu  (saving the current configuration in a file)
		# 
		#
				  #1234567890123456
			Write('touch SHIFT to  ',[0, 0],font20,WHITE)
			Write('save setup      ',[0,20],font20,WHITE)
			if touch[BUT_SHIFT]:
				SaveSetup()
				Write('saved',[0,40],font40,WHITE)
				Done =True
		elif MSel == MENU_LOAD:
		# 
		# The Load submenu  (loading the current configuration from a file)
		# 	
		#
				  #1234567890123456
			Write('touch SHIFT to  ',[0, 0],font20,WHITE)
			Write('reload setup    ',[0,20],font20,WHITE)
			if touch[BUT_SHIFT]:
				res = LoadSetup()
				if res:
					Write('load ok',[0,40],font40,WHITE)
				else:
					Write('failed',[0,40],font40,RED)
				Done =True

		else:
			raise ValueError

		if touch[BUT_MENU]:		
			#
			# leaving the Menu
			#
			MSel = MENU_NONE
			ImageDraw.Draw(img).rectangle([0,0,159,79],BLACK,None,0)
			Done = True
		elif touch[BUT_CYC_NXT]:
			#
			# moving to the next submenu, wrap around in needed 
			#
			MSel = MSel + 1 
			if MSel > MENU_LAST: MSel = MENU_NONE+1
			touch[BUT_CYC_NXT] = False
			ImageDraw.Draw(img).rectangle([0,0,159,79],BLACK,None,0)
		elif touch[BUT_REC_PRV]:
			#
			# moving to the previous submenu, wrap around in needed 
			#
			MSel = MSel - 1 
			if MSel <= MENU_NONE: MSel = MENU_LAST
			touch[BUT_REC_PRV] = False
			ImageDraw.Draw(img).rectangle([0,0,159,79],BLACK,None,0)
		else:
			Done = True
			
	return MSel

def WriteLogHead():
	"""
		Writes the header of the logfile (CSV), depending on what data
		items were enabled for logging
	"""
	f.write('Seconds')
	for i,dc in enumerate(Dconf):
		if i != DCONF_TIME:
			if (dc[DCONF_OPT] & DCONF_OPT_RECVAL) == DCONF_OPT_RECVAL:
				f.write(','+dc[DCONF_NAME]+' V')
			if (dc[DCONF_OPT] & DCONF_OPT_RECAVE) == DCONF_OPT_RECAVE:
				f.write(','+dc[DCONF_NAME]+' A')
	f.write('\n')

def WriteLogEntry(ts):
	"""
		Writes the selected data items as a log line (CSV)
	"""
	f.write('{:4.0f}'.format(ts))
	for i,dc in enumerate(Dconf):
		if i != DCONF_TIME:
			sd = CONF_TO_SENS[i]
			if (dc[DCONF_OPT] & DCONF_OPT_RECVAL) == DCONF_OPT_RECVAL:
				f.write(',{:3.3f}'.format(sd.Val()))
			if (dc[DCONF_OPT] & DCONF_OPT_RECAVE) == DCONF_OPT_RECAVE:
				f.write(',{:3.3f}'.format(sd.Stats.Vave()))
	f.write('\n')



def DoCommand(cmd):
	"""
		execute a shell command 
	"""
	try:
		retcode = subprocess.call(cmd, shell=True)
		if retcode < 0:
			print('child was terminated by signal ',retcode,file=sys.stderr)
		elif retcode > 0:
			print('child returned ',retcode,file=sys.stderr)
	except OSError as e:
		print('execution failed:',e,file=sys.stderr)
	return retcode




if __name__ == "__main__":
	
	isLogging = False

	draw = ImageDraw.Draw(img)

	LoadSetup()

	loopcount = 0
	SensSel = SEN_TEMP
	isTouched = [False] * 13
	ShowCount = SLEEPTIME_CHOICES[SleepTimeIx]
	PopUpMsg  = False
	CycleOn = False
	Snooze = 0
	try:
		start = perf_counter()

		while True: 
			now = perf_counter() - start
			if loopcount % 2 == 0:
				Sens_TEMP.Poll(now)
				Sens_BME.Poll(now)
				Sens_GAS.Poll(now)
				Sens_OPT.Poll(now)
				Sens_SPL.Poll(now)
				Sens_PMS.Poll(now)
				if isLogging:
					if loopcount % (2*RECTIME_CHOICES[RecTimeIx]) == 0:
						WriteLogEntry(now)
					
				
				if MenuSel == MENU_NONE:
					if PopUpMsg:
						ImageDraw.Draw(img).rectangle([0,0,159,79],BLACK,None,0)
						PopUpMsg = False;
						
					ShowSensor(SensSel)
					if ShowCount > 0: 
						ShowCount = ShowCount - 1
					else:
						if SleepTimeIx > 0:
							Snooze = (Snooze  +1) % 8
							#disp.set_backlight(1)
							ImageDraw.Draw(img).rectangle([0,0,159,79],BLACK,None,0)
							Write('*',[20*Snooze,30],font40,GREY)
							#sleep(0.05)
							#disp.set_backlight(0)
					if CycleOn:
						if loopcount % (2*CycleTime) == 0:
							ImageDraw.Draw(img).rectangle([0,0,159,79],BLACK,None,0)
							SensSel = (SensSel + 1) % 8
			 
			# to use the Adafruit MPR121, enable the lines below
			
			# tp = mpr121.touched_pins
			# if any(tp):
				# GPIO.output(BEEPER,GPIO.HIGH)
				# sleep(0.05)
			# for i,p in enumerate(tp):isTouched[i] = p
			# GPIO.output(BEEPER,GPIO.LOW)
			
			# and comment out these lines until the ---- 
			ts = mpr121.Touched()
			if ts != 0: GPIO.output(BEEPER,GPIO.HIGH)
			for el in range(13): 
				isTouched[el] = ((ts & (2**el)) != 0)
			if ts != 0:	sleep(0.05)
			GPIO.output(BEEPER,GPIO.LOW)
			
			# -------------
			
			
			# wake if optical proximity is sensed ..
			if SleepTimeIx > 0 and Sens_OPT_PRX.Val() >= 300:
				#if ShowCount == 0:
					#disp.set_backlight(1)
				ShowCount = SLEEPTIME_CHOICES[SleepTimeIx]
				Snooze = 0

			if any(isTouched):
				# wake if any touch is registered ..
				#if SleepTimeIx > 0 and ShowCount == 0:
					#disp.set_backlight(1)
				ShowCount = SLEEPTIME_CHOICES[SleepTimeIx]
				Snooze = 0
				ImageDraw.Draw(img).rectangle([0,0,159,79],BLACK,None,0)
				
				if isTouched[BUT_TEMP]:
					SensSel = SEN_TEMP
					if isTouched[BUT_SHIFT]: Show_Opt_Pick[SensSel].Next
				elif isTouched[BUT_WEATH]: 
					SensSel = SEN_WEATH
					if isTouched[BUT_SHIFT]: Show_Opt_Pick[SensSel].Next
				elif isTouched[BUT_GAS]: 
					SensSel = SEN_GAS
					if isTouched[BUT_SHIFT]: Show_Opt_Pick[SensSel].Next
				elif isTouched[BUT_PMS_PM]: 
					SensSel = SEN_PMS_PM
					if isTouched[BUT_SHIFT]: Show_Opt_Pick[SensSel].Next
				elif isTouched[BUT_TIME]: 
					SensSel = SEN_TIME
					if isTouched[BUT_SHIFT]:
						PopUpMsg = True
						for c in CONF_TO_SENS:
							if CONF_TO_SENS[c] != None:
								CONF_TO_SENS[c].Stats.ResetMinMax()
						Write('reset minmax ..',[0,40],font20,WHITE)
				elif isTouched[BUT_LUX]: 
					if isTouched[BUT_SHIFT]: Show_Opt_Pick[SensSel].Next
					SensSel = SEN_LUX
				elif isTouched[BUT_SPL]: 
					SensSel = SEN_SPL
					if isTouched[BUT_SHIFT]: Show_Opt_Pick[SensSel].Next
				elif isTouched[BUT_PMS_S]: 
					SensSel = SEN_PMS_S
					if isTouched[BUT_SHIFT]: Show_Opt_Pick[SensSel].Next
				if MenuSel != MENU_NONE:
					MenuSel = Menu(MenuSel,SensSel,isTouched)
				else:
					if isTouched[BUT_MENU]:
						isTouched[BUT_MENU] = False
						MenuSel = Menu(MENU_UNIT,SensSel,isTouched)
						
					elif isTouched[BUT_CYC_NXT]:
						CycleOn = not CycleOn
					elif isTouched[BUT_REC_PRV]:
						PopUpMsg = True
						if isLogging:
							f.close()
							isLogging = False
							Write('recording stopped',[0,0],font20,WHITE)
							result = DoCommand('sudo umount /dev/sda1')
							if result != 0:
								Write('umount failed',[0,20],font20,RED)
						else:
							result = 0
							if not os.path.ismount('/mnt/usb_stick'):
								result = DoCommand('sudo mount -o uid=pi,gid=pi /dev/sda1 /mnt/usb_stick')
							if result != 0:
								Write("can't mount USB",[0,20],font20,RED)
							else:		
								out_name = '/mnt/usb_stick/LOG_'+strftime('%Y%m%d%H%M%S',localtime())+'.csv'
								f = open(out_name,'w')
								WriteLogHead()
								isLogging = True
								Write('now recording ..',[0,40],font20,WHITE)
				
			disp.display(img)
			loopcount = loopcount + 1
			snooze = 0.5 - (perf_counter() - (start + now))
			if snooze < 0:
				#print('!snooze {:3.2f}'.format(snooze))
				snooze = 0
			sleep(snooze)
			

	except KeyboardInterrupt:
		if isLogging: f.close()
		disp.set_backlight(0)
		GPIO.output(BEEPER,GPIO.LOW)
