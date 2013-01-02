# -*- coding: utf-8 -*-

import sys
import inspyred
import time

import sklearn
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import StratifiedKFold

import pyvotune

try:
    import cPickle as pickle
except ImportError:
    import pickle

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


def get_gene_pool(rng):
    n_features = get_num_features()

    gene_pool = pyvotune.sklearn.get_classifiers(n_features, rng) +\
        pyvotune.sklearn.get_preprocessors(n_features, rng) + \
        pyvotune.sklearn.get_decomposers(n_features, rng) +\
        pyvotune.sklearn.get_image_features(n_features, rng) +\
        pyvotune.sklearn.get_pyrbm(n_features, rng)

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
    start_time = time.time()

    try:
        if not candidate.assemble():
            log.error("Candidate failed to assemble: %s" % candidate)
            return 0.

        pipeline = Pipeline([
            (str(i), s) for i, s in enumerate(candidate.assembled)])

        log.debug("Evaluating %s fitness" % (candidate.genome_id))

        skf_start = time.time()

        skf = StratifiedKFold(y, 3, indices=False)

        scores = []
        fold = 1
        for train_index, test_index in skf:
            skf_end = time.time()
            mask_start = time.time()

            train_X, test_X = X[train_index], X[test_index]
            train_y, test_y = y[train_index], y[test_index]

            log.debug("Genome %s Fold %d Training on %s samples (%s skf, %s masking)" % (
                candidate.genome_id, fold, len(train_X),
                (skf_end - skf_start),
                (time.time() - mask_start)))

            pipeline.fit(train_X, train_y)
            observed_y = pipeline.predict(test_X)

            log.debug("Genome %s Fold %d Testing on %s samples" % (
                candidate.genome_id, fold, len(test_X)))

            f1 = sklearn.metrics.f1_score(test_y, observed_y)

            scores.append(f1)

            if f1 > 0 or display:
                log.debug(candidate)
                log.info(
                    "\n%s" % sklearn.metrics.classification_report(test_y, observed_y))

            fold += 1

        avg_f1 = sum(scores) / float(len(scores)) * 100.

        total_time = time.time() - start_time

        log.debug("Evaluated %s Fitness %s in %ss" % (
            candidate.genome_id, avg_f1, total_time))

        return avg_f1
    except Exception as e:
        log.debug(
            "Error evaluating genome %s\nFailed after %s seconds" % (
                candidate.genome_id, time.time() - start_time), exc_info=True)

        return 0.


def validate_models(model_path):
    f = open(model_path, "rb")
    models = pickle.load(f)
    f.close()

    for model in models:
        log.info("Testing model: %s" % model.candidate)

        _evaluator(model.candidate, display=False)
