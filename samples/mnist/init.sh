#!/bin/bash

source `dirname $0`/globals.sh
source `dirname $0`/push.sh

starcluster sshmaster $CLUSTER "$BASE_DIR/$MASTER_SETUP_ROOT_SCRIPT"
starcluster sshmaster $CLUSTER -u $CLUSTER_USER "$BASE_DIR/$MASTER_SETUP_SCRIPT"

#for i in $NODES
#do
	#echo "Setting up node $i"
	#starcluster sshnode $CLUSTER $i "/shared/$SETUP_SCRIPT"
#done

