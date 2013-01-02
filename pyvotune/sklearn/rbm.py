# -*- coding: utf-8 -*-

import pyvotune

from pyvotune.feature_extractors import RBMFeatureExtractor


def get_rbm(n_features):
    pyvotune.dense_input(RBMFeatureExtractor)
    pyvotune.non_terminal(RBMFeatureExtractor)
    pyvotune.pfloat(range=(0., 1.0), name='learning_rate')(RBMFeatureExtractor)
    pyvotune.pint(range=(1, 10), name='training_epochs')(RBMFeatureExtractor)
    pyvotune.pint(range=(1, 1000), name='batch_size')(RBMFeatureExtractor)
    pyvotune.pint(range=(1, 1000), name='n_resamples')(RBMFeatureExtractor)
    pyvotune.pint(range=(5, 1500), name='n_hidden')(RBMFeatureExtractor)

    return [RBMFeatureExtractor]
