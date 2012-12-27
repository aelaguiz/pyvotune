# -*- coding: utf-8 -*-

import pyvotune
from sklearn.preprocessing import Scaler, Normalizer, Binarizer


def get_preprocessors(n_features):
    pyvotune.dense_input(Scaler)
    pyvotune.non_terminal(Scaler)
    pyvotune.pbool(name='with_std')(Scaler)

    pyvotune.non_terminal(Normalizer)
    pyvotune.choice(choices=['l1', 'l2'], name='norm')(Normalizer)

    pyvotune.non_terminal(Binarizer)
    pyvotune.pfloat(range=(0, 10000), name='threshold')(Binarizer)

    return [Scaler, Normalizer, Binarizer]
