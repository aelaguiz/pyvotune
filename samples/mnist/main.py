# -*- coding: utf-8 -*-

import inspyred
import inspyred.ec.cea_parallel_evaluator
import pyvotune
import pyvotune.sklearn
import random
import sys
import redis

from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline
import sklearn.datasets
import multiprocessing

from loader import load_mnist

log = pyvotune.log.logger()


def generator(random, args):
    gen = args['pyvotune_generator']

    genome = gen.generate(max_retries=150)

    if not genome:
        print "ERROR: Failed to generate a genome after 50 tries"
        sys.exit(0)

    return genome


@inspyred.ec.evaluators.evaluator
def evaluator(candidate, args):
    try:
        individual = train_candidate(
            candidate, args['train_X'], args['train_y'])

        if not individual:
            print "Failed to train", candidate
            return 0.

        return test_individual(
            individual, args['test_X'], args['test_y'])
    except Exception as e:
        try:
            print "Exception:", e
            print candidate
        except Exception as e:
            print "Exception in exception handler!!!"
            print e

        return 0.


def train_candidate(candidate, train_X, train_y):
    if not candidate.assemble():
        print "Candidate failed to assemble", candidate
        return

    pipeline = Pipeline([
        (str(i), s) for i, s in enumerate(candidate.assembled)])

    pipeline.fit(train_X, train_y)

    return pipeline


def test_individual(pipeline, test_X, test_y, display=False):
    observed_y = pipeline.predict(test_X)

    f1 = sklearn.metrics.f1_score(test_y, observed_y)

    if display:
        print sklearn.metrics.classification_report(test_y, observed_y)

    return round(f1 * 100., 2)


if __name__ == '__main__':
    pyvotune.set_debug(True)

    ############################
    # Load the initial dataset #
    ############################
    X, y = load_mnist()

    print "Dataset loaded"

    print X.shape
    print y.shape

    # Split the dataset into training, testing and then validation parts
    train_X, temp_X, train_y, temp_y = train_test_split(X, y, test_size=0.25)

    print "Split"
    test_X, validate_X, test_y, validate_y = train_test_split(
        temp_X, temp_y, test_size=0.5)

    print "Training", train_X.shape
    print "Testing", test_X.shape
    print "Validation", validate_X.shape

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

    ea.observer = pyvotune.observers.stats_observer

    # Use PyvoTun variators
    ea.variator = [
        pyvotune.variators.random_reset_mutation,
        pyvotune.variators.param_reset_mutation,
        pyvotune.variators.scramble_mutation,
        pyvotune.variators.uniform_crossover,
        pyvotune.variators.n_point_crossover
    ]


    nprocs = int(multiprocessing.cpu_count() * 1.5)
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
        #mp_ncpus=12,
        rq_timeout=30,
        rq_timeout_fitness=0,

        crossover_rate=0.3,
        mutation_rate=0.2,

        tolerance=0.01,
        #max_time=300,

        train_X=train_X,
        train_y=train_y,
        test_X=test_X,
        test_y=test_y,

        nbh_grid_size=28,
        nbh_size=3,
        num_selected=3,

        maximize=True,
        num_elites=5)

    ####################
    # Display Solution #
    ####################
    best = max(final_pop)
    pipeline = train_candidate(best.candidate, train_X, train_y)
    test_individual(pipeline, validate_X, validate_y, display=True)
    print "Fitness:", best.fitness
    print best.candidate


