#!/bin/python3
import numpy as np
import numpy.typing as npt
import cv2 as cv


invert = True
# chest_lut[nible_ind][line_num] = chest_num
chest_lut = [[0,1],[2,3]]
shulkers: int = 5
max_frames: int = -1
# -1 for all frames
# 0 1
# 2 3
top_left = np.array([-118, 197, -310], np.int32)
vert = np.array([0, -8, 0], np.int32)
horz = np.array([0, 0, -6], np.int32)

chest_cords = ["-122 192 -219", "-122 192 -225",
	       "-122 184 -219", "-122 184 -225"]

chest_cords_int: list[list[int]] = [list(top_left       ), list(top_left + horz),
				    list(top_left + vert), list(top_left + horz +vert)]
chest_cords = [f"{x[0]} {x[1]} {x[2]}" for x in chest_cords_int]


cap = cv.VideoCapture("./test.gif")
if not cap.isOpened():
	print("Cannot open camera")
	exit()

def grey_bin(bin: str):
	mask = val = int(bin, 2)
	while mask > 0:
		mask >>= 1
		val ^= mask
	return val

def list_to_discs(frame: list[list[bool]]):
	ret: list[list[int]] = []
	for i in range(len(frame)):
		line_bin = [ 1 if frame[i][j] else 0 for j in range(len(frame[i]))]
		line_4b = [ line_bin[j:j+4] for j in range(0,len(line_bin),4)]
		line_4b_str = [ ''.join(map(str, line_4b[j])) for j in range(len(line_4b))]
		line_grey = [ grey_bin(line_4b_str[j][::-1]) for j in range(len(line_4b_str))]
		ret.append(line_grey)
	return ret

def discs_to_chests(lines: list[list[int]], chest_lut: list[list[int]]):
	blank_color = grey_bin("1111" if invert else "0000")
	n_chests: int = max([x for i in chest_lut for x in i]) + 1
	cnt = len(chest_lut[0])
	chests: list[list[int]] = [[blank_color]*(3*9*shulkers) for _ in range(n_chests)]
	for i in range(len(lines)):
		for nib in range(len(lines[i])):
			chest_num = chest_lut[nib][i%cnt]
			chests[chest_num][i//cnt] = lines[i][nib]
	return chests

def split_chests(chest: list[int]):
	return [chest[i:i + (3*9)] for i in range(0, len(chest), (3*9))]

def chest_to_nbt(chest: list[int]):
	disc_lut = ["netherite_hoe",        "music_disc_13",
		    "music_disc_cat",       "music_disc_blocks",
		    "music_disc_chirp",     "music_disc_far",
		    "music_disc_mall",      "music_disc_mellohi",
		    "music_disc_stal",      "music_disc_strad",
		    "music_disc_ward",      "music_disc_11",
		    "music_disc_wait",      "music_disc_pigstep",
		    "music_disc_otherside", "music_disc_5"]
	data = "["
	for slot in range(len(chest)):
		name = disc_lut[chest[slot]]
		data += f"{{slot: {slot}, count: 1, item: {{id: {name}}}}}"
		data += "," if slot < (len(chest)-1) else "]"
	return data

def shulker_to_command(chests: list[str], cords: str):
	data = "["
	for i in range(len(chests)):
		data += f"{{Slot: {i}, count: 1, id: shulker_box, components: {{container: {chests[i]}}}}}"
		data += "," if i < (len(chests)-1) else "]"
	return f"/data modify block {cords} Items set value {data}"

def spawn_commands(commands: list[str]):
	text = "summon falling_block ~ ~1 ~ {Time: 1, BlockState: {Name: redstone_block}, Passengers: [{id: falling_block, Time: 1, BlockState: {Name: activator_rail}, Passengers: ["
	for command in commands:
		text += f"{{id: \"command_block_minecart\", Command: \"{command}\"}},"
	text += "{id: command_block_minecart, Command: 'setblock ~ ~1 ~ command_block{auto: 1,Command: \"minecraft:fill ~ ~ ~ ~ ~-2 ~ air\"}'},"
	text += "{id: command_block_minecart, Command: 'minecraft:kill @e[type=command_block_minecart,distance=..1]'}]}]}"
	return text

def print_list(frame: list[list[bool]]):
	for i in range(len(frame)):
		line_bin = [ "■" if frame[7-i][j] else "□" for j in range(len(frame[i]))]
		print("[", *line_bin, "]")
	print()

frame_count = 0
last_buf = []
lines: list[list[int]] = []
while True:
	ret, frame = cap.read()
	if not ret:
#		print("Can't receive frame (stream end?). Exiting ...")
		break
	gray = cv.cvtColor(cv.resize(frame, (8,8), cv.INTER_LANCZOS4), cv.COLOR_BGR2GRAY)
	grey_flip = cv.flip(gray, 0) # flip vertically
	(_, bin) = cv.threshold(grey_flip, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

	if invert:
		bin = cv.bitwise_not(bin)

	if len(last_buf) == 0:
		disped = bin
	else:
		disped = cv.bitwise_xor(bin,last_buf)
	last_buf = bin

	#print_list(disped)
	lines += list_to_discs(cv.bitwise_not(disped))
	frame_count += 1
	if frame_count == max_frames:
		break
cap.release()
# TODO: add check for number of shulkers required for frame_count

#list of the 4 chests per frame with infinite size
chests: list[list[int]] = discs_to_chests(lines, chest_lut)

#list of the 4 chests per frame with size 3*9 but slpit apart
chests_split: list[list[list[int]]] = [split_chests(chest) for chest in chests]

commands: list[str] = []
for i in range(len(chests_split)):
	shulkers_in_chest = [chest_to_nbt(shulker) for shulker in chests_split[i]]
	commands.append(shulker_to_command(shulkers_in_chest, chest_cords[i]))
print(spawn_commands(commands))

