#!/bin/bash

source `dirname $0`/globals.sh
source `dirname $0`/push.sh

starcluster sshmaster $CLUSTER "cd /shared/pyvotune && git pull"

starcluster sshmaster $CLUSTER "/shared/$MASTER_SETUP_SCRIPT"
starcluster sshmaster $CLUSTER "/shared/$SETUP_SCRIPT"

for i in $NODES
do
	echo "Setting up node $i"
	starcluster sshnode $CLUSTER $i "/shared/$SETUP_SCRIPT"
done

