#!/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import sys
import time
import serial
from serial import Serial
from tkcolorpicker import askcolor
if len(sys.argv) != 4:
    print("erroe")
    port = "/dev/ttyUSB1"
    id = "ff"
    baud = 9600
else:
    port = sys.argv[1]
    baud = sys.argv[2]
    id = sys.argv[3]

root = tk.Tk()
style = ttk.Style(root)
style.theme_use('clam')

color = askcolor((255, 255, 0), root)
print(color[0])
ser = serial.Serial(str(port), int(baud) )

ser.write(bytes([   bytes.fromhex( str(id) )[0]  ]))
time.sleep(.1)
ser.write(bytes([color[0][1]]))
time.sleep(.1)
ser.write(bytes([color[0][0]]))
time.sleep(.1)
ser.write(bytes([color[0][2]]))
ser.close()
