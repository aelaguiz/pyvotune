#!/bin/bash

source `dirname $0`/globals.sh

starcluster sshmaster $CLUSTER -u $CLUSTER_USER "cd $PYVOTUNE_DIR && git pull"

echo "Killing master"
starcluster sshmaster $CLUSTER "tmux kill-session -t master"

echo "Flushing master redis"
starcluster sshmaster $CLUSTER "redis-cli flushall"

echo "Starting master..."
starcluster sshmaster $CLUSTER -u $CLUSTER_USER "tmux new -d -s master $PYVOTUNE_DIR/$START_MASTER"

#echo "Pausing"
#sleep 5

#`dirname $0`/start_nodes.sh
