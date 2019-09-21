#!/usr/bin/env python

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
font_size = 20
font = ImageFont.truetype("ttf/Hack-Regular.ttf", font_size)
text_colour = (255, 255, 255)
back_colour = (0, 170, 0)

Done = False


# Width and height to calculate text position.
WIDTH = disp.width
HEIGHT = disp.height


# New canvas to draw on.
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

Pic = Image.open("EnviroPlus.png")
Scale = 1.0
Wscale = Pic.width / WIDTH
Hscale = Pic.height / HEIGHT
if Wscale > Hscale: 
	Scale = Wscale
else:
	Scale = Hscale
Pwidth = int(Pic.width/Scale)
Pheight= int(Pic.height/Scale)
SPic = Pic.resize((Pwidth,Pheight))

Px = int((WIDTH -Pwidth)/2)
Py = int((HEIGHT -Pheight)/2)
while not Done:
	try:
		draw.rectangle((0, 0, 160, 80), back_colour)
		img.paste(SPic,(Px,Py))
		disp.display(img)
		sleep(5.0)


		
		message = "  Hi there! Reviewing the Enviro+ ..."
		size_x, size_y = draw.textsize(message, font)
		# Calculate Y text position to center it 
		y = (HEIGHT / 2) - (size_y / 2)
		for c in message:
			# Draw background rectangle and write text.
			draw.rectangle((0, 0, 160, 80), back_colour)
			draw.text((0, y), message, font=font, fill=text_colour)
			disp.display(img)
			message  = message[1::]+message[0]
			sleep(0.1)
	except KeyboardInterrupt:
		disp.set_backlight(0)
		quit()
