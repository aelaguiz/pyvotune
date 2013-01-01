# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp

from sklearn.preprocessing import normalize

from pyvotune.log import logger
log = logger()


def shared_dataset(theano, T, X, y=None, borrow=True):
    """
    Loads a sklearn style np dataset into theano
    shared variables to allow for GPU computation
    """

    max_val = np.max(X)

    data_x = np.asarray(X, dtype=theano.config.floatX)

    shared_x = theano.shared(data_x,
                             borrow=borrow)

    _y = None

    if y is not None:
        data_y = np.asarray(y, dtype=theano.config.floatX)
        shared_y = theano.shared(data_y,
                                 borrow=borrow)
        _y = T.cast(shared_y, 'int32')

    # When storing data on the GPU it has to be stored as floats
    # therefore we will store the labels as ``floatX`` as well
    # (``shared_y`` does exactly that). But during our computations
    # we need them as ints (we use labels as index, and if they are
    # floats it doesn't make sense) therefore instead of returning
    # ``shared_y`` we will have to cast it to int. This little hack
    # lets ous get around this issue
    return shared_x, _y
