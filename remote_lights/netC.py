#!/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import sys
import time
import asyncio
import websockets
import serial
from serial import Serial
import string
#from tkcolorpicker import askcolor
if len(sys.argv) != 6:
    print("erroe")
    exit()

#root = tk.Tk()
#style = ttk.Style(root)
#style.theme_use('clam')

#color = askcolor((255, 255, 0), root)
#ser = serial.Serial('/dev/ttyUSB0',9600)
#print(color[0])
ser = serial.Serial(str(sys.argv[1]), int(sys.argv[2]) )
import socket

HOST = sys.argv[4]  # Standard loopback interface address (localhost)
PORT = int(sys.argv[5])       # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data = data.decode("utf-8")
                hexstr = data.strip().split(' ')
                if(len(hexstr) != 3):
                    break
                if(len(hexstr[0]) > 2):
                    break
                if(len(hexstr[1]) > 2):
                    break
                if(len(hexstr[2]) > 2):
                    break
                for i in range(0,len(hexstr)):
                    if(len(hexstr[i]) == 1):
                        hexstr[i] = '0' + hexstr[i]
                print(hexstr)
                if(not all(c in string.hexdigits for c in hexstr[0])):
                    break
                if(not all(c in string.hexdigits  for c in hexstr[1])):
                    break
                if(not all(c in string.hexdigits  for c in hexstr[2])):
                    break
                ser.write(bytes([   bytes.fromhex( str(sys.argv[3]) )[0]  ]))
                time.sleep(.1)
                ser.write(bytes([bytes.fromhex(hexstr[1])[0]]))
                time.sleep(.1)
                ser.write(bytes([bytes.fromhex(hexstr[0])[0]]))
                time.sleep(.1)
                ser.write(bytes([bytes.fromhex(hexstr[2])[0]]))
                conn.close()
                break