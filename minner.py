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
def killM():
	global proc
	if proc != None:
		proc.kill()
def minewith(mining):
	global proc
	if proc != None:
		proc.kill()
	proc = subprocess.Popen(['/bin/ccminer', '-a', 'verus', '-o','stratum+tcp://na.luckpool.net:3956', '-u', 'RXhFKA9cTJXRbK8nuuZ3aCVDyQvC96dRLD.ja_02', '-p', 'x', '-t' ,  str(mining)])
while True:
	free_cores = (100-psutil.cpu_percent())/(100/cores)
	if  always_free_cores+deviation < free_cores:
		tmp = mining_cores + math.floor(free_cores-math.ceil(always_free_cores))
		if tmp < (cores-always_free_cores ) and mining_cores != tmp:
			mining_cores = tmp
			minewith(mining_cores)
			print("There are "+ str(round(free_cores,2)) + " free cores. Mining on " + str(mining_cores)+ " of " + str(cores) + " cores.")
	elif always_free_cores-deviation >  free_cores:
		killM()
		time.sleep(10)
		print("Recalculating cores")
	time.sleep(1)
