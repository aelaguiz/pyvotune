# -*- coding: utf-8 -*-

import sys
import inspyred
import time

import sklearn
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import StratifiedKFold

import pyvotune

from loader import load_mnist

log = pyvotune.log.logger()

global X
global y

X = None
y = None


def load_dataset(num_samples):
    global X
    global y

    ############################
    # Load the initial dataset #
    ############################
    X, y = load_mnist(num_samples)


def get_num_features():
    return X.shape[1]


def get_gene_pool():
    n_features = get_num_features()

    gene_pool = pyvotune.sklearn.get_classifiers(n_features) +\
        pyvotune.sklearn.get_decomposers(n_features) +\
        pyvotune.sklearn.get_image_features(n_features) +\
        pyvotune.sklearn.get_preprocessors(n_features)

    return gene_pool


def generator(random, args):
    gen = args['pyvotune_generator']

    genome = gen.generate(max_retries=150)

    if not genome:
        log.error("ERROR: Failed to generate a genome after 50 tries")
        sys.exit(0)

    return genome


@inspyred.ec.evaluators.evaluator
def evaluator(candidate, args):
    return _evaluator(candidate)


def _evaluator(candidate, display=False):
    try:
        if not candidate.assemble():
            log.error("Candidate failed to assemble: %s" % candidate)
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
                log.info(
                    "\n%s" % sklearn.metrics.classification_report(test_y, observed_y))

        avg_f1 = sum(scores) / float(len(scores)) * 100.

        total_time = time.time() - start_time

        log.debug("Train/test time: %s" % total_time)

        return avg_f1
    except Exception as e:
        log.exception("Exception: %s %s" % (e, candidate.genome_id))

        return 0.
