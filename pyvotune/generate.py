# -*- coding: utf-8 -*-

import random
from log import logger


class Generate:
    def __init__(self, rng=random):
        self.rng = rng
        pass

    def random_genome(gene_pool, length):
        state = {
            'empty': True
        }

        for i in range(length):
            pass

    def next_gene(self, gene_pool, state):
        avail_genes = [self.is_gene_avail(gene, state) for gene in gene_pool]

        if not avail_genes:
            return

        return self.rng.choice(avail_genes)

    def is_gene_avail(self, gene, state):
        input_requirements = gene._pyvotune['input']

        for req, val in input_requirements.iteritems():
            if req == '_fn':
                if not val(gene, state):
                    return False
            elif req not in state:
                return False
            elif state[req] != val:
                return False

        return True

    def update_state(self, gene, state):
        output_updates = gene._pyvotune['output']

        for key, val in output_updates.iteritems():
            if key == '_fn':
                state = val(gene, state)
            else:
                state[key] = val

        state['empty'] = False
        return state
