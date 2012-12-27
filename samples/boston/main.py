import inspyred
import pyvotune
import random
import sys

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline
import sklearn.datasets

pyvotune.dense_input(RandomForestRegressor)
pyvotune.terminal(RandomForestRegressor)
pyvotune.pint(range=(1, 1000), name='n_estimators')(RandomForestRegressor)
pyvotune.pfloat(range=(0, 1), name='min_density')(RandomForestRegressor)
pyvotune.pconst(value=8, name='n_jobs')(RandomForestRegressor)
pyvotune.pbool(name='bootstrap')(RandomForestRegressor)

pyvotune.dense_input(GradientBoostingRegressor)
pyvotune.terminal(GradientBoostingRegressor)
pyvotune.pint(range=(10, 5000), name='n_estimators')(GradientBoostingRegressor)
pyvotune.pint(range=(1, 13), name='max_features')(GradientBoostingRegressor)
pyvotune.pfloat(range=(0, 1), name='learn_rate')(GradientBoostingRegressor)
pyvotune.pfloat(range=(0, 1), name='subsample')(GradientBoostingRegressor)

pyvotune.dense_input(KNeighborsRegressor)
pyvotune.terminal(KNeighborsRegressor)
pyvotune.pint(range=(1, 100), name='n_neighbors')(KNeighborsRegressor)
pyvotune.choice(choices=['uniform', 'distance'], name='weights')(KNeighborsRegressor)
pyvotune.choice(choices=['auto', 'ball_tree', 'kd_tree', 'brute'], name='algorithm')(KNeighborsRegressor)
pyvotune.pint(range=(10, 100), name='leaf_size')(KNeighborsRegressor)
pyvotune.pint(range=(1, 20), name='p')(KNeighborsRegressor)

#pyvotune.dense_input(SGDRegressor)
pyvotune.terminal(SGDRegressor)
#pyvotune.pfloat(range=(0, 0.2), name='alpha')(SGDRegressor)
#pyvotune.pfloat(range=(0, 1), name='rho')(SGDRegressor)
#pyvotune.pfloat(range=(0, 1), name='eta0')(SGDRegressor)
#pyvotune.pint(range=(1, 20), name='n_iter')(SGDRegressor)


def generator(random, args):
    gen = args['pyvotune_generator']

    return gen.generate()


@inspyred.ec.evaluators.evaluator
def evaluator(candidate, args):
    if not candidate.assemble():
        return sys.maxint

    print "Testing", candidate.assembled
    #try:
    pipeline = Pipeline([
        (str(i), s) for i, s in enumerate(candidate.assembled)])

    pipeline.fit(args['train_X'], args['train_y'])

    observed_y = pipeline.predict(args['test_X'])

    mse = sklearn.metrics.mean_squared_error(
        args['test_y'], observed_y)

    print "Error", mse

    return mse
    #except Exception as e:
        #print e
        #return sys.maxint


if __name__ == '__main__':
    pyvotune.set_debug(True)

    data = sklearn.datasets.load_boston()
    X = data['data']
    y = data['target']

    train_X, temp_X, train_y, temp_y = train_test_split(X, y, train_size=0.75)
    test_X, validate_X, test_y, validate_y = train_test_split(temp_X, temp_y, train_size=0.5)

    gen = pyvotune.Generate(
        initial_state={
            'sparse': False
        },
        gene_pool=[
            RandomForestRegressor,
            GradientBoostingRegressor,
            KNeighborsRegressor],
#SGDRegressor, 
        max_length=1,
        noop_frequency=0.0)

    ea = inspyred.ec.GA(random.Random())
    ea.terminator = [
        inspyred.ec.terminators.time_termination,
        #inspyred.ec.terminators.average_fitness_termination
    ]

    ea.observer = inspyred.ec.observers.stats_observer

    ea.variator = [
        pyvotune.variators.param_reset_mutation,
        pyvotune.variators.scramble_mutation,
        pyvotune.variators.uniform_crossover
    ]
    #ea.logger = pyvotune.log.logger()

    final_pop = ea.evolve(
        generator=generator,
        evaluator=evaluator,
        pyvotune_generator=gen,

        #tolerance=0.25,
        max_time=10,

        train_X=train_X,
        train_y=train_y,
        test_X=test_X,
        test_y=test_y,

        pop_size=200,
        maximize=False,
        num_elites=5)

    best = max(final_pop)
