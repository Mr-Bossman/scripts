#!/usr/bin/env python
import os 
import subprocess
import time
import psutil
import multiprocessing
import math
deviation = 0.5
always_free_cores  = 1.5


cores = multiprocessing.cpu_count()
mining_cores = 0
proc = None
while True:
	free_cores = (100-psutil.cpu_percent())/(100/cores)
	if  always_free_cores+deviation < free_cores:
		tmp = mining_cores + math.floor(free_cores-math.ceil(always_free_cores))
		if tmp < (cores-always_free_cores ) and mining_cores != tmp:
			mining_cores = tmp
			if proc != None:
				proc.kill()
			proc = subprocess.Popen(['/home/jesse/Documents/verus/ccminer/ccminer', '-a', 'verus', '-o','stratum+tcp://na.luckpool.net:3956', '-u', 'RXhFKA9cTJXRbK8nuuZ3aCVDyQvC96dRLD.ja_02', '-p', 'x', '-t' ,  str(mining_cores)])
	elif always_free_cores-deviation >  free_cores:
		tmp = mining_cores - math.ceil(always_free_cores)
		if tmp > 0 and mining_cores != tmp:
			mining_cores = tmp
			if proc != None:
				proc.kill()
			proc = subprocess.Popen(['/home/jesse/Documents/verus/ccminer/ccminer', '-a', 'verus', '-o','stratum+tcp://na.luckpool.net:3956', '-u', 'RXhFKA9cTJXRbK8nuuZ3aCVDyQvC96dRLD.ja_02', '-p', 'x', '-t' ,  str(mining_cores)])
		else:
			mining_cores = 0
			if proc != None:
				proc.kill()
	print("There are "+ str(round(free_cores,2)) + " free cores. Mining on " + str(mining_cores)+ " of " + str(cores) + " cores.")

	time.sleep(1)
