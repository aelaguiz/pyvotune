# -*- coding: utf-8 -*-

import inspyred
import inspyred.ec.cea_parallel_evaluator
import pyvotune
import pyvotune.sklearn
import argparse
import random
import sys
import redis
import time


import multiprocessing
from shared import load_dataset, generator, evaluator, _evaluator,\
    get_gene_pool, validate_models, classify_models


log = pyvotune.log.logger()


def get_args():
    parser = argparse.ArgumentParser(description='Lark',
                                     formatter_class=
                                     argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-r', '--host', dest='host', type=str,
                        default='localhost', required=False,
                        help="Redis host")

    parser.add_argument('-p', '--port', dest='port', type=int,
                        default=6379, required=False,
                        help="Redis port")

    parser.add_argument('-b', '--db', dest='db', type=int,
                        default=0, required=False,
                        help="Redis db")

    parser.add_argument('-g', '--grid_size', dest='grid_size', type=int,
                        default=None, required=True,
                        help="Size of eval grid")

    parser.add_argument('-s', '--neighborhood_size', dest='neighborhood_size', type=int,
                        default=None, required=True,
                        help="Diameter of neighborhood")

    parser.add_argument('-t', '--eval_timeout', dest='eval_timeout', type=int,
                        default=None, required=True,
                        help="Max duration of an eval in seconds")

    parser.add_argument('-u', '--num_samples', dest='num_samples', type=int,
                        default=None, required=False,
                        help="Maximum number of samples to test with")

    parser.add_argument('-l', '--max_length', dest='max_length', type=int,
                        default=None, required=False,
                        help="Maximum length of genome")

    parser.add_argument('-m', '--mutation_rate', dest='mutation_rate', type=float,
                        default=None, required=True,
                        help="Mutation rate (0-1.0)")

    parser.add_argument('-c', '--crossover_rate', dest='crossover_rate', type=float,
                        default=None, required=True,
                        help="Crossover rate (0-1.0)")

    parser.add_argument('-d', '--debug-mode', dest='debug_mode', default=False,
                        action='store_true', required=False,
                        help="Enable debug mode")

    parser.add_argument('-w', '--worker-mode', dest='worker_mode', default=False,
                        action='store_true', required=False, help="Enable worker mode")

    parser.add_argument('-v', '--validate', dest='validate', default=None,
                        nargs=1, required=False,
                        help="Validate a given model")

    parser.add_argument('-k', '--classify', dest='classify', default=None,
                        nargs=1, required=False,
                        help="Save classification into given output file")

    return parser.parse_args()

if __name__ == '__main__':
    app_args = get_args()

    load_dataset(app_args.num_samples)

    pyvotune.set_debug(app_args.debug_mode)

    rng = random.Random()
    gene_pool = get_gene_pool(rng)

    if app_args.classify:
        if not app_args.validate:
            log.error("Need path to model -v")
            sys.exit(0)

        classify_models(app_args.validate[0], app_args.classify[0])
        sys.exit(1)
    elif app_args.validate:
        validate_models(app_args.validate[0])
        sys.exit(1)

    if not app_args.worker_mode:
        #################################
        # Initialize PyvoTune Generator #
        #################################
        gen = pyvotune.Generate(
            initial_state={
                'sparse': False
            },
            gene_pool=gene_pool,
            max_length=app_args.max_length,
            noop_frequency=0.2,
            rng=rng)

        ####################################
        # Initialize Inspyred Genetic Algo #
        ####################################
        ea = inspyred.ec.cEA(rng)
        ea.logger = log
        ea.terminator = [
            #inspyred.ec.terminators.time_termination,
            inspyred.ec.terminators.average_fitness_termination
        ]
        ea.selector = inspyred.ec.selectors.fitness_proportionate_selection

        ea.archiver = pyvotune.archivers.pickle_wrap_archiver

        ea.observer = pyvotune.observers.stats_observer

        # Use PyvoTun variators
        ea.variator = [
            pyvotune.variators.random_reset_mutation,
            pyvotune.variators.param_reset_mutation,
            pyvotune.variators.scramble_mutation,
            pyvotune.variators.uniform_crossover,
            pyvotune.variators.n_point_crossover
        ]


        # Go!
        final_pop = ea.evolve(
            neighborhood=inspyred.ec.neighborhoods.grid_neighborhood,

            generator=generator,
            evaluator=pyvotune.evaluators.cell_evaluator_rq,
            pyvotune_generator=gen,

            async_evaluator=True,

            rq_host=app_args.host,
            rq_port=app_args.port,
            rq_db=app_args.db,
            rq_evaluator=evaluator,
            rq_timeout=app_args.eval_timeout,
            rq_timeout_fitness=0.,

            crossover_rate=app_args.crossover_rate,
            mutation_rate=app_args.mutation_rate,

            tolerance=0.01,
            #max_time=300,
            
            underlying_archiver=inspyred.ec.archivers.best_archiver,
            archive_path='./archive.pkl',

            nbh_grid_size=app_args.grid_size,
            nbh_size=app_args.neighborhood_size,
            num_selected=2,

            maximize=True,
            num_elites=5)

        ####################
        # Display Solution #
        ####################
        best = max(final_pop)
        fitness = _evaluator(best.candidate, display=True)
        log.info("Fitness: %f" % fitness)
        log.info(best.candidate)
    else:
        import pysplash
        pysplash.set_debug(app_args.debug_mode)

        # Start redis queue workers
        pyvotune.evaluators.cea_rq_worker.start_pool(
            app_args.host, app_args.port, '', app_args.db)
