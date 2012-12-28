# -*- coding: utf-8 -*-

from pyvotune.log import logger
import functools
try:
    import cPickle as pickle
except ImportError:
    import pickle

log = logger()


def parallel_evaluation_mp(candidates, args):
    """
    Borrowed and modified from inspyred.ec.evaluators. Added a timeout.

    Evaluate the candidates in parallel using ``multiprocessing``.

    This function allows parallel evaluation of candidate solutions.
    It uses the standard multiprocessing library to accomplish the
    parallelization. The function assigns the evaluation of each
    candidate to its own job, all of which are then distributed to the
    available processing units.

    .. note::

       All arguments to the evaluation function must be pickleable.
       Those that are not will not be sent through the ``args`` variable
       and will be unavailable to your function.

    .. Arguments:
       candidates -- the candidate solutions
       args -- a dictionary of keyword arguments

    Required keyword arguments in args:

    - *mp_evaluator* -- actual evaluation function to be used (This function
      should have the same signature as any other inspyred evaluation function.)

    Optional keyword arguments in args:

    - *mp_timeout* -- maximum number of seconds the evaluation is allowed to
      execute for (default 30.0)

    - *mp_timeout_return -- return value to be used for a timedout evaluation
      (default 0), generally will want this to be very high if attempting to
      minimize or very low if attempting to maximize

    - *mp_nprocs* -- number of processors that will be used (default machine
      cpu count)

    """
    import time
    import multiprocessing

    try:
        evaluator = args['mp_evaluator']
    except KeyError:
        log.error('parallel_evaluation_mp requires \'mp_evaluator\' be defined in the keyword arguments list')
        raise
    try:
        nprocs = args['mp_nprocs']
    except KeyError:
        nprocs = multiprocessing.cpu_count()

    timeout = args.setdefault('mp_timeout', 30)
    timeout_retval = args.setdefault('mp_timeout_return', 0)

    pickled_args = {}
    for key in args:
        try:
            pickle.dumps(args[key])
            pickled_args[key] = args[key]
        except (TypeError, pickle.PickleError, pickle.PicklingError):
            log.debug('unable to pickle args parameter {0} in parallel_evaluation_mp'.format(key))
            pass

    start = time.time()
    try:
        pool = multiprocessing.Pool(processes=nprocs)
        results = [pool.apply_async(
            evaluator, ([c], pickled_args)) for c in candidates]
        outstanding_results = list(results)

        while outstanding_results:
            duration = time.time() - start
            if duration > timeout:
                log.error(u"Timed out waiting for processes to finish after {0} seconds".format(
                    duration))
                pool.terminate()
                pool.join()

                res = []
                for r, c in zip(results, candidates):
                    if r.ready():
                        res.append(r.get()[0])
                    else:
                        log.warning(u"Timed out for candidate {0}".format(c))
                        res.append(timeout_retval)

                return res

            outstanding_results = [r for r in outstanding_results if not r.ready()]

            time.sleep(0.2)

        pool.close()
        pool.join()
        return [r.get()[0] for r in results]
    except (OSError, RuntimeError) as e:
        log.error('failed parallel_evaluation_mp: {0}'.format(str(e)))
        raise
    else:
        end = time.time()
        log.debug('completed parallel_evaluation_mp in {0} seconds'.format(
            end - start))
