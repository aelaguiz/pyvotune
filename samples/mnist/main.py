# -*- coding: utf-8 -*-

import inspyred
import inspyred.ec.cea_parallel_evaluator
import pyvotune
import pyvotune.sklearn
import random
import sys
import redis
import time

from sklearn.cross_validation import StratifiedKFold
from sklearn.pipeline import Pipeline
import sklearn.datasets
import multiprocessing

from loader import load_mnist

log = pyvotune.log.logger()

############################
# Load the initial dataset #
############################
X, y = load_mnist()


def generator(random, args):
    gen = args['pyvotune_generator']

    genome = gen.generate(max_retries=150)

    if not genome:
        print "ERROR: Failed to generate a genome after 50 tries"
        sys.exit(0)

    return genome


@inspyred.ec.evaluators.evaluator
def evaluator(candidate, args):
    return _evaluator(candidate)


def _evaluator(candidate, display=False):
    try:
        if not candidate.assemble():
            print "Candidate failed to assemble", candidate
            return 0.

        pipeline = Pipeline([
            (str(i), s) for i, s in enumerate(candidate.assembled)])

        skf = StratifiedKFold(y, 3, indices=False)

        start_time = time.time()
        scores = []
        for train_index, test_index in skf:
            train_X, test_X = X[train_index], X[test_index]
            train_y, test_y = y[train_index], y[test_index]

            pipeline.fit(train_X, train_y)
            observed_y = pipeline.predict(test_X)

            f1 = sklearn.metrics.f1_score(test_y, observed_y)

            scores.append(f1)

            if display:
                print sklearn.metrics.classification_report(test_y, observed_y)

        avg_f1 = sum(scores) / float(len(scores)) * 100.

        total_time = time.time() - start_time

        print "Train/test time", total_time

        return avg_f1
    except Exception as e:
        print "Exception:", e, candidate.genome_id
        #print candidate

        return 0.


if __name__ == '__main__':
    pyvotune.set_debug(True)

    n_features = X.shape[1]

    #################################
    # Initialize PyvoTune Generator #
    #################################
    gen = pyvotune.Generate(
        initial_state={
            'sparse': False
        },
        gene_pool=pyvotune.sklearn.get_classifiers(n_features) +
        pyvotune.sklearn.get_decomposers(n_features) +
        pyvotune.sklearn.get_image_features(n_features) +
        pyvotune.sklearn.get_preprocessors(n_features),
        max_length=4,
        noop_frequency=0.2)

    ####################################
    # Initialize Inspyred Genetic Algo #
    ####################################
    ea = inspyred.ec.cEA(random.Random())
    ea.logger = log
    ea.terminator = [
        #inspyred.ec.terminators.time_termination,
        inspyred.ec.terminators.average_fitness_termination
    ]
    ea.selector = inspyred.ec.selectors.fitness_proportionate_selection

    ea.archiver = pyvotune.archivers.pickle_wrap_archiver

    ea.observer = pyvotune.observers.stats_observer

    # Use PyvoTun variators
    ea.variator = [
        pyvotune.variators.random_reset_mutation,
        pyvotune.variators.param_reset_mutation,
        pyvotune.variators.scramble_mutation,
        pyvotune.variators.uniform_crossover,
        pyvotune.variators.n_point_crossover
    ]


    nprocs = int(multiprocessing.cpu_count() * 2)
    #nprocs = 4

    con_str = "redis://localhost:6379/3"

    # Start redis queue workers
    pyvotune.evaluators.cea_rq_worker.start_workers(processes=nprocs, con_str=con_str)

    # Go!
    final_pop = ea.evolve(
        neighborhood=inspyred.ec.neighborhoods.grid_neighborhood,

        generator=generator,
        evaluator=pyvotune.evaluators.cell_evaluator_rq,
        pyvotune_generator=gen,

        async_evaluator=True,

        rq_constr=con_str,
        rq_evaluator=evaluator,
        rq_timeout=300,
        rq_timeout_fitness=0,

        crossover_rate=0.5,

        mutation_rate=0.3,

        tolerance=0.01,
        #max_time=300,
        
        underlying_archiver=inspyred.ec.archivers.best_archiver,
        archive_path='./archive.pkl',

        nbh_grid_size=50,
        nbh_size=2,
        num_selected=2,

        maximize=True,
        num_elites=5)

    ####################
    # Display Solution #
    ####################
    best = max(final_pop)
    fitness = _evaluator(best.candidate, display=True)
    print "Fitness:", fitness
    print best.candidate
