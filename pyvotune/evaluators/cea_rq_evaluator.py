from rq import Worker, Queue, Connection
from rq.job import Status, NoSuchJobError

import pyvotune.evaluators.cea_rq_runner

from .util import get_args

import functools
import time
import redis

__async_results = []
__async_queue = None


def get_queue(args):
    global __async_queue

    if __async_queue:
        return __async_queue

    name = args.setdefault('rq_name', 'pyvotune')

    host = args.setdefault('rq_host', 'localhost')
    port = args.setdefault('rq_port', 6379)
    db = args.setdefault('rq_db', 0)
    password = args.setdefault('rq_password', '')

    con = redis.StrictRedis(host=host, port=port, db=db, password=password)

    __async_queue = Queue(name, connection=con)

    return __async_queue


def cell_evaluator_rq(individuals, callback_fn, args):
    """
    Evaluator function will asynchronously dispatch any new individuals
    for evaluation and block while there are outstanding evaluations.

    This functions by maintaining a single global process pool which is
    spun up on demand and then maintained until `cell_evaluator_mp_cleanup`
    is called.

    This allows asynchronous operations to take place because the callback
    into the actual algorithm will allow new asynchronous operations to
    be enqueued in a recursive manner.
    """
    global __async_results

    logger = args['_ec'].logger
    rq_timeout = args.setdefault('rq_timeout', 60)

    if individuals:
        queue = get_queue(args)

        pickled_args = get_args(args)

        for idx, ind in individuals:
            #res = pyvotune.evaluators.cea_rq_runner.rq_runner([ind.candidate], args)
            #ind.fitness = res
            #callback_fn(idx, ind)
            job = queue.enqueue_call(
                func=pyvotune.evaluators.cea_rq_runner.rq_runner,
                args=( 
                    [ind.candidate], pickled_args),
                timeout=rq_timeout*3)
           
            #logger.debug("Dispatching {0} for evaluation".format(
                #ind))
            __async_results.append((idx, callback_fn, ind, job, None))

    defered, __async_results = dispatch_results(__async_results, args)
    [callback_fn(idx, ind) for (idx, callback_fn, ind) in defered]


def dispatch_results(async_results, args):
    """Calls the evaluation callback for any asynchronous evaluations which have
    finished processing and returned results.
    """

    timeout_val = args.setdefault('rq_timeout_fitness', 0)
    rq_timeout = args.setdefault('rq_timeout', 60)

    logger = args['_ec'].logger

    defered = []

    remaining_results = []

    running_count = 0
    for idx, callback_fn, ind, job, start_time in list(async_results):
        job_dead = False

        try:
            job.refresh()
        except NoSuchJobError as e:
            logger.debug("Job {0} does not exist anymore".format(
                job))
            job_dead = True

        #logger.debug("Job {0} Status {1}".format(
            #job, job.status))
        if job_dead or job.status == Status.FAILED or \
                (job.status == Status.FINISHED and job.result is None) or\
                (job.status == Status.STARTED and start_time is not None and
                    (time.time()-start_time) > (rq_timeout+5)):

            logger.warning("Failed getting fitness for {0} ind, after {1}".format(
                ind, (time.time() - start_time) if start_time else None))

            ind.fitness = timeout_val

            defered.append((idx, callback_fn, ind))
        elif job.status == Status.FINISHED and job.result is not None:
            ret = job.result

            #logger.debug("Received results from {0} = {1} after {2}s".format(
                #ind, ret, (time.time() - start_time)))

            ind.fitness = ret

            defered.append((idx, callback_fn, ind))
        else:
            if job.status == Status.STARTED:
                running_count += 1
                if start_time is None:
                    #logger.debug("Job {0} - {1} started".format(
                        #idx, ind))
                    start_time = time.time()
            #logger.debug("Continuing to wait for {0} after {1} seconds".format(
                #idx, (time.time() - start_time)))
            remaining_results.append((idx, callback_fn, ind, job, start_time))

    logger.debug("{0} jobs running, {1} total".format(
        running_count, len(async_results)))

    return defered, remaining_results


def get_evaluator(args):
    logger = args['_ec'].logger

    try:
        return args['rq_evaluator']
    except KeyError:
        logger.error('cea_rq_evaluator requires \'rq_evaluator\' be defined in the keyword arguments list')
        raise 
