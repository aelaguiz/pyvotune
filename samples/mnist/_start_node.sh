#!/bin/bash

source `dirname $0`/globals.sh

ps aux | grep python | awk '{print $2}' | xargs kill

if [ -e /mnt/mnist.txt ];
then
	mv /mnt/mnist.txt.bak
fi

cd /home/pyvotune
PYTHONPATH=. python samples/mnist/main.py -r redis://master:6379 -n $NUM_WORKERS -g $GRID_SIZE -s $NEIGHBORHOOD_SIZE -m $MUTATION_RATE -c $CROSSOVER_RATE -u $NUM_SAMPLES -t $EVAL_TIMEOUT -l $MAX_LENGTH -d  >> /mnt/mnist.txt 2>&1
