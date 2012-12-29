__all__ = ['Pool']

#
# Imports
#

import threading
import Queue
import itertools
import collections
import time
import os

from pyvotune.log import logger

import multiprocessing
from multiprocessing import Process, cpu_count, TimeoutError
from multiprocessing.util import Finalize, log_to_stderr
from multiprocessing.pool import TERMINATE, CLOSE, RUN, Pool, IMapIterator, IMapUnorderedIterator, mapstar, ApplyResult, MapResult
from logging import DEBUG


log = logger()


def worker(proc_num, inqueue, outqueue, initializer=None, initargs=(), maxtasks=None):
    print "In worker process"
    try:
        log.debug("Worker {0} asserting".format(maxtasks))
        assert maxtasks is None or (type(maxtasks) == int and maxtasks > 0)
        put = outqueue.put
        get = inqueue.get

        log.debug("Worker {0} started".format(proc_num))

        if initializer is not None:
            initializer(*initargs)

        completed = 0
        while maxtasks is None or (maxtasks and completed < maxtasks):
            try:
                task = get()
            except (EOFError, IOError):
                log.debug('worker got EOFError or IOError -- exiting')
                break

            if task is None:
                log.debug('worker got sentinel -- exiting')
                break

            job, i, func, args, kwds = task
            try:
                put((job, i, proc_num, 'started'))
                log.debug("Worker {0} starting job {1} {2} {3}".format(
                    proc_num, job, func, args))

                result = (True, func(*args, **kwds))

                log.debug("Worker {0} finished job {1} {2} {3}".format(
                    proc_num, job, func, args))
            except Exception, e:
                log.exception("Exception in worker {0} - {1} - {2} {3} {4}".format(
                    proc_num, e, job, func, args))
                result = (False, e)
            put((job, i, proc_num, result))
            completed += 1
        log.debug('worker exiting after %d tasks' % completed)
    except:
        log.exception("Worker excepted {0}".format(
            proc_num))


