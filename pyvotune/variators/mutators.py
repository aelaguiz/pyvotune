# -*- coding: utf-8 -*-

import functools
import inspyred

import pyvotune
from pyvotune.log import logger
from pyvotune.util.id_generator import get_id

log = logger()


def mutator(mutate):
    """
    Creates an inspyred mutator function which will always return either the current genome
    or a new and valid genome mutated from the current genome
    """
    @functools.wraps(mutate)
    def validating_mutator(random, genome, args):
        next_genome = mutate(random, genome, args)

        if next_genome.validate():
            return next_genome

        return genome

    return inspyred.ec.variators.mutators.mutator(
        validating_mutator)


@mutator
def param_reset_mutation(random, candidate, args):
    """
    Varies a candidate by randomly resetting parameters
    """
    rate = args.setdefault('mutation_rate', 0.1)
    mutant = pyvotune.Genome(
        get_id(), initial_state=candidate.initial_state,
        parent=candidate)
    grouped_genes = candidate.group_genes(remove_noops=False)
    if not grouped_genes:
        print "Received invalid genome in mutator"
        print candidate

    for gene, gene_param, param_values in grouped_genes:
        new_values = []
        for param, value in zip(gene_param, param_values):
            if random.random() < rate:
                new_values.append(param.generate())
            else:
                new_values.append(value)

        mutant.add_gene(new_values, gene)

    return mutant


@mutator
def random_reset_mutation(random, candidate, args):
    """
    Varies a candidate by randomly resetting parameters
    """
    rate = args.setdefault('mutation_rate', 0.1)
    generator = args['pyvotune_generator']
    max_tries = args.setdefault('reset_max_tries', 25)

    grouped_genes = candidate.group_genes(remove_noops=False)
    mutant_genes = [random.random() for g in grouped_genes]

    for i in range(max_tries):
        mutant = pyvotune.Genome(
            get_id(),
            initial_state=candidate.initial_state,
            parent=candidate)

        for (gene, gene_param, param_values), r in zip(grouped_genes, mutant_genes):
            new_values = []

            if r < rate:
                replacement = random.choice(generator.gene_pool)
                vals = generator.get_gene_param_vals(replacement)

                mutant.add_gene(vals, replacement)
            else:
                mutant.add_gene(param_values, gene)

        if mutant.validate():
            return mutant

    return candidate


@mutator
def scramble_mutation(random, candidate, args):
    """
    Scrambles a candidate by switching around parts of the genome
    """
    rate = args.setdefault('mutation_rate', 0.1)

    if random.random() < rate:
        grouped_genes = candidate.group_genes(remove_noops=False)

        size = len(grouped_genes)
        p = random.randint(0, size - 1)
        q = random.randint(0, size - 1)

        p, q = min(p, q), max(p, q)

        s = grouped_genes[p:q + 1]

        random.shuffle(s)

        return pyvotune.Genome(
            get_id(), initial_state=candidate.initial_state,
            init_parts=grouped_genes[:p] + s[::-1] + grouped_genes[q + 1:],
            parent=candidate)
    else:
        return candidate


#@mutator
#def bit_flip_mutation(random, candidate, args):
    #"""Return the mutants produced by bit-flip mutation on the candidates.

    #This function performs bit-flip mutation. If a candidate solution contains
    #non-binary values, this function leaves it unchanged.

    #.. Arguments:
       #random -- the random number generator object
       #candidate -- the candidate solution
       #args -- a dictionary of keyword arguments

    #Optional keyword arguments in args:

    #- *mutation_rate* -- the rate at which mutation is performed (default 0.1)

    #The mutation rate is applied on a bit by bit basis.

    #"""
    #rate = args.setdefault('mutation_rate', 0.1)
    #mutant = copy.copy(candidate)
    #if len(mutant) == len([x for x in mutant if x in [0, 1]]):
        #for i, m in enumerate(mutant):
            #if random.random() < rate:
                #mutant[i] = (m + 1) % 2
    #return mutant


