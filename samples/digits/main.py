# -*- coding: utf-8 -*-

import inspyred
import pyvotune
import pyvotune.sklearn
import random
import sys

from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline
import sklearn.datasets


def generator(random, args):
    gen = args['pyvotune_generator']

    genome = gen.generate(max_retries=50)

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
            return 0

        return test_individual(
            individual, args['test_X'], args['test_y'])
    except Exception as e:
        print "Exception:", e
        print candidate
        return 0


def train_candidate(candidate, train_X, train_y):
    if not candidate.assemble():
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
    pyvotune.set_debug(False)

    ############################
    # Load the initial dataset #
    ############################
    data = sklearn.datasets.load_digits()
    X = data['data']
    y = data['target']

    print X.shape

    # Split the dataset into training, testing and then validation parts
    train_X, temp_X, train_y, temp_y = train_test_split(X, y, test_size=0.25)
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
    ea = inspyred.ec.GA(random.Random())
    ea.terminator = [
        inspyred.ec.terminators.time_termination,
        #inspyred.ec.terminators.average_fitness_termination
    ]

    ea.observer = inspyred.ec.observers.stats_observer

    # Use PyvoTun variators
    ea.variator = [
        pyvotune.variators.param_reset_mutation,
        pyvotune.variators.scramble_mutation,
        pyvotune.variators.uniform_crossover
    ]

    # Go!
    final_pop = ea.evolve(
        generator=generator,
        evaluator=pyvotune.evaluators.parallel_evaluation_mp,
        pyvotune_generator=gen,

        mp_evaluator=evaluator,
        mp_ncpus=12,
        mp_timeout=60,
        mp_timeout_return=0,

        tolerance=0.25,
        max_time=300,

        train_X=train_X,
        train_y=train_y,
        test_X=test_X,
        test_y=test_y,

        pop_size=50,
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

