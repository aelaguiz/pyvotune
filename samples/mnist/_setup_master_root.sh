#!/bin/bash

source `dirname $0`/globals.sh

rm -rf /usr/local/lib/python2.7/dist-packages/redis*
rm -rf /usr/local/lib/python2.7/dist-packages/hiredis*
rm -rf /usr/local/lib/python2.7/dist-packages/times*
rm -rf /usr/local/lib/python2.7/dist-packages/scikit-learn*
rm -rf /usr/local/lib/python2.7/dist-packages/scikit_learn*
rm -rf /usr/local/lib/python2.7/dist-packages/sklearn*
rm -rf /usr/local/lib/python2.7/dist-packages/numpy*
rm -rf /usr/local/lib/python2.7/dist-packages/scipy*
rm -rf /usr/local/lib/python2.7/dist-packages/six*

cd $BASE_DIR
wget http://redis.googlecode.com/files/redis-2.4.18.tar.gz
tar -zxvf redis-2.4.18.tar.gz
cd redis-2.4.18
make -j8 install
