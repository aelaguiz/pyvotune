#!/bin/bash

source `dirname $0`/globals.sh

starcluster sshmaster $CLUSTER "/shared/$MASTER_SETUP_SCRIPT"
starcluster sshmaster $CLUSTER "/shared/$SETUP_SCRIPT"

for i in $NODES
do
	starcluster sshnode $CLUSTER $i "/shared/$SETUP_SCRIPT"
done

