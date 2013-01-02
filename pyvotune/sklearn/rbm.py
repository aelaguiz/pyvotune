# -*- coding: utf-8 -*-

import pyvotune

from pyvotune.feature_extractors import PyRBMFeatureExtractor
from pyvotune.feature_extractors import TheanoRBMFeatureExtractor


def get_pyrbm(n_features, rng):
    print "Called get pyrbm"
    pyvotune.dense_input(PyRBMFeatureExtractor)
    pyvotune.non_terminal(PyRBMFeatureExtractor)
    pyvotune.pfloat(range=(0., 1.0), name='learning_rate', rng=rng)(PyRBMFeatureExtractor)
    pyvotune.pfloat(range=(0., 1.0), name='momentum', rng=rng)(PyRBMFeatureExtractor)
    pyvotune.pfloat(range=(0., 1.0), name='l2_weight', rng=rng)(PyRBMFeatureExtractor)
    pyvotune.pfloat(range=(0., 1.0), name='sparsity', rng=rng)(PyRBMFeatureExtractor)
    pyvotune.pfloat(range=(0., 1.0), name='scale', rng=rng)(PyRBMFeatureExtractor)
    pyvotune.pbool(name='binary', rng=rng)(PyRBMFeatureExtractor)
    pyvotune.pint(range=(1, 10), name='n_training_epochs', rng=rng)(PyRBMFeatureExtractor)
    pyvotune.pint(range=(1, 1000), name='batch_size', rng=rng)(PyRBMFeatureExtractor)
    pyvotune.pint(range=(5, 1500), name='n_hidden', rng=rng)(PyRBMFeatureExtractor)

    return [PyRBMFeatureExtractor]


def get_theano(n_features, rng):
    pyvotune.dense_input(TheanoRBMFeatureExtractor)
    pyvotune.non_terminal(TheanoRBMFeatureExtractor)
    pyvotune.pfloat(range=(0., 1.0), name='learning_rate', rng=rng)(TheanoRBMFeatureExtractor)
    pyvotune.pint(range=(1, 10), name='training_epochs', rng=rng)(TheanoRBMFeatureExtractor)
    pyvotune.pint(range=(1, 1000), name='batch_size', rng=rng)(TheanoRBMFeatureExtractor)
    pyvotune.pint(range=(1, 1000), name='n_resamples', rng=rng)(TheanoRBMFeatureExtractor)
    pyvotune.pint(range=(5, 1500), name='n_hidden', rng=rng)(TheanoRBMFeatureExtractor)

    return [TheanoRBMFeatureExtractor]
