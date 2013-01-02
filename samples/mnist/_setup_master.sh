#!/bin/bash

tmux kill-session -t redis

source `dirname $0`/globals.sh

echo "Cloning $PYVOTUNE_GIT"
git clone "$PYVOTUNE_GIT"

echo "Cloning $INSPYRED_GIT"
git clone "$INSPYRED_GIT"

tmux new -d -s redis /usr/local/bin/redis-server
sleep 1
echo "Flushing redis"
redis-cli flushall

cd $BASE_DIR
virtualenv --distribute venv 
source venv/bin/activate

cd $BASE_DIR/inspyred
pip uninstall inspyred -y
pip install paver
./build_distribution.sh
python setup.py install

cd $PYVOTUNE_DIR
pip install -r requirements.txt
pip install git+https://github.com/nvie/rq.git
