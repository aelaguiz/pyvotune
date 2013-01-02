#!/bin/bash

source `dirname $0`/globals.sh

cd $BASE_DIR
wget http://redis.googlecode.com/files/redis-2.4.18.tar.gz
tar -zxvf redis-2.4.18.tar.gz
cd redis-2.4.18
make -j8 install
