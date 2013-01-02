#!/bin/bash

source `dirname $0`/globals.sh

#starcluster sshmaster $CLUSTER "/etc/init.d/nfs-kernel-server restart"

for i in $NODES
do
	starcluster sshnode $CLUSTER $i "mount /home"
done


