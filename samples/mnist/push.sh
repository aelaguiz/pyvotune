#!/bin/bash

CLUSTER='lark'
NODES="node001"
MASTER_SETUP_SCRIPT=_setup_master.sh
MASTER_SETUP=samples/mnist/$MASTER_SETUP_SCRIPT
SETUP_SCRIPT=setup_cluster.sh
SETUP=samples/mnist/$SETUP_SCRIPT
START_NODE_SCRIPT=_start_node.sh
START_NODE=samples/mnist/$START_NODE_SCRIPT
START_MASTER_SCRIPT=_start_node.sh
START_MASTER=samples/mnist/$START_MASTER_SCRIPT

starcluster put $CLUSTER $MASTER_SETUP /shared/.
starcluster put $CLUSTER $SETUP /shared/.
starcluster put $CLUSTER $START_NODE /shared/.
starcluster put $CLUSTER $START_MASTER /shared/.

starcluster sshmaster $CLUSTER "/shared/$MASTER_SETUP_SCRIPT"
starcluster sshmaster $CLUSTER "/shared/$SETUP_SCRIPT"

for i in $NODES
do
	starcluster sshnode $CLUSTER $i "/shared/$SETUP_SCRIPT"
done
