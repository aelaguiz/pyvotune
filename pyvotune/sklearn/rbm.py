# -*- coding: utf-8 -*-

import pyvotune

from pyvotune.feature_extractors import RBMFeatureExtractor


def get_rbm(n_features, rng):
    pyvotune.dense_input(RBMFeatureExtractor)
    pyvotune.non_terminal(RBMFeatureExtractor)
    pyvotune.pfloat(range=(0., 1.0), name='learning_rate', rng=rng)(RBMFeatureExtractor)
    pyvotune.pint(range=(1, 10), name='training_epochs', rng=rng)(RBMFeatureExtractor)
    pyvotune.pint(range=(1, 1000), name='batch_size', rng=rng)(RBMFeatureExtractor)
    pyvotune.pint(range=(1, 1000), name='n_resamples', rng=rng)(RBMFeatureExtractor)
    pyvotune.pint(range=(5, 1500), name='n_hidden', rng=rng)(RBMFeatureExtractor)

    return [RBMFeatureExtractor]