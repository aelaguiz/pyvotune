#!/bin/bash

source `dirname $0`/globals.sh

#source `dirname $0`/stop_cluster.sh

starcluster sshmaster $CLUSTER -u $CLUSTER_USER "cd $PYVOTUNE_DIR && git pull"

echo "Starting master..."
starcluster sshmaster $CLUSTER -u $CLUSTER_USER "tmux new -d -s master $PYVOTUNE_DIR/$START_MASTER"

echo "Pausing"
sleep 5

`dirname $0`/start_nodes.sh