class TimeoutPool(object):
    '''
    Class which supports an async version of the `apply()` builtin
    '''
    Process = Process

    def __init__(self, processes=None, initializer=None, initargs=(),
                 maxtasksperchild=None, timeout_seconds=30):
        log_to_stderr(level=DEBUG)

        self._setup_queues()
        self._taskqueue = Queue.Queue()
        self._cache = {}
        self._state = RUN
        self._maxtasksperchild = maxtasksperchild
        self._initializer = initializer
        self._initargs = initargs
        self._proc_num = 0

        if processes is None:
            try:
                processes = cpu_count()
            except NotImplementedError:
                processes = 1

        if initializer is not None and not hasattr(initializer, '__call__'):
            raise TypeError('initializer must be a callable')

        self._processes = processes
        self._pool = []
        self._repopulate_pool()

        self._worker_handler = threading.Thread(
            target=Pool._handle_workers,
            args=(self, )
        )

        self._worker_handler.daemon = True
        self._worker_handler._state = RUN
        self._worker_handler.start()

        self._task_handler = threading.Thread(
            target=Pool._handle_tasks,
            args=(self._taskqueue, self._quick_put, self._outqueue, self._pool)
        )

        self._task_handler.daemon = True
        self._task_handler._state = RUN
        self._task_handler.start()

        self.timeout_seconds = timeout_seconds

        self._result_handler = threading.Thread(
            target=TimeoutPool._handle_results,
            args=(self._outqueue, self._quick_get, self._cache, self._pool, self.timeout_seconds)
        )

        self._result_handler.daemon = True
        self._result_handler._state = RUN
        self._result_handler.start()

        self._terminate = Finalize(
            self, self._terminate_pool,
            args=(self._taskqueue, self._inqueue, self._outqueue, self._pool,
                  self._worker_handler, self._task_handler,
                  self._result_handler, self._cache),
            exitpriority=15
        )

    def _join_exited_workers(self):
        """Cleanup after any worker processes which have exited due to reaching
        their specified lifetime.  Returns True if any workers were cleaned up.
        """
        cleaned = False
        for i in reversed(range(len(self._pool))):
            worker = self._pool[i]
            if worker.exitcode is not None:
                # worker exited
                log.debug('cleaning up worker %d' % i)
                worker.join()
                cleaned = True
                del self._pool[i]

        return cleaned

    def _repopulate_pool(self):
        """Bring the number of pool processes up to the specified number,
        for use after reaping workers which have exited.
        """
        for i in range(self._processes - len(self._pool)):
            proc_num = self._proc_num
            self._proc_num += 1
            w = self.Process(target=worker,
                             args=(proc_num,
                                   self._inqueue, self._outqueue,
                                   self._initializer,
                                   self._initargs,
                                   self._maxtasksperchild)
                             )
            w._proc_num = proc_num
            self._pool.append(w)
            w.name = w.name.replace('Process', 'PoolWorker')
            w.daemon = True
            w.start()
            log.debug("groups {0}".format(os.getgroups()))
            log.debug('added worker {0} {1}'.format(w.name, len(self._pool) - 1))

    def _maintain_pool(self):
        """Clean up any exited workers and start replacements for them.
        """
        if self._join_exited_workers():
            self._repopulate_pool()

    def _setup_queues(self):
        from multiprocessing.queues import SimpleQueue
        self._inqueue = SimpleQueue()
        self._outqueue = multiprocessing.Queue()
        self._quick_put = self._inqueue._writer.send
        self._quick_get = self._outqueue.get

    def apply(self, func, args=(), kwds={}):
        '''
        Equivalent of `apply()` builtin
        '''
        assert self._state == RUN
        return self.apply_async(func, args, kwds).get()

    def map(self, func, iterable, chunksize=None):
        '''
        Equivalent of `map()` builtin
        '''
        assert self._state == RUN
        return self.map_async(func, iterable, chunksize).get()

    def imap(self, func, iterable, chunksize=1):
        '''
        Equivalent of `itertools.imap()` -- can be MUCH slower than `Pool.map()`
        '''
        assert self._state == RUN
        if chunksize == 1:
            result = IMapIterator(self._cache)
            self._taskqueue.put((((result._job, i, func, (x,), {})
                                  for i, x in enumerate(iterable)), result._set_length))
            return result
        else:
            assert chunksize > 1
            task_batches = Pool._get_tasks(func, iterable, chunksize)
            result = IMapIterator(self._cache)
            self._taskqueue.put((((result._job, i, mapstar, (x,), {})
                                  for i, x in enumerate(task_batches)), result._set_length))
            return (item for chunk in result for item in chunk)

    def imap_unordered(self, func, iterable, chunksize=1):
        '''
        Like `imap()` method but ordering of results is arbitrary
        '''
        assert self._state == RUN
        if chunksize == 1:
            result = IMapUnorderedIterator(self._cache)
            self._taskqueue.put((((result._job, i, func, (x,), {})
                                  for i, x in enumerate(iterable)), result._set_length))
            return result
        else:
            assert chunksize > 1
            task_batches = Pool._get_tasks(func, iterable, chunksize)
            result = IMapUnorderedIterator(self._cache)
            self._taskqueue.put((((result._job, i, mapstar, (x,), {})
                                  for i, x in enumerate(task_batches)), result._set_length))
            return (item for chunk in result for item in chunk)

    def apply_async(self, func, args=(), kwds={}, callback=None):
        '''
        Asynchronous equivalent of `apply()` builtin
        '''
        assert self._state == RUN
        result = ApplyResult(self._cache, callback)
        self._taskqueue.put(([(result._job, None, func, args, kwds)], None))
        return result

    def map_async(self, func, iterable, chunksize=None, callback=None):
        '''
        Asynchronous equivalent of `map()` builtin
        '''
        assert self._state == RUN
        if not hasattr(iterable, '__len__'):
            iterable = list(iterable)

        if chunksize is None:
            chunksize, extra = divmod(len(iterable), len(self._pool) * 4)
            if extra:
                chunksize += 1
        if len(iterable) == 0:
            chunksize = 0

        task_batches = Pool._get_tasks(func, iterable, chunksize)
        result = MapResult(self._cache, chunksize, len(iterable), callback)
        self._taskqueue.put((((result._job, i, mapstar, (x,), {})
                              for i, x in enumerate(task_batches)), None))
        return result

    @staticmethod
    def _handle_workers(pool):
        while pool._worker_handler._state == RUN and pool._state == RUN:
            pool._maintain_pool()
            time.sleep(0.1)
        # send sentinel to stop workers
        pool._taskqueue.put(None)
        log.debug('worker handler exiting')

    @staticmethod
    def _handle_tasks(taskqueue, put, outqueue, pool):
        thread = threading.current_thread()

        for taskseq, set_length in iter(taskqueue.get, None):
            i = -1
            for i, task in enumerate(taskseq):
                if thread._state:
                    log.debug('task handler found thread._state != RUN')
                    break
                try:
                    put(task)
                except IOError:
                    log.debug('could not put task on queue')
                    break
            else:
                if set_length:
                    log.debug('doing set_length()')
                    set_length(i + 1)
                continue
            break
        else:
            log.debug('task handler got sentinel')

        try:
            # tell result handler to finish when cache is empty
            log.debug('task handler sending sentinel to result handler')
            outqueue.put(None)

            # tell workers there is no more work
            log.debug('task handler sending sentinel to workers')
            for p in pool:
                put(None)
        except IOError:
            log.debug('task handler got IOError when sending sentinels')

        log.debug('task handler exiting')

    @staticmethod
    def _handle_results(outqueue, get, cache, pool, timeout_seconds):
        thread = threading.current_thread()

        running_jobs = {}

        def _check_timeouts(running_jobs):
            log.debug("{0} Jobs running".format(
                len(running_jobs)))
            for job, (start_time, i, proc_num) in running_jobs.items():
                diff_time = (time.time() - start_time)
                if diff_time > timeout_seconds:
                    log.debug("Proc {0} timed out on job {1} in {2} seconds".format(
                        proc_num, job, diff_time))

                    for w in pool:
                        if w._proc_num == proc_num:
                            log.debug("Terminating worker {0}".format(w))
                            w.terminate()

                    print "Before delete", len(running_jobs)
                    del running_jobs[job]
                    print "After delete", len(running_jobs)
                    try:
                        cache[job]._set(i, (False, TimeoutError()))
                    except KeyError:
                        pass
                    

        while 1:
            try:
                task = get(True, 0.2)
            except (Queue.Empty):
                #log.debug("result handler received nothing during wait period")
                _check_timeouts(running_jobs)
                continue
            except (IOError, EOFError):
                log.debug('result handler got EOFError/IOError -- exiting')
                return

            if thread._state:
                assert thread._state == TERMINATE
                log.debug('result handler found thread._state=TERMINATE')
                break

            _check_timeouts(running_jobs)

            if task is None:
                log.debug('result handler got sentinel')
                break

            job, i, proc_num, obj = task
            if isinstance(obj, basestring) and obj == 'started':
                log.debug("worker started job {0}".format(job))

                running_jobs[job] = (time.time(), i, proc_num)
                continue

            if job not in running_jobs:
                log.debug("Worker is already done, ignoring result for job {0}".format(
                    job))
                continue


            del running_jobs[job]
            log.debug("Worker finished job {0}".format(job))

            try:
                cache[job]._set(i, obj)
            except KeyError:
                pass

        while cache and thread._state != TERMINATE:
            try:
                task = get()
            except (Queue.Empty):
                #log.debug("result handler received nothing during wait period")
                _check_timeouts(running_jobs)
                continue
            except (IOError, EOFError):
                log.debug('result handler got EOFError/IOError -- exiting')
                return

            _check_timeouts(running_jobs)

            if task is None:
                log.debug('result handler ignoring extra sentinel')
                continue

            job, i, proc_num, obj = task
            if isinstance(obj, basestring) and obj == 'started':
                log.debug("worker started job {0}".format(job))

                running_jobs[job] = (time.time(), i, proc_num)
                continue

            if job not in running_jobs:
                log.debug("Worker is already done, ignoring result for job {0}".format(
                    job))
                continue

            del running_jobs[job]
            log.debug("Worker finished job {0}".format(job))

            try:
                cache[job]._set(i, obj)
            except KeyError:
                pass

        if hasattr(outqueue, '_reader'):
            log.debug('ensuring that outqueue is not full')
            # If we don't make room available in outqueue then
            # attempts to add the sentinel (None) to outqueue may
            # block.  There is guaranteed to be no more than 2 sentinels.
            try:
                for i in range(10):
                    if not outqueue._reader.poll():
                        break
                    get()
            except (IOError, EOFError):
                pass

        log.debug('result handler exiting: len(cache)=%s, thread._state=%s', len(cache), thread._state)

    @staticmethod
    def _get_tasks(func, it, size):
        it = iter(it)
        while 1:
            x = tuple(itertools.islice(it, size))
            if not x:
                return
            yield (func, x)

    def __reduce__(self):
        raise NotImplementedError(
            'pool objects cannot be passed between processes or pickled'
        )

    def close(self):
        log.debug('closing pool')
        if self._state == RUN:
            self._state = CLOSE
            self._worker_handler._state = CLOSE

    def terminate(self):
        log.debug('terminating pool')
        self._state = TERMINATE
        self._worker_handler._state = TERMINATE
        self._terminate()

    def join(self):
        log.debug('joining pool')
        assert self._state in (CLOSE, TERMINATE)
        self._worker_handler.join()
        self._task_handler.join()
        self._result_handler.join()
        for p in self._pool:
            p.join()

    @staticmethod
    def _help_stuff_finish(inqueue, task_handler, size):
        # task_handler may be blocked trying to put items on inqueue
        log.debug('removing tasks from inqueue until task handler finished')
        inqueue._rlock.acquire()
        while task_handler.is_alive() and inqueue._reader.poll():
            inqueue._reader.recv()
            time.sleep(0)

    @classmethod
    def _terminate_pool(cls, taskqueue, inqueue, outqueue, pool,
                        worker_handler, task_handler, result_handler, cache):
        # this is guaranteed to only be called once
        log.debug('finalizing pool')

        worker_handler._state = TERMINATE
        task_handler._state = TERMINATE

        log.debug('helping task handler/workers to finish')
        cls._help_stuff_finish(inqueue, task_handler, len(pool))

        assert result_handler.is_alive() or len(cache) == 0

        result_handler._state = TERMINATE
        outqueue.put(None)                  # sentinel

        # We must wait for the worker handler to exit before terminating
        # workers because we don't want workers to be restarted behind our back.
        log.debug('joining worker handler')
        worker_handler.join()

        # Terminate workers which haven't already finished.
        if pool and hasattr(pool[0], 'terminate'):
            log.debug('terminating workers')
            for p in pool:
                if p.exitcode is None:
                    p.terminate()

        log.debug('joining task handler')
        task_handler.join(1e100)

        log.debug('joining result handler')
        result_handler.join(1e100)

        if pool and hasattr(pool[0], 'terminate'):
            log.debug('joining pool workers')
            for p in pool:
                if p.is_alive():
                    # worker has not yet exited
                    log.debug('cleaning up worker %d' % p.pid)
                    p.join()
