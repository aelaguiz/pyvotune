# -*- coding: utf-8 -*-

import inspyred
import pyvotune
import sys
import re

import random


@pyvotune.loader
@pyvotune.output_type("scalar")
class mass:
    def set_equation(self, pipeline):
        equat = ""

        for step in pipeline:
            equat += " " + step()

        self.equation = equat

    def __repr__(self):
        return "m" + self.equation

    def __call__(self, m):
        return eval(str(m) + self.equation)


@pyvotune.input_type("operator")
@pyvotune.output_type("scalar")
@pyvotune.terminal
@pyvotune.pfloat(range=(-100000000, 100000000))
class someconst:
    def __init__(self, c):
        self.c = c

    def __call__(self):
        return str(self.c)


@pyvotune.input_type("scalar")
@pyvotune.output_type("operator")
@pyvotune.non_terminal
@pyvotune.choice(choices=["/", "*", "-", "+"])
class oper:
    def __init__(self, op):
        self.op = op

    def __call__(self):
        return self.op


def generator(random, args):
    gen = args['pyvotune_generator']

    return gen.generate()


@inspyred.ec.evaluators.evaluator
def evaluator(candidate, args):
    equation = eq(candidate)
    if not equation:
        #print "Invalidate candidate", candidate
        return sys.maxint

    total_err = 0

    for i in range(100):
        val = random.uniform(-100000, 100000)

        target = actual(val)
        observed = equation(val)

        err = abs(target - observed)

        total_err += err

    #print "Evaluating", loader, "=", total_err

    return total_err


def actual(val):
    return val * (299792458 ** 2)


def eq(candidate):
    if not candidate.assemble():
        return

    #print "Validate candidate", candidate

    individual = candidate.assembled
    loader = individual[0]
    loader.set_equation(individual[1:])

    return loader


def comma_me(amount):
    if not isinstance(amount, basestring):
        amount = '{0:f}'.format(amount)
    orig = amount
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>,\g<2>', amount)
    if orig == new:
        return new
    else:
        return comma_me(new)


if __name__ == '__main__':
    pyvotune.set_debug(False)

    gen = pyvotune.Generate(
        gene_pool=[mass, someconst, oper],
        max_length=10,
        noop_frequency=0.2)

    ea = inspyred.ec.GA(random.Random())
    ea.terminator = inspyred.ec.terminators.time_termination
    ea.observer = inspyred.ec.observers.stats_observer

    ea.variator = [
        pyvotune.variators.param_reset_mutation,
        pyvotune.variators.n_point_crossover
    ]
    #ea.logger = pyvotune.log.logger()

    final_pop = ea.evolve(
        generator=generator,
        evaluator=evaluator,
        pyvotune_generator=gen,

        max_time=15,
        pop_size=100,
        maximize=False,
        num_elites=5)

    best = max(final_pop)
    best_eq = eq(best.candidate)
    print "Best Solution:", best_eq
    print "Fitness", best.fitness
    print ""

    for i in range(100):
        #val = random.uniform(-100000, 100000)
        val = i

        target = actual(val)
        observed = best_eq(val)

        err = abs(target - observed)
        print i, comma_me(target), comma_me(observed), comma_me(err)
