#!/usr/bin/env python
import pyaudio
import numpy as np
import math
import ST7735
from PIL import Image, ImageDraw, ImageFont
from time import sleep

# Create LCD class instance.
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)
font_size = 12
font = ImageFont.truetype("ttf/Hack-Regular.ttf", font_size)
text_colour = (255, 255, 255)
back_colour = (0, 0, 0)

WIDTH = disp.width
HEIGHT = disp.height
# New canvas to draw on.
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

RATE  = 22000
CHUNK = 22000
CHANNEL=1
audio = pyaudio.PyAudio()

FSdbSPL = 120

def Display_SPL(Prompt,SPL,Ypos,Barcolour):
	txt = Prompt + '{:3.0f} :'.format(SPL)
	txtsize_x, txtsize_y = draw.textsize(txt, font)
	draw.text((0, Ypos), txt, font=font, fill=text_colour)
	bar_len = int(SPL * ((WIDTH - txtsize_x)/FSdbSPL))
	draw.rectangle((txtsize_x,Ypos,txtsize_x+bar_len,Ypos+txtsize_y),fill=Barcolour)


def PCM_to_dbSPL(pcm):
	res = 0.0
	if pcm > 0:
		dbFS = 20*math.log10(pcm/0x1ffff)
		res = FSdbSPL +dbFS	
	return res
	
print('++++++++ default host api info +++++++')
info = audio.get_default_host_api_info()

stream = audio.open(format=pyaudio.paInt32, 
					input_device_index = info['defaultInputDevice'],
					channels = CHANNEL,
					rate = RATE,
					input = True,
					frames_per_buffer=CHUNK)

Record = False
MSec = 0
Sum = 0.0
Cnt = 0
noisefloor = 1e12
maxSPL = 0.0
Done = False
if Record:
	fo = open('SPL-Test.csv','w')
	fo.write('t,vmin,vmax,DCOFFSET,vmin_nodc,vmax_nodc,vabs,noisefloor,vfinal,dbSPL,maxSPL\n')
	
while not Done:
	try:
		sdata = stream.read(CHUNK)
		if MSec >=3000:
			idata = np.frombuffer(bytes(sdata),'<i4')
			fdata = idata.astype(float)
			vmax = (np.amax(fdata)) / 0x4000
			vmin = (np.amin(fdata)) / 0x4000
			DCoffset = (np.sum(fdata)) / (0x4000 * fdata.size)
			vmax_nodc = vmax - DCoffset
			vmin_nodc = vmin - DCoffset
			if abs(vmax_nodc) > abs(vmin_nodc): 
				vabs = abs(vmax_nodc)
			else:
				vabs = abs(vmin_nodc)
			if vabs < noisefloor: noisefloor = vabs 
	
			vfinal = vabs - noisefloor

			dbSPL = PCM_to_dbSPL(vfinal)
			if dbSPL > maxSPL:
				maxSPL = dbSPL
				
			print(MSec)
			draw.rectangle((0, 0, 160, 80), back_colour)
			Display_SPL('now',dbSPL,0,(0,170,0))
			Display_SPL('max',maxSPL,20,(255,0,0))
			draw.text((0, 40),'nfloor {:3.1f}'.format(noisefloor), font=font, fill=(255,255,255))
			draw.text((0, 60),'dcoffs {:+6.0f}'.format(DCoffset), font=font, fill=(255,255,255))
			disp.display(img)
				
			if Record:
				fo.write('{:5d}'.format(MSec))
				fo.write(',{:+10.0f}'.format(vmin))
				fo.write(',{:+10.0f}'.format(vmax))
				fo.write(',{:+10.0f}'.format(DCoffset))
				fo.write(',{:+10.0f}'.format(vmin_nodc))
				fo.write(',{:+10.0f}'.format(vmax_nodc))
				fo.write(',{:+10.0f}'.format(vabs))
				fo.write(',{:+10.0f}'.format(noisefloor))
				fo.write(',{:+10.0f}'.format(vfinal))
				fo.write(',{:4.0f}'.format(dbSPL))
				fo.write(',{:4.0f}'.format(maxSPL))
				fo.write('\n')
		MSec = MSec + 1000

	except KeyboardInterrupt:
		print()
		if Record: fo.close()
		stream.stop_stream()
		stream.close()
		audio.terminate()
		disp.set_backlight(0)
		quit()
 



