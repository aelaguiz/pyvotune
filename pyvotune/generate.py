# -*- coding: utf-8 -*-

"""
    pyvotune.generate
    --------------------------

    This module defines the Generate class which creates Genomes
    for consumption by an evoluationary algorithm.
"""

from pyvotune.log import logger
from pyvotune.genome import Genome
from pyvotune.pyvotune_globals import NOOP_GENE
from pyvotune.util.id_generator import get_id

import random

log = logger()


class Generate:
    def __init__(
            self, gene_pool,
            max_length,
            noop_frequency=0.2,
            initial_state={},
            rng=random):
        self.initial_state = initial_state
        self.max_length = max_length
        self.noop_frequency = noop_frequency
        self.rng = rng
        self.gene_pool = gene_pool

    def generate(self, max_retries=25):
        for i in range(max_retries):
            genome = self._generate()

            if genome:
                return genome

        log.error(u"Generate: Failed after {0} tries to generate a genome".format(
            max_retries))

    def _generate(self):
        genome = Genome(get_id(), self.initial_state)

        for i in range(self.max_length):
            gene = self.next_gene(genome)

            if not gene:
                #log.debug(u"Generate: Failed, ran out of valid genes")
                return

            params = self.get_gene_param_vals(gene)
            genome.add_gene(params, gene)

        if genome.validate():
            return genome

        #log.debug(u"Generate: Failed, invalid genome generated")

    def next_gene(self, genome):
        if self.rng.random() < self.noop_frequency:
            return NOOP_GENE

        avail_genes = [gene for gene in self.gene_pool if genome.does_gene_fit(gene)]

        if not avail_genes:
            #log.debug(u"Generate: No available genes")
            return

        #log.debug(u"Generate: Available genes {0}".format(avail_genes))
        return self.rng.choice(avail_genes)

    def get_gene_param_vals(self, gene):
        params = self.get_gene_params(gene)
        return [p.generate() for p in params]

    def get_gene_params(self, gene):
        if not hasattr(gene, '_pyvotune_params'):
            return []
        return gene._pyvotune_params
