#!/bin/python3
import time
import sys
from serial import Serial
from colorsys import hsv_to_rgb
from random import seed
from random import random

seed(time.time())

def rgb(colour, id, ser):
	color = [int(c*255) for c in colour]
	set_color(color, id, ser)

def set_color(color, id, ser):
	ser.write(bytes([bytes.fromhex(str(id))[0]]))
	ser.write(bytes([color[1]]))
	ser.write(bytes([color[0]]))
	ser.write(bytes([color[2]]))
	time.sleep(.001)

if len(sys.argv) == 1:
    port = "/dev/ttyUSB0"
    baud = 9600
    id = "ff"
elif len(sys.argv) == 2:
    port = sys.argv[1]
    baud = 9600
    id = "ff"
else:
    port = sys.argv[1]
    baud = sys.argv[2]
    id = sys.argv[3]

ser = Serial(str(port), int(baud))

while True:
	for i in range(0,100):
		rgb(hsv_to_rgb(float(i)/100.0, 1, 1), id, ser)
		time.sleep(random()/80+0.001)
