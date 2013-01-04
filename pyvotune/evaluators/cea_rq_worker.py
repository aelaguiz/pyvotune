# -*- coding: utf-8 -*-

from rq import Queue, Worker, Connection
from multiprocessing import Process
import redis
import logging

from pyvotune.log import logger
log = logger()


def _start_worker(con_str, queue):
    try:
        con = redis.from_url(con_str)

        with Connection(con):
            worker = Worker(Queue(queue))
            #worker.log.level = 'WARNING'
            worker.work()
    except Exception as e:
        log.exception("Worker excepted %s" % e)


def start_pool(host, port, password, db, queue='pyvotune'):
    import pysplash

    log.debug("Starting pool with %s %s %s %s" % (
        host, port, password, db))

    pool = pysplash.Pool(
        [queue], host=host, port=port, password=password,
        db=db, max_cpu=120.)

    log.debug("Starting pool")
    pool.start()
