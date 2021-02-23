import sys
import math 
import time
import serial
import json


from serial import Serial
ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)

#if len(sys.argv) != 3:
#    exit()

#ser = serial.Serial(str(sys.argv[1]), int(sys.argv[2]) )
def Send8(val):
    ser.write(bytes([(val).to_bytes(1, byteorder='little')[0]  ]))

def Send16(val):
    ser.write(bytes([(val).to_bytes(2, byteorder='little')[0]  ]))
    ser.write(bytes([(val).to_bytes(2, byteorder='little')[1]  ]))

def Send32(val):
    ser.write(bytes([(val).to_bytes(4, byteorder='little')[0]  ]))
    ser.write(bytes([(val).to_bytes(4, byteorder='little')[1]  ]))
    ser.write(bytes([(val).to_bytes(4, byteorder='little')[2]  ]))
    ser.write(bytes([(val).to_bytes(4, byteorder='little')[3]  ]))

def Read32():
    return int.from_bytes(ser.read(4), "little")
def Read16():
    return int.from_bytes(ser.read(2), "little")
def Read8():
    return int.from_bytes(ser.read(1), "little")


def sendOSC(freq,dudy):
    Send32(int(freq))
    Send8(int(dudy))
    i = Read8()
    div = 20000000/(2**i)
    pwm = Read16()
    top = Read16()
    #return [div/top,(pwm*100)/top]
    return [freq,dudy]

def sendOSC2(Tl,Th):
    freq = 1/(Tl+Th)
    dudy = (Th*100)/(Tl+Th)
    if(dudy >= 100):
        return 1
    if(dudy < 1):
        return 1

    print(Th)
    print(dudy)

    Send32(int(freq))
    Send8(int(dudy))
    i = Read8()
    div = 20000000/(2**i)
    pwm = Read16()
    top = Read16()
    #return [div/top,(pwm*100)/top]
    return 0

def GetV(ratio):
    Vin = 4
    Factor = 8
    return ((Read32()*Vin)/(1024*Factor))*ratio
def frange(start, end, jump):
    points = int((end-start)/jump)
    return [(x * jump) + start for x in range(points)]

#with open('output.txt','w') as filehandle:
# data = json.load(filehandle)
base = 10 # base for the exponent for log scale
startF = 100 # starting frequency 
endF = 500000 # ending frequency 
dataPoints = 100 # amount of data points to collect between frequency jumps
lists = []
for dudy in range(10,1000,10): # starting dudy cycle ending dudy cycle and increment amount   
    for exp in frange(math.log(startF,base),math.log(endF,base),(math.log(endF,base)-math.log(startF,base))/dataPoints):
        Th = .001/dudy
        Tl = base**(-1*exp)-Th
        if(sendOSC2(Tl,Th)):
            continue
        lista = [Tl,Th]
        listb = []
        for _ in range(40): #2 seconds of data becuse of 10hz send rate
            listb.append(GetV(511.0/11.0))
        lists.append(lista)
        lists.append(listb)
        print(lists)
        with open('out.txt','w') as filehandle:
            json.dump(lists, filehandle)
