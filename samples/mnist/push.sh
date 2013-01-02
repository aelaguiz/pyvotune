#!/bin/bash

source `dirname $0`/globals.sh

starcluster put $CLUSTER -u $CLUSTER_USER `dirname $0`/globals.sh $BASE_DIR/.
starcluster put $CLUSTER -u $CLUSTER_USER $MASTER_SETUP $BASE_DIR/.
starcluster put $CLUSTER -u $CLUSTER_USER $MASTER_SETUP_ROOT $BASE_DIR/.
starcluster put $CLUSTER -u $CLUSTER_USER ~/.ssh/id_rsa.pub /home/$CLUSTER_USER/.ssh/.
