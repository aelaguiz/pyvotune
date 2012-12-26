# -*- coding: utf-8 -*-

from log import logger
from genome import Genome
from pyvotune_globals import *
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
        self.logger = logger()

    def generate(self):
        genome = Genome(get_id())

        for i in range(self.max_length):
            print "On ", i, "of", self.max_length
            gene = self.next_gene(genome)

            if not gene:
                self.logger.debug(u"Generate: Failed, ran out of valid genes")
                return

            genome.add_gene([], gene)

        return genome

    def next_gene(self, genome):
        if self.rng.random() < self.noop_frequency:
            self.logger.debug(u"Generate: Noop")
            return NOOP_GENE

        avail_genes = [gene for gene in self.gene_pool if genome.does_gene_fit(gene)]

        if not avail_genes:
            self.logger.debug(u"Generate: No available genes")
            return

        self.logger.debug(u"Generate: Available genes {0}".format(avail_genes))
        return self.rng.choice(avail_genes)
