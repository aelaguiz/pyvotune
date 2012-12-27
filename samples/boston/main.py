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
            return sys.maxint

        return test_individual(
            individual, args['test_X'], args['test_y'])
    except Exception as e:
        print "Exception:", e
        print candidate
        return sys.maxint


def train_candidate(candidate, train_X, train_y):
    if not candidate.assemble():
        return

    pipeline = Pipeline([
        (str(i), s) for i, s in enumerate(candidate.assembled)])

    pipeline.fit(train_X, train_y)

    return pipeline


def test_individual(pipeline, test_X, test_y, display=False):
    observed_y = pipeline.predict(test_X)

    mse = sklearn.metrics.mean_squared_error(
        test_y, observed_y)

    if display:
        total_err = 0
        total_actual = 0
        print "  #", "Actual", "Observed", "Err %"
        print "---", "------", "--------", "-----"
        for i, (actual, observed) in enumerate(
                random.sample(zip(test_y, observed_y), 10)):
            err = abs(observed - actual)
            err_pct = round(err / actual * 100., 2)

            total_err += err
            total_actual += actual

            print str(i).zfill(3), str(actual).ljust(6), str(observed).ljust(8), str(err_pct).ljust(4)
        print "MSE:", mse
        print "Avg Err %:", round(total_err / total_actual * 100., 2)

    return mse


if __name__ == '__main__':
    pyvotune.set_debug(False)

    data = sklearn.datasets.load_boston()
    X = data['data']
    y = data['target']

    train_X, temp_X, train_y, temp_y = train_test_split(X, y, test_size=0.25)
    test_X, validate_X, test_y, validate_y = train_test_split(
        temp_X, temp_y, test_size=0.5)

    print "Total dataset", len(X)
    print "Training on", len(train_X)
    print "Testing on", len(test_X)
    print "Validating on", len(validate_X)

    n_features = X.shape[1]
    gen = pyvotune.Generate(
        initial_state={
            'sparse': False
        },
        gene_pool=pyvotune.sklearn.get_regressors(n_features) + pyvotune.sklearn.get_decomposers(n_features),
        max_length=4,
        noop_frequency=0.2)

    ea = inspyred.ec.GA(random.Random())
    ea.terminator = [
        inspyred.ec.terminators.time_termination,
        inspyred.ec.terminators.average_fitness_termination
    ]

    ea.observer = inspyred.ec.observers.stats_observer

    ea.variator = [
        pyvotune.variators.param_reset_mutation,
        pyvotune.variators.scramble_mutation,
        pyvotune.variators.uniform_crossover
    ]

    final_pop = ea.evolve(
        generator=generator,
        evaluator=inspyred.ec.evaluators.parallel_evaluation_mp,
        pyvotune_generator=gen,

        mp_evaluator=evaluator,
        mp_nprocs=12,

        tolerance=0.25,
        max_time=300,

        train_X=train_X,
        train_y=train_y,
        test_X=test_X,
        test_y=test_y,

        pop_size=100,
        maximize=False,
        num_elites=5)

    best = max(final_pop)

    pipeline = train_candidate(best.candidate, train_X, train_y)
    test_individual(pipeline, validate_X, validate_y, display=True)
    print best.candidate
