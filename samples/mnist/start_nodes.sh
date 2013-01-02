#!/bin/bash

source `dirname $0`/globals.sh

for i in $NODES
do
	echo "Starting $i..."
	starcluster sshnode $CLUSTER $i -u $CLUSTER_USER "tmux new -d -s worker $PYVOTUNE_DIR/$START_NODE"
done

