# -*- coding: utf-8 -*-

from pyvotune.log import logger
from pyvotune.genome import Genome
from pyvotune.pyvotune_globals import NOOP_GENE
from pyvotune.util.id_generator import get_id

import random


class Generate:
    def __init__(
            self, gene_pool,
            max_length,
            noop_frequency=0.2,
            rng=random):
        self.max_length = max_length
        self.noop_frequency = noop_frequency
        self.rng = rng
        self.gene_pool = gene_pool
        self.log = logger()

    def generate(self):
        genome = Genome(get_id())

        for i in range(self.max_length):
            gene = self.next_gene(genome)

            if not gene:
                self.log.debug(u"Generate: Failed, ran out of valid genes")
                return

            params = self.get_gene_param_vals(gene, genome)
            genome.add_gene(params, gene)

        return genome

    def next_gene(self, genome):
        if self.rng.random() < self.noop_frequency:
            self.log.debug(u"Generate: Noop")
            return NOOP_GENE

        avail_genes = [gene for gene in self.gene_pool if genome.does_gene_fit(gene)]

        if not avail_genes:
            self.log.debug(u"Generate: No available genes")
            return

        self.log.debug(u"Generate: Available genes {0}".format(avail_genes))
        return self.rng.choice(avail_genes)

    def get_gene_param_vals(self, gene, genome):
        params = genome.get_gene_params(gene)
        return [p.generate() for p in params]
