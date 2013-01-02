# -*- coding: utf-8 -*-

from collections import Mapping, Sequence
from operator import itemgetter

import math
import time
import numpy as np
import scipy.sparse as sp


import random

from sklearn.preprocessing import normalize
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import atleast2d_or_csr

from pyvotune.pyrbm.rbm import RBM, Trainer


from pyvotune.log import logger
log = logger()


global_theano = None
global_T = None
global_RandomStreams = None


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


class PyRBMFeatureExtractor(BaseEstimator, TransformerMixin):
    def __init__(
        self,
            n_hidden=500, binary=True,
            learning_rate=0.1, momentum=0.2,
            l2_weight=0.001, sparsity=0.1,
            n_training_epochs=10,
            scale=0.001,
            batch_size=20):

        self.n_hidden = n_hidden
        self.binary = binary
        self.momentum = momentum
        self.learning_rate = learning_rate
        self.l2_weight = l2_weight
        self.sparsity = sparsity
        self.batch_size = batch_size
        self.scale = scale
        self.n_training_epochs = n_training_epochs


        super(PyRBMFeatureExtractor, self).__init__()

    def fit(self, X, y=None):
        n_features = X.shape[1]

        self.rbm = RBM(
            n_features, self.n_hidden, self.binary, self.scale)

        trainer = Trainer(
            self.rbm, l2=self.l2_weight, momentum=self.momentum,
            target_sparsity=self.sparsity)

        for i in range(self.n_training_epochs):
            for j, batch in enumerate(chunks(X, self.batch_size)):
                #log.debug("Training rbm on epoch %s batch %s" % (i, j))
                trainer.learn(batch, learning_rate=self.learning_rate)

        return self

    def transform(self, X, y=None):
        out = self.rbm.hidden_expectation(X)

        #log.debug("Result on rbm {0}".format(out))


        return out
