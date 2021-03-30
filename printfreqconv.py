import sys
import math 
import matplotlib.pyplot as plt
import json
import numpy as np 
from os import walk
output_path = "./output"
def files():
    f = []
    for (dirpath, dirnames, filenames) in walk(output_path):
        f.extend(filenames)
        break
    return f
inct = 20
obj = 20
def incavg(arr, inc):
    ret = []
    for a in range(0,len(arr),inc):
        avg = 0.0
        for b in range(inc-1):
            avg += arr[a+b]
        avg /= inc
        if avg > 60:
            avg = 5
        ret.append(avg)
    return ret
while True:
    color = ['r','g','b','c','m','y','k','r','g','b','c','m','y','k','r','g','b','c','m','y','k','r','g','b','c','m','y','k','r','g','b','c','m','y','k','r','g','b','c','m','y','k']
    dudy = [[[],[]]]
    file_names = files()
    for i in range(len(file_names)):
        if(len(dudy)-1 > i):
            continue
        dudy.append([[],[]])
        with open(output_path+ "/" + file_names[i],'r') as filehandle:
            lists = json.load( filehandle)
        for index in range(len(lists)):
            if type(lists[index]) is float:
                dudy[i][0] += [float(file_names[i])/(100*lists[index])]*len(lists[index+1])
            else:
                dudy[i][1] += lists[index]
        #for a in range(len(y)):
        #    for b in range(len(y[a])):
        #        dudy = (a*10)+10
        #        y[a][b] = (1/y[a][b])*(dudy/100)
    for i in range(len(dudy)):
        plt.plot(dudy[i][0],dudy[i][1],color[i])
    plt.xscale('log')
    plt.draw()
    plt.pause(.1)
    plt.clf()

