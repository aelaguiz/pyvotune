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

from pyvotune.theano import dataset, RBM


from pyvotune.log import logger
log = logger()


global_theano = None
global_T = None
global_RandomStreams = None


class PyRBMFeatureExtractor(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        learning_rate=0.1, training_epochs=15,
            batch_size=20, n_resamples=10,
            n_hidden=500):

        self.learning_rate = learning_rate
        self.training_epochs = training_epochs
        self.batch_size = batch_size
        self.n_hidden = n_hidden
        self.n_resamples = n_resamples

        super(PyRBMFeatureExtractor, self).__init__()

    def fit(self, X, y=None):
        global global_theano
        global global_T
        global global_RandomStreams

        log.debug(u"RBM Fitting with lr={0} epochs={1} n_hidden={2}".format(
            self.learning_rate, self.training_epochs, self.n_hidden))

        ## This prevents us from multiple importing theano which is important
        ## since it performs some global initialization, especially for cuda
        if not global_theano:
            log.debug(u"Importing Py")
            import theano
            import theano.tensor as T
            from theano.tensor.shared_randomstreams import RandomStreams
            theano.config.warn.subtensor_merge_bug = False

            global_theano = theano
            global_T = T
            global_RandomStreams = RandomStreams

        self.rng = np.random.RandomState(123456)
        self.theano_rng = global_RandomStreams(self.rng.randint(2 ** 30))

        self.n_visible = np.shape(X)[1]

        #log.debug(u"RBM Featureset has {0} visible nodes".format(
            #self.n_visible))

        train_x, train_y = dataset.shared_dataset(global_theano, global_T, X, y, borrow=True)

        self.init_objects(train_x)

        self.train(train_x)

        return self

    def train(self, train_x):
        n_train_batches = train_x.get_value(borrow=True).shape[0] / self.batch_size

        #log.debug(
            #u"Fitting RBM With {0} training batches".format(n_train_batches))

        for epoch in xrange(self.training_epochs):

            # go through the training set
            mean_cost = []
            t_start = time.time()

            #log.debug(u"RBM Training epoch {0}".format(epoch))

            for batch_index in xrange(n_train_batches):
                t_batch_start = time.time()
                mean_cost += [self.train_rbm(batch_index)]
                t_batch_end = time.time()

                #log.debug(u"Training batch {0} of {1} - took {2}s".format(
                    #batch_index, n_train_batches, t_batch_end - t_batch_start))

            t_end = time.time()
            #log.debug(u'Training epoch {0}, cost is {1} - took {2}s'.format(
                #epoch, np.mean(mean_cost), t_end - t_start))

    def transform(self, X, y=None):
        test_set_x, _ = dataset.shared_dataset(global_theano, global_T, X, borrow=True)

        # pick random test examples, with which to initialize the persistent chain
        persistent_vis_chain = global_theano.shared(np.asarray(test_set_x.get_value(borrow=True), dtype=global_theano.config.floatX))

        [presig_hids, hid_mfs, hid_samples, presig_vis,
         vis_mfs, vis_samples], updates =  \
            global_theano.scan(
                self.rbm.gibbs_vhv,
                outputs_info=[None, None, None, None, None, persistent_vis_chain],
                n_steps=1)

        # add to updates the shared variable that takes care of our persistent
        # chain :.
        #updates.update({persistent_vis_chain: vis_samples[-1]})

        # construct the function that implements our persistent chain.
        # we generate the "mean field" activations for plotting and the actual
        # samples for reinitializing the state of our persistent chain
        sample_fn = global_theano.function(
            [], [hid_mfs[-1], hid_samples[-1], vis_mfs[-1], vis_samples[-1]],
            name='sample_fn')

        ident = random.randint(0, 500)

        all_hid_mfs = []
        all_vis_sample = []
        all_hid_sample = []
        for i in range(self.n_resamples):
            hid_mfs, hid_sample, vis_mfs, vis_sample = sample_fn()

            all_hid_mfs.append(hid_mfs)
            all_hid_sample.append(hid_sample)
            all_vis_sample.append(vis_sample)

        hidden_mean_field = np.mean(all_hid_mfs, axis=0)

        print "all_hid_mfs shape", np.shape(all_hid_mfs)
        print "Hidden mean field", np.shape(hidden_mean_field)
        print "Shapes", np.shape(hidden_mean_field), np.shape(all_hid_mfs)

        #self.sample_all(X, all_hid_sample, all_vis_sample, ident)

        return hidden_mean_field

    #def sample_all(self, X, all_hid_sample, all_vis_sample, ident):
        #width = np.shape(X)[1]
        #sq = math.sqrt(width)

        #if width != sq ** 2:
            #return

        #hid_sample_mean_field = np.mean(all_hid_sample, axis=0)
        #vis_sample_mean_field = np.mean(all_vis_sample, axis=0)

        #all_recons = []

        #n_padding = (width - self.n_hidden) / 2

        #padding = np.zeros((n_padding, ))

        #for sample, recons, hidden in zip(X, vis_sample_mean_field, hid_sample_mean_field)[:10]:

            #padded_hidden = np.hstack((padding, hidden, padding))

            #comb = np.hstack((
                #sample.reshape(50, 50), recons.reshape(50, 50),
                #padded_hidden.reshape(50, 50)))

            #comb = np.flipud(comb)

            #all_recons.append(comb)

        #np_to_pil(
            #np.vstack(all_recons), colorize=True,
            #filename='samples/%i_samp_reconstruction_%i_%ires.png' % (
                #ident, len(X), self.n_resamples))

    def init_objects(self, train_x):
        # allocate symbolic variables for the data
        self.index = global_T.lscalar()    # index to a [mini]batch
        self.x = global_T.matrix('x')  # the data is presented as rasterized images

        # initialize storage for the persistent chain (state = hidden
        # layer of chain)
        self.persistent_chain = global_theano.shared(
            np.zeros(
                (self.batch_size, self.n_hidden),
                dtype=global_theano.config.floatX),
            borrow=True)

        # construct the RBM class
        self.rbm = RBM(
            global_theano, global_T,
            input=self.x, n_visible=self.n_visible,

            n_hidden=self.n_hidden, np_rng=self.rng, theano_rng=self.theano_rng)

        # get the cost and the gradient corresponding to one step of CD-15
        self.cost, self.updates = self.rbm.get_cost_updates(
            lr=self.learning_rate, persistent=self.persistent_chain, k=15)

        # it is ok for a theano function to have no output
        # the purpose of train_rbm is solely to update the RBM parameters
        self.train_rbm = global_theano.function(
            [self.index], self.cost,
            updates=self.updates,
            givens={self.x: train_x[self.index * self.batch_size: (self.index + 1) * self.batch_size]},
            name='train_rbm')

