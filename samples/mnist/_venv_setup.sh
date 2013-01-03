#!/bin/bash

source `dirname $0`/globals.sh

cd $BASE_DIR
virtualenv --distribute venv 
source venv/bin/activate

cd $BASE_DIR/inspyred
pip uninstall inspyred -y
pip install paver
./build_distribution.sh
python setup.py install

cd $PYVOTUNE_DIR
git pull
pip install -r requirements.txt
pip install git+https://github.com/nvie/rq.git
pip install redis
pip install hiredis
