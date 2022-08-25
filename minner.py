#!/usr/bin/env python
import os
import subprocess
import time
import psutil
import multiprocessing
import math
deviation = 1.5
always_free_cores  = 2.3

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
	proc = subprocess.Popen(['/bin/ccminer', '-a', 'verus', '-o','stratum+tcp://na.luckpool.net:3956', '-u', 'RXhFKA9cTJXRbK8nuuZ3aCVDyQvC96dRLD.ja_02', '-p', 'x', '-t' ,  str(mining)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
while True:
	free_cores = (100-psutil.cpu_percent())*cores/100
	if always_free_cores-deviation >  free_cores:
		killM()
		print("Recalculating cores", flush=True)
		time.sleep(10)
		mining_cores = 0
	elif  always_free_cores+deviation < free_cores:
		tmp = mining_cores + math.floor(free_cores-always_free_cores)
		if tmp < (cores-always_free_cores) and mining_cores != tmp:
			if mining_cores == 0:
				free_cores -= tmp
			mining_cores = tmp
			minewith(mining_cores)
			print("There are "+ str(round(free_cores,2)) + " free cores. Mining on " + str(mining_cores)+ " of " + str(cores) + " cores.", flush=True)
	time.sleep(1)
