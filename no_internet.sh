#!/bin/bash

while [ True ]
do
if ! ping 10.4.1.1 -c 1 ; then
	systemctl restart networking
fi
sleep 5
done
