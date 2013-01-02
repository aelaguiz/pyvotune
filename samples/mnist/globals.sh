#!/bin/bash

CLUSTER='lark'
CLUSTER_USER='ubuntu'
#NODES=""
#NODES="node001"
NODES="node001 node002 node003 node004 node005 node006 node007 node008 node009 node010 node011 node012 node013 node014"

INSPYRED_GIT=https://github.com/aelaguiz/inspyred.git
PYVOTUNE_GIT=https://github.com/aelaguiz/pyvotune.git

BASE_DIR=/home/ubuntu
PYVOTUNE_DIR=$BASE_DIR/pyvotune

MASTER_SETUP_SCRIPT=_setup_master.sh
MASTER_SETUP=samples/mnist/$MASTER_SETUP_SCRIPT

MASTER_SETUP_ROOT_SCRIPT=_setup_master_root.sh
MASTER_SETUP_ROOT=samples/mnist/$MASTER_SETUP_ROOT_SCRIPT

SETUP_SCRIPT=setup_cluster.sh
SETUP=samples/mnist/$SETUP_SCRIPT

START_NODE_SCRIPT=_start_node.sh
START_NODE=samples/mnist/$START_NODE_SCRIPT

START_MASTER_SCRIPT=_start_master.sh
START_MASTER=samples/mnist/$START_MASTER_SCRIPT

NUM_SAMPLES=42000
#NUM_SAMPLES=4000
CROSSOVER_RATE=0.5
MUTATION_RATE=0.3
NEIGHBORHOOD_SIZE=2
GRID_SIZE=30
NUM_WORKERS=32
EVAL_TIMEOUT=300
MAX_LENGTH=5
