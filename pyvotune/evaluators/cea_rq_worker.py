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


def start_workers(processes, con_str, queue='pyvotune'):
    for i in range(processes):
        p = Process(target=_start_worker, args=(con_str, queue))
        p.start()
