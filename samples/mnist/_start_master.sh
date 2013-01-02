#!/bin/bash

source `dirname $0`/globals.sh

ps aux | grep python | awk '{print $2}' | xargs kill

cd $BASE_DIR
source venv/bin/activate
cd $PYVOTUNE_DIR
PYTHONPATH=. python samples/mnist/main.py -r redis://localhost:6379 -n 0 -g $GRID_SIZE -s $NEIGHBORHOOD_SIZE -m $MUTATION_RATE -c $CROSSOVER_RATE -u $NUM_SAMPLES -t $EVAL_TIMEOUT -l $MAX_LENGTH -d 
