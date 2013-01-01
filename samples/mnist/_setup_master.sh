#!/bin/bash

tmux kill-session -t redis

cd /home
wget http://redis.googlecode.com/files/redis-2.4.18.tar.gz
tar -zxvf redis-2.4.18.tar.gz
cd redis-2.4.18
make -j8 install
tmux new -d -s redis /usr/local/bin/redis-server
