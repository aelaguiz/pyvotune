#!/bin/bash

echo "Setting up node"
cd /shared/inspyred
pip uninstall inspyred -y
pip install paver
./build_distribution.sh
python setup.py install

cp -r /shared/pyvotune /home/
cd /home/pyvotune

pip install -r requirements.txt
pip install git+https://github.com/nvie/rq.git
