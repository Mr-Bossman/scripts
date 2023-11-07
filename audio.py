#!/bin/python
import math
import sys
import time
samplerate=8000
soundarr=[1]*samplerate
freq=2000
notes=[440,466.164,493.883,523.251,554.365,587.329,622.254,659.255,698.456,739.989,783.991,830.609]
def printscaled(value):
	sys.stdout.buffer.write(int((value+1)*127.5).to_bytes(1,'big'))
def playsin(freq,duration,volume=1):
	for i in range(int(duration*samplerate)):
		t=freq*(i/samplerate)
		printscaled(math.sin(2*math.pi*t)*volume)
def playstop(duration):
	for i in range(int(duration*samplerate)):
		printscaled(0)

song=[8,6,4,6,8,8,8,6,6,6,8,8,8,8,6,4,6,8,8,8,8,6,6,8,6,4]
while True:
	for i in song:
		playsin(notes[i]*1.2,0.6,0.5)
		playstop(0.1)
	playstop(0.4)

