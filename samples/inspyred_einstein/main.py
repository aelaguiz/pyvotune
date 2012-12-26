import inspyred
import pyvotune

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
@pyvotune.float(range=(-100000000, 100000000))
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
    #res = genome.assemble()
    #print "Result of assembly", res
    #individual = genome.assembled
    #print individual

    #pass


@inspyred.ec.evaluators.evaluator
def evaluator(candidate, args):
    candidate.assemble()
    individual = candidate.assembled
    loader = individual[0]
    loader.set_equation(individual[1:])

    total_err = 0

    for i in range(100):
        val = random.uniform(-100000, 100000)

        target = val * (299792458 ** 2)
        observed = loader(val)

        err = abs(target - observed)

        total_err += err

    #print "Evaluating", loader, "=", total_err

    return total_err

if __name__ == '__main__':
    pyvotune.set_debug(False)

    gen = pyvotune.Generate(
        gene_pool=[mass, someconst, oper],
        max_length=10,
        noop_frequency=0.2)

    #loader = individual[0]
    #loader.set_equation(individual[1:])
    #print loader(5)

    ea = inspyred.ec.GA(random.Random())
    ea.terminator = inspyred.ec.terminators.time_termination
    #ea.logger = pyvotune.log.logger()

    final_pop = ea.evolve(
        generator=generator,
        evaluator=evaluator,
        pyvotune_generator=gen,

        max_time=15,
        pop_size=100,
        maximize=False,
        num_elites=2)

    best = max(final_pop)
    candidate = best.candidate
    candidate.assemble()
    best_loader = candidate.assembled[0]
    best_loader.set_equation(candidate.assembled[1:])
    print "Best Solution:", best_loader
    print "Fitness", best.fitness
