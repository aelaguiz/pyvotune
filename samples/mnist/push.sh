#!/bin/bash

source `dirname $0`/globals.sh

starcluster put $CLUSTER `dirname $0`/globals.sh /shared/.
starcluster put $CLUSTER $MASTER_SETUP /shared/.
starcluster put $CLUSTER $SETUP /shared/.
starcluster put $CLUSTER $START_NODE /shared/.
starcluster put $CLUSTER $START_MASTER /shared/.
