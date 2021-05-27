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
    exit()

root = tk.Tk()
style = ttk.Style(root)
style.theme_use('clam')

color = askcolor((255, 255, 0), root)
#ser = serial.Serial('/dev/ttyUSB0',9600)
print(color[0])
ser = serial.Serial(str(sys.argv[1]), int(sys.argv[2]) )

ser.write(bytes([   bytes.fromhex( str(sys.argv[3]) )[0]  ]))
time.sleep(.1)
ser.write(bytes([color[0][1]]))
time.sleep(.1)
ser.write(bytes([color[0][0]]))
time.sleep(.1)
ser.write(bytes([color[0][2]]))
ser.close()
