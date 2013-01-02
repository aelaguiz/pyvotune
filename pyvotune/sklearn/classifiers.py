# -*- coding: utf-8 -*-
import pyvotune
from sklearn.svm import SVC, NuSVC
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB


def get_classifiers(n_features, rng):
    pyvotune.dense_input(RandomForestClassifier)
    pyvotune.excl_terminal(RandomForestClassifier)
    pyvotune.choice(
        choices=['gini', 'entropy'], name='criterion', rng=rng)(RandomForestClassifier)
    pyvotune.pint(range=(1, 1000), name='n_estimators', rng=rng)(RandomForestClassifier)
    pyvotune.pfloat(range=(0, 1), name='min_density', rng=rng)(RandomForestClassifier)
    pyvotune.pconst(value=1, name='n_jobs', rng=rng)(RandomForestClassifier)
    pyvotune.pbool(name='bootstrap', rng=rng)(RandomForestClassifier)
    pyvotune.pbool(name='oob_score', rng=rng)(RandomForestClassifier)

    pyvotune.dense_input(ExtraTreesClassifier)
    pyvotune.excl_terminal(ExtraTreesClassifier)
    pyvotune.choice(
        choices=['gini', 'entropy'], name='criterion', rng=rng)(ExtraTreesClassifier)
    pyvotune.pint(range=(1, 1000), name='n_estimators', rng=rng)(ExtraTreesClassifier)
    pyvotune.pfloat(range=(0, 1), name='min_density', rng=rng)(ExtraTreesClassifier)
    pyvotune.pconst(value=1, name='n_jobs', rng=rng)(ExtraTreesClassifier)
    pyvotune.pbool(name='bootstrap', rng=rng)(ExtraTreesClassifier)
    pyvotune.pbool(name='oob_score', rng=rng)(ExtraTreesClassifier)

    pyvotune.dense_input(GradientBoostingClassifier)
    pyvotune.excl_terminal(GradientBoostingClassifier)
    pyvotune.pint(range=(10, 1000), name='n_estimators', rng=rng)(GradientBoostingClassifier)
    pyvotune.pint(range=(1, n_features), name='max_features', rng=rng)(GradientBoostingClassifier)
    pyvotune.pfloat(range=(0, 1), name='learn_rate', rng=rng)(GradientBoostingClassifier)
    pyvotune.pfloat(range=(0, 1), name='subsample', rng=rng)(GradientBoostingClassifier)

    pyvotune.dense_input(GaussianNB)
    pyvotune.excl_terminal(GaussianNB)

    pyvotune.dense_input(MultinomialNB)
    pyvotune.pfloat(range=(0, 1), name='alpha', rng=rng)(MultinomialNB)
    pyvotune.pbool(name='fit_prior', rng=rng)(MultinomialNB)
    pyvotune.excl_terminal(MultinomialNB)

    pyvotune.dense_input(KNeighborsClassifier)
    pyvotune.excl_terminal(KNeighborsClassifier)
    pyvotune.pint(range=(2, 100), name='n_neighbors', rng=rng)(KNeighborsClassifier)
    pyvotune.choice(
        choices=['uniform', 'distance'], name='weights', rng=rng)(KNeighborsClassifier)
    pyvotune.choice(
        choices=[
            'auto', 'ball_tree', 'kd_tree', 'brute'], name='algorithm', rng=rng)(
                KNeighborsClassifier)
    pyvotune.pint(range=(10, 100), name='leaf_size', rng=rng)(KNeighborsClassifier)
    pyvotune.pint(range=(1, 20), name='p', rng=rng)(KNeighborsClassifier)

    pyvotune.excl_terminal(SVC)
    pyvotune.pfloat(range=(0, 1000), name='C', rng=rng)(SVC)
    pyvotune.choice(choices=['linear', 'poly', 'rbf', 'sigmoid'], name='kernel', rng=rng)(SVC)
    pyvotune.pint(range=(0, 10), name='degree', rng=rng)(SVC)
    pyvotune.pfloat(range=(0, 100.), name='gamma', rng=rng)(SVC)
    pyvotune.pfloat(range=(-10000, 10000.), name='coef0', rng=rng)(SVC)
    pyvotune.pbool(name='shrinking', rng=rng)(SVC)

    pyvotune.excl_terminal(NuSVC)
    pyvotune.pfloat(range=(0, 1.), name='nu', rng=rng)(NuSVC)
    pyvotune.choice(choices=['poly', 'rbf', 'sigmoid'], name='kernel', rng=rng)(NuSVC)
    pyvotune.pint(range=(0, 10), name='degree', rng=rng)(NuSVC)
    pyvotune.pfloat(range=(0, 100.), name='gamma', rng=rng)(NuSVC)
    pyvotune.pfloat(range=(-10000, 10000.), name='coef0', rng=rng)(NuSVC)
    pyvotune.pbool(name='shrinking', rng=rng)(NuSVC)

    return [SVC, NuSVC, GaussianNB, RandomForestClassifier, MultinomialNB,
            KNeighborsClassifier, ExtraTreesClassifier,
            GradientBoostingClassifier]
