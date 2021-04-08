#!/bin/python3
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import time
import ffmpeg
import signal
import socket 
import select 
import sys
import threading
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
if len(sys.argv) != 5: 
    print ("Correct usage: script, server IP, Local IP address, server port number client port")
    exit() 
IP_address = str(sys.argv[2]) 
Port = int(sys.argv[4]) 
server_address = "tcp://" + sys.argv[1] + ":" + sys.argv[3]
server.bind((IP_address, Port)) 
server.listen(10) 
list_of_clients = [] 
pid  = []
stream_pid = 0
st = time.perf_counter()
net = False 
exi = False


def signal_handler(sig, frame):
    for connection in list_of_clients: 
        list_of_clients.remove(connection)     
    server.close()
    exi = True
    for id in pid:
        id.kill()
    sys.exit(0)





def clientthread(conn, addr): 
    global net
    global stream_pid
    global pid
    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 
                    if str(message).find("stream") != -1:
                        net = True
                    if str(message).find("end") != -1:
                        net = False
                    if str(message).find("kill") != -1:
                        pid.remove(stream_pid)
                        stream_pid.kill()   
                        stream_pid = 0
                else:
                    net = False 
                    remove(conn) 
            except: 
                continue
  
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
def stream(server_url):
    video_format = "mpegts"
    return (
        ffmpeg
        .input("/dev/video2", 
            format = "v4l2",
            r = "30")
        .output(
            server_url, 
            codec = "mpeg4", # use same codecs of the original video
            f="mpegts",
            pix_fmt='yuv420p',
            video_bitrate = "600k",
            audio_bitrate = "0",
            g = "600",
            r = "30"
            )
        .global_args("-re", "-hide_banner" ,"-loglevel", "panic") # argument to act as a live stream
        .run_async()
    )


def copy(out):
    video_format = "mpegts"
    return (
        ffmpeg
        .input("/dev/video0", 
            format = "v4l2",
            r = "30")
        .output(
            out, 
            format = "v4l2",
            r = "30"
            )
        .global_args("-re", "-hide_banner" ,"-loglevel", "panic") # argument to act as a live stream
        .run_async()
    )

def start(check):
    global net
    global st
    global stream_pid
    global pid
    global server_address
    if(not check):
        st = time.perf_counter()
    if(stream_pid == 0 and not check):
        stream_pid = stream(server_address)
        pid.append(stream_pid)
    if(stream_pid == 0 and net):
        stream_pid = stream(server_address)
        pid.append(stream_pid)
    if(time.perf_counter()-st > 200):
        if(not (net or stream_pid == 0)) :
            pid.remove(stream_pid)
            stream_pid.kill()   
            stream_pid = 0
def motionDetection():
    global exi
    times = 5
    cap = cv.VideoCapture("/dev/video2")
    ret, frameL = cap.read()
    ret, frame = cap.read()
    frameMash = cv.absdiff(frameL,frame)
    for frames in range(0,times):
        ret, frame = cap.read()
        diff = cv.absdiff(frameL, frame)
        frameMash = cv.addWeighted(diff,0.2,frameMash,0.75,0)
        frameL = frame


    while cap.isOpened():
        diff_gray = cv.cvtColor(frameMash, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(cv.addWeighted( diff_gray, 1.2, diff_gray, 0, 1.1), (5, 5), 0)
        _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
        dilated = cv.dilate(thresh, None, iterations=3)
        contours, _ = cv.findContours(
            dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv.boundingRect(contour)
            if cv.contourArea(contour) < 400:
                continue
            if cv.contourArea(contour) >5000:
                continue
            start(False)
            break
        start(True)
        for frames in range(0,times):
            ret, frame = cap.read()
            diff = cv.absdiff(frameL, frame)
            frameMash = cv.addWeighted(diff,0.7,frameMash,0.3,0)    
            frameL = frame
        if exi:
            break


    cap.release()


 
 
signal.signal(signal.SIGINT, signal_handler)
pid.append(copy("/dev/video2"))
T1 = threading.Thread(target=motionDetection)
T1.start()
while True: 
    conn, addr = server.accept() 
    list_of_clients.append(conn) 
  
    T2 = threading.Thread(target=clientthread,args=(conn,addr))
    T2.start()    









