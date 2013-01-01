#!/bin/bash

source `dirname $0`/globals.sh

echo "Killing master"
starcluster sshmaster $CLUSTER "tmux kill-session -t master"

for i in $NODES
do
	echo "Killing $i..."
	starcluster sshnode $CLUSTER $i "tmux kill-session -t worker"
done

echo "Flushing master redis"
starcluster sshmaster $CLUSTER "redis-cli flushall"
