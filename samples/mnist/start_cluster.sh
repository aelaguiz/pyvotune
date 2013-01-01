#!/bin/bash

source `dirname $0`/globals.sh
source `dirname $0`/push.sh

echo "Killing master"
starcluster sshmaster $CLUSTER "tmux kill-session -t master"

for i in $NODES
do
	echo "Killing $i..."
	starcluster sshnode $CLUSTER $i "tmux kill-session -t worker"
done

echo "Flushing master redis"
starcluster sshmaster $CLUSTER "redis-cli flushall"

starcluster sshmaster $CLUSTER "cd /shared/pyvotune && git pull"

for i in $NODES
do
	echo "Starting $i..."
	starcluster sshnode $CLUSTER $i "tmux new -d -s worker /shared/$START_NODE_SCRIPT"
done

echo "Starting master..."
starcluster sshmaster $CLUSTER "tmux new -d -s master /shared/$START_MASTER_SCRIPT"
