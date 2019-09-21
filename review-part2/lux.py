#!/usr/bin/env python
from ltr559 import LTR559
import ST7735
from PIL import Image, ImageDraw, ImageFont
from time import sleep


ltr559 = LTR559()

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


def Display_Range(Prompt,Min,Now,Max,Xpos,Colour):
	txtsize_x, txtsize_y = draw.textsize(Prompt, font)
	Ypos = 0
	draw.text((Xpos, Ypos), Prompt, font=font, fill=Colour) 
	Ypos = Ypos + txtsize_y+5
	draw.text((Xpos, Ypos), '{:8.1f}'.format(Max), font=font, fill=(255,0,0)) 
	Ypos = Ypos + txtsize_y+5
	draw.text((Xpos, Ypos), '{:8.1f}'.format(Now), font=font, fill=(0,255,0)) 
	Ypos = Ypos + txtsize_y+5
	draw.text((Xpos, Ypos), '{:8.1f}'.format(Min), font=font, fill=(255,255,0)) 
	


Record = False
MSec = 0
MaxLux = 0.0
MinLux = 1e12
MaxProx = 0.0
MinProx = 1e12

LUXRANGE = [(96, 0.01, 600.0),
			(48, 0.02,1300.0),
			(8, 0.125,8000.0),
			(4, 0.25,16000.0),
			(2, 0.5,32000.0),
			(1, 1.0,64000.0)]
		  
		  
def AutoLux():
	gain = ltr559.get_gain()
	Lux = ltr559.get_lux() 
	bestgain = 1
	for r in LUXRANGE:
		if Lux < r[2]: 
			bestgain = r[0]
			break
	if bestgain != gain:
		ltr559.set_light_options(True,bestgain)
		sleep(0.5)
		Lux = ltr559.get_lux()
	print('gain:'+str(ltr559.get_gain())+' lux='+str(Lux))
	return Lux

Done = False

ltr559.set_light_integration_time_ms(100)

if Record:
	fo = open('Lux-Test.csv','w')
	fo.write('t,MinLux,Lux,MaxLux,MinProx,Prox,MaxProx\n')
	
while not Done:
	try:
		Lux = AutoLux()
		
		if Lux > MaxLux: MaxLux = Lux
		if Lux < MinLux: MinLux = Lux
		Prox = ltr559.get_proximity()
		if Prox > MaxProx: MaxProx = Prox
		if Prox < MinProx: MinProx = Prox
		
		
			
		draw.rectangle((0, 0, 160, 80), back_colour)
		Display_Range(' Lux ',MinLux,Lux,MaxLux,0,(255,255,255))
		Display_Range(' Prox ',MinProx,Prox,MaxProx,80,(255,255,255))
		disp.display(img)
				
		if Record:
			fo.write('{:5d}'.format(MSec))
			fo.write(',{:+10.0f}'.format(MinLux))
			fo.write(',{:+10.0f}'.format(Lux))
			fo.write(',{:+10.0f}'.format(MaxLux))
			fo.write(',{:+10.0f}'.format(MinProx))
			fo.write(',{:+10.0f}'.format(Prox))
			fo.write(',{:+10.0f}'.format(MaxProx))
		sleep(1.0)
		MSec = MSec + 1000

		if Prox > 200:
			MaxLux = 0.0
			MaxProx = 0.0

	except KeyboardInterrupt:
		print()
		if Record: fo.close()
		disp.set_backlight(0)
		quit()
 



