from rq import Queue, Worker, Connection
from multiprocessing import Pool
import redis

from pyvotune.log import logger
log = logger()


def _start_worker(con_str, queue):
    try:
        con = redis.from_url(con_str)

        with Connection(con):
            worker = Worker(Queue(queue))
            worker.work()
    except:
        log.exception("Worker excepted")


def start_workers(processes, con_str, queue='pyvotune'):
    pool = Pool(processes)

    for i in range(processes):
        pool.apply_async(_start_worker, (con_str, queue, ))
