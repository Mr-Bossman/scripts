import math


r = 10
units = 5
centerX = 190
centerY = -85
for i in range(units):
	y = (r*math.cos(((2*math.pi)/units)*math.floor(i))) + centerY
	x = (r*math.sin(((2*math.pi)/units)*math.floor(i))) + centerX
	print(str(x) +" , " + str(y) + " , " + str((units-i)* (360/units)))

