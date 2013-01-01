#!/bin/bash

source `dirname $0`/globals.sh

starcluster put $CLUSTER $SETUP /shared/.

starcluster sshmaster $CLUSTER "/shared/$MASTER_SETUP_SCRIPT"
