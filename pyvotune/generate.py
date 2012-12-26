# -*- coding: utf-8 -*-

from log import logger
from genome import Genome

import random


class Generate:
    def __init__(self, rng=random):
        self.rng = rng
        self.logger = logger()

    def random_genome(gene_pool, length):
        genome = Genome()

        for i in range(length):
            pass

    def next_gene(self, gene_pool, genome):
        state = genome.state
        avail_genes = [state.is_gene_avail(gene) for gene in gene_pool]

        if not avail_genes:
            return

        return self.rng.choice(avail_genes)
