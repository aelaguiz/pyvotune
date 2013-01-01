#!/bin/bash

CLUSTER='lark'
NODES="node001"
START_NODE_SCRIPT=_start_node.sh
START_NODE=samples/mnist/$START_NODE_SCRIPT

for i in $NODES
do
	starcluster sshnode $CLUSTER $i "tmux new -d -s worker /shared/$START_NODE_SCRIPT"
done

starcluster sshmaster $CLUSTER "tmux new -d -s worker /shared/$START_MASTER_SCRIPT"
#starcluster sshmaster $CLUSTER "/shared/$SETUP_SCRIPT"

