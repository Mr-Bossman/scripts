#!/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import sys
import time
import serial
from serial import Serial
from tkcolorpicker import askcolor
if len(sys.argv) == 2:
  port = sys.argv[1]
  id = "ff"
  baud = 9600
elif len(sys.argv) != 4:
    port = "/dev/ttyUSB0"
    id = "ff"
    baud = 9600
else:
    port = sys.argv[1]
    baud = sys.argv[2]
    id = sys.argv[3]
ser = serial.Serial(str(port), int(baud) )

ser.write(bytes([   bytes.fromhex( str(id) )[0]]))
time.sleep(.1)
ser.write(bytes([0]))
time.sleep(.1)
ser.write(bytes([0]))
time.sleep(.1)
ser.write(bytes([0]))
ser.close()
