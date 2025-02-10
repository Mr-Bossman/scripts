#!/bin/python3
import time
import sys
from serial import Serial
from random import seed
from random import random
from tkcolorpicker import askcolor
import tkinter as tk
import tkinter.ttk as ttk

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

root = tk.Tk()
style = ttk.Style(root)
style.theme_use('clam')

ser = Serial(str(port), int(baud))
color = askcolor((255, 255, 0), root)
set_color(color[0], id, ser)
