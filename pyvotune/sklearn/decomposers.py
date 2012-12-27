# -*- coding: utf-8 -*-

import pyvotune
from sklearn.decomposition import PCA, ProbabilisticPCA, ProjectedGradientNMF


def get_decomposers(n_features):
    pyvotune.dense_input(PCA)
    pyvotune.non_terminal(PCA)
    pyvotune.pbool(name='whiten')(PCA)

    pyvotune.non_terminal(ProjectedGradientNMF)
    pyvotune.pint(
        range=(1, n_features), name='n_components')(ProjectedGradientNMF)
    pyvotune.choice(
        choices=['nndsvd', 'nndsvda', 'nndsvdar'],
        name='init')(ProjectedGradientNMF)
    pyvotune.choice(
        choices=['data', 'components', None],
        name='sparseness')(ProjectedGradientNMF)
    pyvotune.pfloat(
        range=(1, 10), name='beta')(ProjectedGradientNMF)
    pyvotune.pfloat(
        range=(0.01, 10), name='eta')(ProjectedGradientNMF)
    pyvotune.pint(
        range=(1, 600), name='max_iter')(ProjectedGradientNMF)
    pyvotune.pint(
        range=(100, 4000), name='nls_max_iter')(ProjectedGradientNMF)

    # PCA & ProbabilisticPCA are initialized together since ProbabilisticPCA
    # wraps PCA
    return [PCA, ProbabilisticPCA, ProjectedGradientNMF]
