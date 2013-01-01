#!/bin/bash

source `dirname $0`/globals.sh

echo "Setting up node"

cd /shared/inspyred
pip uninstall inspyred -y
pip install paver
./build_distribution.sh
python setup.py install

cp -r /shared/pyvotune $BASE_DIR/

cd $PYVOTUNE_DIR
pip install -r requirements.txt
pip uninstall rq -y

mv /usr/local/lib/python2.7/dist-packages/rq-0.3.0-py2.7.egg-info/ /tmp/.
pip install -U git+https://github.com/nvie/rq.git
