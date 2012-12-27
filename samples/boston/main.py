import inspyred
import pyvotune
import random
import sys

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline
import sklearn.datasets

pyvotune.dense_input(RandomForestRegressor)
pyvotune.terminal(RandomForestRegressor)
pyvotune.pint(range=(1, 1000), name='n_estimators')(RandomForestRegressor)
pyvotune.pfloat(range=(0, 1), name='min_density')(RandomForestRegressor)
pyvotune.pconst(value=1, name='n_jobs')(RandomForestRegressor)
pyvotune.pbool(name='bootstrap')(RandomForestRegressor)

pyvotune.dense_input(GradientBoostingRegressor)
pyvotune.terminal(GradientBoostingRegressor)
pyvotune.pint(range=(10, 5000), name='n_estimators')(GradientBoostingRegressor)
pyvotune.pint(range=(1, 13), name='max_features')(GradientBoostingRegressor)
pyvotune.pfloat(range=(0, 1), name='learning_rate')(GradientBoostingRegressor)
pyvotune.pfloat(range=(0, 1), name='subsample')(GradientBoostingRegressor)

pyvotune.dense_input(KNeighborsRegressor)
pyvotune.terminal(KNeighborsRegressor)
pyvotune.pint(range=(2, 100), name='n_neighbors')(KNeighborsRegressor)
pyvotune.choice(choices=['uniform', 'distance'], name='weights')(KNeighborsRegressor)
pyvotune.choice(choices=['auto', 'ball_tree', 'kd_tree', 'brute'], name='algorithm')(KNeighborsRegressor)
pyvotune.pint(range=(10, 100), name='leaf_size')(KNeighborsRegressor)
pyvotune.pint(range=(1, 20), name='p')(KNeighborsRegressor)


def generator(random, args):
    gen = args['pyvotune_generator']

    return gen.generate()


@inspyred.ec.evaluators.evaluator
def evaluator(candidate, args):
    individual = train_candidate(
        candidate, args['train_X'], args['train_y'])

    if not individual:
        return sys.maxint

    return test_individual(
        individual, args['test_X'], args['test_y'])


def train_candidate(candidate, train_X, train_y):
    if not candidate.assemble():
        return

    pipeline = Pipeline([
        (str(i), s) for i, s in enumerate(candidate.assembled)])

    pipeline.fit(train_X, train_y)

    return pipeline


def test_individual(pipeline, test_X, test_y, display=False):
    observed_y = pipeline.predict(test_X)

    mse = sklearn.metrics.mean_squared_error(
        test_y, observed_y)

    if display:
        total_err = 0
        total_actual = 0
        print "  #", "Actual", "Observed", "Err %"
        print "---", "------", "--------", "-----"
        for i, (actual, observed) in enumerate(zip(test_y, observed_y)):
            err = abs(observed - actual)
            err_pct = round(err / actual * 100., 2)

            total_err += err
            total_actual += actual

            print str(i).zfill(3), str(actual).ljust(6), str(observed).ljust(8), str(err_pct).ljust(4)
        print "MSE:", mse
        print "Avg Err %:", round(total_err / total_actual * 100., 2)

    return mse


if __name__ == '__main__':
    pyvotune.set_debug(False)

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
            GradientBoostingRegressor,
            RandomForestRegressor,
            KNeighborsRegressor],

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
        evaluator=inspyred.ec.evaluators.parallel_evaluation_mp,
        pyvotune_generator=gen,

        mp_evaluator=evaluator,
        mp_nprocs=8,

        #tolerance=0.25,
        max_time=10,

        train_X=train_X,
        train_y=train_y,
        test_X=test_X,
        test_y=test_y,

        pop_size=50,
        maximize=False,
        num_elites=5)

    best = max(final_pop)

    print best.candidate

    pipeline = train_candidate(best.candidate, train_X, train_y)
    test_individual(pipeline, validate_X, validate_y, display=True)
