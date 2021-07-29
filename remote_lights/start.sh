#!/bin/bash
sudo echo ""
function kill(){
    ps -j -A | grep $py_PID  | awk '{print $3 }' | sudo xargs pkill -s 
}
trap kill EXIT
node test.js&
web_PID=$!
sudo python3 netC.py /dev/ttyUSB1 9600 ff 10.4.10.87 678&
py_PID=$!
while [ True ]; do
sleep 1
done

#python3 n
