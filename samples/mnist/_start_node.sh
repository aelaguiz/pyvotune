#!/bin/bash

cd /home/pyvotune

ps aux | grep python | awk '{print $2}' | xargs kill

if [ -e /mnt/mnist.txt ];
then
	mv /mnt/mnist.txt.bak
fi

PYTHONPATH=. python samples/mnist/main.py -r redis://master -n 64 -g 0 -s 0 -m 0 -c 0 -t 0 -d -w  >> /mnt/mnist.txt 2>&1
