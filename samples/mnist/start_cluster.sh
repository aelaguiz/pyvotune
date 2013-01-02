#!/bin/bash

source `dirname $0`/globals.sh

echo "Killing master"
starcluster sshmaster $CLUSTER -u $CLUSTER_USER "tmux kill-session -t master"

for i in $NODES
do
	echo "Killing $i..."
	starcluster sshnode $CLUSTER $i -u $CLUSTER_USER "tmux kill-session -t worker"
done

echo "Flushing master redis"
starcluster sshmaster $CLUSTER -u $CLUSTER_USER "redis-cli flushall"

starcluster sshmaster $CLUSTER -u $CLUSTER_USER "cd $PYVOTUNE_DIR && git pull"

echo "Starting master..."
starcluster sshmaster $CLUSTER -u $CLUSTER_USER "tmux new -d -s master $PYVOTUNE_DIR/$START_MASTER"

echo "Pausing"
sleep 5

`dirname $0`/start_nodes.sh
