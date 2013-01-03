#!/bin/bash

tmux kill-session -t redis

source `dirname $0`/globals.sh

echo "Cloning $PYVOTUNE_GIT"
git clone "$PYVOTUNE_GIT"

echo "Cloning $INSPYRED_GIT"
git clone "$INSPYRED_GIT"

tmux new -d -s redis /usr/local/bin/redis-server
sleep 1
echo "Flushing redis"
redis-cli flushall
