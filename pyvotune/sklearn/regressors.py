# -*- coding: utf-8 -*-
import pyvotune
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor


def get_regressors(n_features):
    pyvotune.dense_input(RandomForestRegressor)
    pyvotune.excl_terminal(RandomForestRegressor)
    pyvotune.pint(range=(1, 1000), name='n_estimators')(RandomForestRegressor)
    pyvotune.pfloat(range=(0, 1), name='min_density')(RandomForestRegressor)
    pyvotune.pconst(value=1, name='n_jobs')(RandomForestRegressor)
    pyvotune.pbool(name='bootstrap')(RandomForestRegressor)

    pyvotune.dense_input(GradientBoostingRegressor)
    pyvotune.excl_terminal(GradientBoostingRegressor)
    pyvotune.pint(range=(10, 5000), name='n_estimators')(GradientBoostingRegressor)
    pyvotune.pint(range=(1, n_features), name='max_features')(GradientBoostingRegressor)
    pyvotune.pfloat(range=(0, 1), name='learning_rate')(GradientBoostingRegressor)
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

    return [RandomForestRegressor, GradientBoostingRegressor, KNeighborsRegressor]
