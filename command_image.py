#!/bin/python3
import numpy as np
import cv2 as cv


invert = True
# chest_lut[nible_ind][chest_num] = line_num
chest_lut = [[2,0,1,3],[2,0,1,3]]
chest_cords = ["-53 111 108", "-54 111 108",
	       "-59 111 108", "-60 111 108",
	       "-79 111 108", "-80 111 108",
	       "-85 111 108", "-86 111 108"]
cap = cv.VideoCapture("./test.gif")
if not cap.isOpened():
	print("Cannot open camera")
	exit()

def list_to_discs(frame):
	ret = []
	for i in range(len(frame)):
		line = [ 1 if frame[i][j] else 0 for j in range(len(frame[i]))]
		line = [ line[j:j+4] for j in range(0,len(line),4)]
		line = [ int(''.join(map(str, line[j])), 2) for j in range(len(line))]
		ret.append(line)
	return ret

def discs_to_chests(lines, chest_lut):
	chests = [[15]*(3*9) for _ in range(len(chest_lut[0])*len(chest_lut))]
	for i in range(len(lines)):
		for nib in range(len(lines[i])):
			cnt = len(chest_lut[nib])
			chest_num = chest_lut[nib].index(i%cnt) + (nib*cnt)
			chests[chest_num][i//cnt] = lines[i][nib]
	return chests

def chest_to_command(chest, cords):
	disc_lut = ["netherite_hoe", "13",
		    "cat",           "blocks",
		    "chirp",         "far",
		    "mall",          "mellohi",
		    "stal",          "strad",
		    "ward",          "11",
		    "wait",          "pigstep",
		    "otherside",     "5"]
	data = "["
	for slot in range(len(chest)):
		name = disc_lut[chest[slot]]
		data += "{Slot:" + str(slot) + "b,id:\\\"music_disc_" + name + "\\\",Count:1b}"
		data += "," if slot < (len(chest)-1) else "]"
	return "/data modify block " + cords + " Items set value " + data

last_buf = []
lines = []
while True:
	ret, frame = cap.read()
	if not ret:
#		print("Can't receive frame (stream end?). Exiting ...")
		break
	gray = cv.cvtColor(cv.resize(frame, (8,8), cv.INTER_LANCZOS4), cv.COLOR_BGR2GRAY)
	(_, bin) = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

	if invert:
		bin = cv.bitwise_not(bin)

	if len(last_buf) == 0:
		disped = bin
	else:
		disped = cv.bitwise_xor(bin,last_buf)
	last_buf = bin


	lines += list_to_discs(cv.bitwise_not(disped))

chests = discs_to_chests(lines,chest_lut)

text = "summon minecraft:falling_block ~ ~3 ~ {BlockState:{Name:\"minecraft:activator_rail\"},Time:1,Passengers:["
for i in range(len(chests)):
	prefix = "{id:\"minecraft:command_block_minecart\",Command:\""
	suffix = "\"},"
	text += prefix + chest_to_command(chests[i],chest_cords[i]) + suffix
text += "{id:\"minecraft:command_block_minecart\",Command:\"kill @e[type=command_block_minecart,distance=..5]\"}]}"
text += "{id:\"minecraft:command_block_minecart\",Command:\"minecraft:kill @e[type=command_block_minecart,distance=..5]\"}]}"
print(text)
cap.release()
