# -*- coding: utf-8 -*-

import inspyred
import inspyred.ec.cea_parallel_evaluator
import pyvotune
import pyvotune.sklearn
import random
import sys
import redis

try:
    import cPickle as pickle
except ImportError:
    import pickle

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
            print "Exception:", e, candidate.genome_id
            #print candidate
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

    #############################
    ## Load the initial dataset #
    #############################
    X, y = load_mnist()

    print "Dataset loaded"

    print X.shape
    print y.shape

    # Split the dataset into training, testing and then validation parts
    train_X, temp_X, train_y, temp_y = train_test_split(X, y, test_size=0.25)

    print "Split"
    test_X, validate_X, test_y, validate_y = train_test_split(
        temp_X, temp_y, test_size=0.5)

    f = open(sys.argv[1], "rb")
    archive = pickle.load(f)
    f.close()

    for ind in archive:
        genome = ind.candidate

        print "-----------------------------------------------"
        print genome
        pipeline = train_candidate(ind.candidate, train_X, train_y)

        print "Testing dataset:"
        test_individual(pipeline, test_X, test_y, display=True)

        print "Validation dataset:"
        test_individual(pipeline, validate_X, validate_y, display=True)

        print "Fitness:", ind.fitness
        print ind.candidate
