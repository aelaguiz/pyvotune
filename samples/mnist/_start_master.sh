#!/bin/bash

cd /home/pyvotune

ps aux | grep python | awk '{print $2}' | xargs kill

if [ -e /mnt/mnist.txt ];
then
	mv /mnt/mnist.txt.bak
fi

PYTHONPATH=. python samples/mnist/main.py -r redis://master -n 0 -g 10 -s 2 -m 0.3 -c 0.5 -t 30 -d -w  >> /mnt/mnist.txt 2>&1
