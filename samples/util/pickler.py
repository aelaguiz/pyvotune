# -*- coding: utf-8 -*-

import pyvotune
import collections
import pyvotune.sklearn
import random
import copy
import sys

try:
    import cPickle as pickle
except ImportError:
    import pickle

log = pyvotune.log.logger()


def reproduce(offspring_cs, variator, rng, args):
    if isinstance(variator, collections.Iterable):
        for op in variator:
            offspring_cs = op(random=rng, candidates=offspring_cs, args=args)

        return offspring_cs
    else:
        return [variator(random=rng, candidates=offspring_cs, args=args)]


if __name__ == '__main__':
    pyvotune.set_debug(True)

    # Dummy data
    n_features = 28 * 28

    rng = random.Random()

    #################################
    # Initialize PyvoTune Generator #
    #################################
    gen = pyvotune.Generate(
        initial_state={
            'sparse': False
        },
        gene_pool=pyvotune.sklearn.get_classifiers(n_features, rng) +
        pyvotune.sklearn.get_decomposers(n_features, rng) +
        pyvotune.sklearn.get_image_features(n_features, rng) +
        pyvotune.sklearn.get_preprocessors(n_features, rng),
        max_length=4,
        noop_frequency=0.2,
        rng=rng)

    args = {
        'crossover_rate': 0.5,
        'mutation_rate': 0.3,
        'pyvotune_generator': gen
    }

    # Use PyvoTun variators
    variators = [
        pyvotune.variators.random_reset_mutation,
        pyvotune.variators.param_reset_mutation,
        pyvotune.variators.scramble_mutation,
        pyvotune.variators.uniform_crossover,
        pyvotune.variators.n_point_crossover
    ]

    genome = gen.generate(max_retries=150)

    print genome
    p_genome = pickle.dumps(genome)
    print p_genome
    u_genome = pickle.loads(p_genome)

    print pyvotune.util.side_by_side([genome, u_genome], 50)

    if genome == u_genome:
        print "EQUAL"
    else:
        print "NOT EQUAL"
