# -*- coding: utf-8 -*-
import pyvotune
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR, NuSVR


def get_regressors(n_features):
    pyvotune.dense_input(LinearRegression)
    pyvotune.excl_terminal(LinearRegression)
    pyvotune.pbool(name='normalize')(LinearRegression)
    pyvotune.pbool(name='fit_intercept')(LinearRegression)

    pyvotune.dense_input(Ridge)
    pyvotune.excl_terminal(Ridge)
    pyvotune.pfloat(range=(0, 1), name='alpha')(Ridge)
    pyvotune.pbool(name='normalize')(Ridge)
    pyvotune.pbool(name='fit_intercept')(Ridge)

    pyvotune.dense_input(RandomForestRegressor)
    pyvotune.excl_terminal(RandomForestRegressor)
    pyvotune.pint(range=(1, 1000), name='n_estimators')(RandomForestRegressor)
    pyvotune.pfloat(range=(0, 1), name='min_density')(RandomForestRegressor)
    pyvotune.pconst(value=1, name='n_jobs')(RandomForestRegressor)
    pyvotune.pbool(name='bootstrap')(RandomForestRegressor)
    pyvotune.pbool(name='oob_score')(RandomForestRegressor)

    pyvotune.dense_input(ExtraTreesRegressor)
    pyvotune.excl_terminal(ExtraTreesRegressor)
    pyvotune.pint(range=(1, 1000), name='n_estimators')(ExtraTreesRegressor)
    pyvotune.pfloat(range=(0, 1), name='min_density')(ExtraTreesRegressor)
    pyvotune.choice(choices=['auto', 'sqrt', 'log2', None], name='max_features')(ExtraTreesRegressor)
    pyvotune.pconst(value=1, name='n_jobs')(ExtraTreesRegressor)
    pyvotune.pbool(name='bootstrap')(ExtraTreesRegressor)
    pyvotune.pbool(name='oob_score')(RandomForestRegressor)

    pyvotune.dense_input(GradientBoostingRegressor)
    pyvotune.excl_terminal(GradientBoostingRegressor)
    pyvotune.pint(range=(10, 1000), name='n_estimators')(GradientBoostingRegressor)
    pyvotune.pint(range=(1, n_features), name='max_features')(GradientBoostingRegressor)
    pyvotune.pfloat(range=(0, 1), name='learn_rate')(GradientBoostingRegressor)
    pyvotune.pfloat(range=(0, 1), name='subsample')(GradientBoostingRegressor)

    pyvotune.dense_input(KNeighborsRegressor)
    pyvotune.excl_terminal(KNeighborsRegressor)
    pyvotune.pint(range=(2, 100), name='n_neighbors')(KNeighborsRegressor)
    pyvotune.choice(
        choices=['uniform', 'distance'], name='weights')(KNeighborsRegressor)
    pyvotune.choice(
        choices=[
            'auto', 'ball_tree', 'kd_tree', 'brute'], name='algorithm')(
                KNeighborsRegressor)
    pyvotune.pint(range=(10, 100), name='leaf_size')(KNeighborsRegressor)
    pyvotune.pint(range=(1, 20), name='p')(KNeighborsRegressor)

    pyvotune.excl_terminal(SVR)
    pyvotune.pfloat(range=(0, 1000), name='C')(SVR)
    pyvotune.pfloat(range=(0, 2.0), name='epsilon')(SVR)
    pyvotune.choice(choices=['linear', 'poly', 'rbf', 'sigmoid'], name='kernel')(SVR)
    pyvotune.pint(range=(0, 10), name='degree')(SVR)
    pyvotune.pfloat(range=(0, 100.), name='gamma')(SVR)
    pyvotune.pfloat(range=(-10000, 10000.), name='coef0')(SVR)
    pyvotune.pbool(name='shrinking')(SVR)

    pyvotune.excl_terminal(NuSVR)
    pyvotune.pfloat(range=(0, 1.), name='nu')(NuSVR)
    pyvotune.choice(choices=['poly', 'rbf', 'sigmoid'], name='kernel')(NuSVR)
    pyvotune.pint(range=(0, 10), name='degree')(NuSVR)
    pyvotune.pfloat(range=(0, 100.), name='gamma')(NuSVR)
    pyvotune.pfloat(range=(-10000, 10000.), name='coef0')(NuSVR)
    pyvotune.pbool(name='shrinking')(NuSVR)

    return [RandomForestRegressor, GradientBoostingRegressor,
            KNeighborsRegressor, SVR, NuSVR, ExtraTreesRegressor,
            LinearRegression, Ridge]
