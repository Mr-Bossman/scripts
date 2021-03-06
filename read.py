import sys
import math 
import matplotlib.pyplot as plt
import json
import numpy as np 
inct = 40
obj = 40
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
    color = ['r','g','b','c','m','y','k','r','g','b','c','m','y','k','r','g','b','c','m','y','k']
    with open('output.txt','r') as filehandle:
        lists = json.load( filehandle)
    dudy = lists[0][1]
    x = [[]]
    y = [[]]
    for arr in lists:
        if(len(arr) == 2):
            if(dudy != arr[1]):
                dudy = arr[1]
                x.append([])
                y.append([])
            if len(y[-1]):
                last = y[-1][-1]
            else:
                last = arr[0]
            jump = (arr[0]-last) / inct
            y[-1] += [(x * jump) + last for x in range(1,int(obj/inct)+1)]
        else:
            x[-1] += incavg(arr,inct)


    #for a in range(len(y)):
    #    for b in range(len(y[a])):
    #        dudy = (a*10)+10
    #        y[a][b] = (1/y[a][b])*(dudy/100)
  
    for i in range(0, len(y),1):
        plt.plot(y[i],x[i],color[i])
    plt.xscale('log')
    plt.draw()
    plt.pause(1)
    plt.clf()

