#!/bin/bash

source `dirname $0`/globals.sh

echo "Killing master"
starcluster sshmaster $CLUSTER "tmux kill-session -t master"

source `dirname $0`/stop_nodes.sh

echo "Flushing master redis"
starcluster sshmaster $CLUSTER "redis-cli flushall"
