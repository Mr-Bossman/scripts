import sys
import time
import serial
from serial import Serial
#ser = serial.Serial('/dev/ttyUSB2',9600)

if len(sys.argv) != 5:
    exit()

ser = serial.Serial(str(sys.argv[1]), int(sys.argv[2]) )

ser.write(bytes([   bytes.fromhex( str(sys.argv[3]) )[0]  ]))
time.sleep(.1)
ser.write(bytes([ bytes.fromhex(str(sys.argv[4]))[1] ]))
time.sleep(.1)
ser.write(bytes([ bytes.fromhex(str(sys.argv[4]))[0] ]))
time.sleep(.1)
ser.write(bytes([ bytes.fromhex(str(sys.argv[4]))[2] ]))
ser.close()
