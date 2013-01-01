#!/bin/bash

CLUSTER='lark'
MASTER_SETUP_SCRIPT=_setup_master.sh
SETUP=samples/mnist/$MASTER_SETUP_SCRIPT

starcluster put $CLUSTER $SETUP /shared/.

starcluster sshmaster $CLUSTER "/shared/$MASTER_SETUP_SCRIPT"

tmux new -d -s redis /usr/local/bin/redis-server
redis-cli localhost flushall
