import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import serial
from serial import Serial
#fig = plt.figure()
#ax = fig.add_subplot(projection='3d')
ser = serial.Serial('/dev/ttyUSB1',115200)
color = ['r','g','b','c','m','y','k']
g = 0
b = 0
while True:
	line = str(ser.readline(),'ascii')
	if(len(line.split(',')) != 3):
		continue
	tmp = [int(i) for i in line.split(',')]
	if(tmp[1] == 0 and tmp[2] == 0):
		b = 0
		g+=1
	b += 1
	plt.scatter(b,tmp[0],c=color[g%len(color)])
	plt.draw()
	plt.pause(0.01)
