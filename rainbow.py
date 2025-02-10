#!/bin/python3
import time
import colorsys
import socket
from random import seed
from random import random

seed(367546)
seed(random())

server_address = ('localhost', 1234)
def rgb(colour):
    color = [c*255 for c in colour]
    try:
        message = bytearray([int(color[0])]).hex() + " "
        message += bytearray([int(color[1])]).hex() + " "
        message += bytearray([int(color[2])]).hex()
        sock.send(message.encode())
    finally:
        sock.close()
while True:
    for i in range(0,100):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        rgb(colorsys.hsv_to_rgb(float(i)/100.0, 1, 1))
        time.sleep(random()/5+0.01)