#@mutator
#def random_reset_mutation(random, candidate, args):
    #"""Return the mutants produced by randomly choosing new values.

    #This function performs random-reset mutation. It assumes that
    #candidate solutions are composed of discrete values. This function
    #makes use of the bounder function as specified in the EC's
    #``evolve`` method, and it assumes that the bounder contains
    #an attribute called *values* (which is true for instances of
    #``DiscreteBounder``).

    #The mutation moves through a candidate solution and, with rate
    #equal to the *mutation_rate*, randomly chooses a value from the
    #set of allowed values to be used in that location. Note that this
    #value may be the same as the original value.

    #.. Arguments:
       #random -- the random number generator object
       #candidate -- the candidate solution
       #args -- a dictionary of keyword arguments

    #Optional keyword arguments in args:

    #- *mutation_rate* -- the rate at which mutation is performed (default 0.1)

    #The mutation rate is applied on an element by element basis.

    #"""
    #bounder = args['_ec'].bounder
    #try:
        #values = bounder.values
    #except AttributeError:
        #values = None
    #if values is not None:
        #rate = args.setdefault('mutation_rate', 0.1)
        #mutant = copy.copy(candidate)
        #for i, m in enumerate(mutant):
            #if random.random() < rate:
                #mutant[i] = random.choice(values)
        #return mutant
    #else:
        #return candidate




#@mutator
#def inversion_mutation(random, candidate, args):
    #"""Return the mutants created by inversion mutation on the candidates.

    #This function performs inversion mutation. It randomly chooses two
    #locations along the candidate and reverses the values within that
    #slice.

    #.. Arguments:
       #random -- the random number generator object
       #candidate -- the candidate solution
       #args -- a dictionary of keyword arguments

    #Optional keyword arguments in args:

    #- *mutation_rate* -- the rate at which mutation is performed (default 0.1)

    #The mutation rate is applied to the candidate as a whole (i.e., it
    #either mutates or it does not, based on the rate).

    #"""
    #rate = args.setdefault('mutation_rate', 0.1)
    #if random.random() < rate:
        #size = len(candidate)
        #p = random.randint(0, size - 1)
        #q = random.randint(0, size - 1)
        #p, q = min(p, q), max(p, q)
        #s = candidate[p:q + 1]
        #return candidate[:p] + s[::-1] + candidate[q + 1:]
    #else:
        #return candidate


#@mutator
#def gaussian_mutation(random, candidate, args):
    #"""Return the mutants created by Gaussian mutation on the candidates.

    #This function performs Gaussian mutation. This function
    #makes use of the bounder function as specified in the EC's
    #``evolve`` method.

    #.. Arguments:
       #random -- the random number generator object
       #candidate -- the candidate solution
       #args -- a dictionary of keyword arguments

    #Optional keyword arguments in args:

    #- *mutation_rate* -- the rate at which mutation is performed (default 0.1)
    #- *gaussian_mean* -- the mean used in the Gaussian function (default 0)
    #- *gaussian_stdev* -- the standard deviation used in the Gaussian function
      #(default 1)

    #The mutation rate is applied on an element by element basis.

    #"""
    #mut_rate = args.setdefault('mutation_rate', 0.1)
    #mean = args.setdefault('gaussian_mean', 0.0)
    #stdev = args.setdefault('gaussian_stdev', 1.0)
    #bounder = args['_ec'].bounder
    #mutant = copy.copy(candidate)
    #for i, m in enumerate(mutant):
        #if random.random() < mut_rate:
            #mutant[i] += random.gauss(mean, stdev)
    #mutant = bounder(mutant, args)
    #return mutant


#@mutator
#def nonuniform_mutation(random, candidate, args):
    #"""Return the mutants produced by nonuniform mutation on the candidates.

    #The function performs nonuniform mutation as specified in
    #(Michalewicz, "Genetic Algorithms + Data Structures = Evolution
    #Programs," Springer, 1996). This function also makes use of the
    #bounder function as specified in the EC's ``evolve`` method.

    #.. note::

       #This function **requires** that *max_generations* be specified in
       #the *args* dictionary. Therefore, it is best to use this operator
       #in conjunction with the ``generation_termination`` terminator.

    #.. Arguments:
       #random -- the random number generator object
       #candidate -- the candidate solution
       #args -- a dictionary of keyword arguments

    #Required keyword arguments in args:

    #- *max_generations* -- the maximum number of generations for which
      #evolution should take place

    #Optional keyword arguments in args:

    #- *mutation_strength* -- the strength of the mutation, where higher
      #values correspond to greater variation (default 1)

    #"""
    #bounder = args['_ec'].bounder
    #num_gens = args['_ec'].num_generations
    #max_gens = args['max_generations']
    #strength = args.setdefault('mutation_strength', 1)
    #exponent = (1.0 - num_gens / float(max_gens)) ** strength
    #mutant = copy.copy(candidate)
    #for i, (c, lo, hi) in enumerate(zip(candidate, bounder.lower_bound, bounder.upper_bound)):
        #if random.random() <= 0.5:
            #new_value = c + (hi - c) * (1.0 - random.random() ** exponent)
        #else:
            #new_value = c - (c - lo) * (1.0 - random.random() ** exponent)
        #mutant[i] = new_value
    #return mutant
