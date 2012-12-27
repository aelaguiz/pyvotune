# -*- coding: utf-8 -*-
import pyvotune
from sklearn.svm import SVC, NuSVC
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB


def get_classifiers(n_features):
    pyvotune.dense_input(RandomForestClassifier)
    pyvotune.excl_terminal(RandomForestClassifier)
    pyvotune.choice(
        choices=['gini', 'entropy'], name='criterion')(RandomForestClassifier)
    pyvotune.pint(range=(1, 1000), name='n_estimators')(RandomForestClassifier)
    pyvotune.pfloat(range=(0, 1), name='min_density')(RandomForestClassifier)
    pyvotune.pconst(value=1, name='n_jobs')(RandomForestClassifier)
    pyvotune.pbool(name='bootstrap')(RandomForestClassifier)
    pyvotune.pbool(name='oob_score')(RandomForestClassifier)

    pyvotune.dense_input(ExtraTreesClassifier)
    pyvotune.excl_terminal(ExtraTreesClassifier)
    pyvotune.choice(
        choices=['gini', 'entropy'], name='criterion')(ExtraTreesClassifier)
    pyvotune.pint(range=(1, 1000), name='n_estimators')(ExtraTreesClassifier)
    pyvotune.pfloat(range=(0, 1), name='min_density')(ExtraTreesClassifier)
    pyvotune.pconst(value=1, name='n_jobs')(ExtraTreesClassifier)
    pyvotune.pbool(name='bootstrap')(ExtraTreesClassifier)
    pyvotune.pbool(name='oob_score')(ExtraTreesClassifier)

    pyvotune.dense_input(GradientBoostingClassifier)
    pyvotune.excl_terminal(GradientBoostingClassifier)
    pyvotune.pint(range=(10, 1000), name='n_estimators')(GradientBoostingClassifier)
    pyvotune.pint(range=(1, n_features), name='max_features')(GradientBoostingClassifier)
    pyvotune.pfloat(range=(0, 1), name='learn_rate')(GradientBoostingClassifier)
    pyvotune.pfloat(range=(0, 1), name='subsample')(GradientBoostingClassifier)

    pyvotune.dense_input(GaussianNB)
    pyvotune.excl_terminal(GaussianNB)

    pyvotune.dense_input(MultinomialNB)
    pyvotune.pfloat(range=(0, 1), name='alpha')(MultinomialNB)
    pyvotune.pbool(name='fit_prior')(MultinomialNB)
    pyvotune.excl_terminal(MultinomialNB)

    pyvotune.dense_input(KNeighborsClassifier)
    pyvotune.excl_terminal(KNeighborsClassifier)
    pyvotune.pint(range=(2, 100), name='n_neighbors')(KNeighborsClassifier)
    pyvotune.choice(
        choices=['uniform', 'distance'], name='weights')(KNeighborsClassifier)
    pyvotune.choice(
        choices=[
            'auto', 'ball_tree', 'kd_tree', 'brute'], name='algorithm')(
                KNeighborsClassifier)
    pyvotune.pint(range=(10, 100), name='leaf_size')(KNeighborsClassifier)
    pyvotune.pint(range=(1, 20), name='p')(KNeighborsClassifier)

    pyvotune.excl_terminal(SVC)
    pyvotune.pfloat(range=(0, 1000), name='C')(SVC)
    pyvotune.choice(choices=['linear', 'poly', 'rbf', 'sigmoid'], name='kernel')(SVC)
    pyvotune.pint(range=(0, 10), name='degree')(SVC)
    pyvotune.pfloat(range=(0, 100.), name='gamma')(SVC)
    pyvotune.pfloat(range=(-10000, 10000.), name='coef0')(SVC)
    pyvotune.pbool(name='shrinking')(SVC)

    pyvotune.excl_terminal(NuSVC)
    pyvotune.pfloat(range=(0, 1.), name='nu')(NuSVC)
    pyvotune.choice(choices=['poly', 'rbf', 'sigmoid'], name='kernel')(NuSVC)
    pyvotune.pint(range=(0, 10), name='degree')(NuSVC)
    pyvotune.pfloat(range=(0, 100.), name='gamma')(NuSVC)
    pyvotune.pfloat(range=(-10000, 10000.), name='coef0')(NuSVC)
    pyvotune.pbool(name='shrinking')(NuSVC)

    return [SVC, NuSVC, GaussianNB, RandomForestClassifier, MultinomialNB,
            KNeighborsClassifier, ExtraTreesClassifier,
            GradientBoostingClassifier]
