# -*- coding: utf-8 -*-

import pyvotune

from pyvotune.feature_extractors import RBMFeatureExtractor

        #learning_rate=0.1, training_epochs=15,
            #batch_size=20, n_resamples=10,
            #n_hidden=500):


def get_rbm(n_features):
    pyvotune.dense_input(RBMFeatureExtractor)
    pyvotune.non_terminal(RBMFeatureExtractor)
    pyvotune.pfloat(range=(0., 1.0), name='learning_rate')(RBMFeatureExtractor)
    pyvotune.pint(range=(1, 10), name='training_epochs')(RBMFeatureExtractor)
    pyvotune.pint(range=(1, 1000), name='batch_size')(RBMFeatureExtractor)
    pyvotune.pint(range=(1, 1000), name='n_resamples')(RBMFeatureExtractor)
    pyvotune.pint(range=(5, 1500), name='n_hidden')(RBMFeatureExtractor)

    return [RBMFeatureExtractor]
