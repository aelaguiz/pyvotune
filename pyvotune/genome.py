# -*- coding: utf-8 -*-

from log import logger
from assembly_state import AssemblyState


class Genome:
    def __init__(self, genome_id):
        self.logger = logger()
        self.genome_id = genome_id
        self.param_vals = []
        self.genes = []
        self.state = AssemblyState()

        self.assembled = None

        self.logger.debug(
            u"G{0}: Instantiated new genome".format(self.genome_id))

    def add_gene(self, param_vals, gene):
        self.param_vals += param_vals
        self.genes.append(gene)

    def assemble(self):
        try:
            return self._assemble()
        except:
            self.logger.exception(
                u"G{0}: Assembly hard excepted, failing".format(
                    self.genome_id))
            return False

    def _assemble(self):
        remaining_param_vals = list(self.param_vals)

        for gene in self.genes:
            gene_params = self.get_gene_params(gene)
            num_gene_params = len(gene_params)

            if num_gene_params > len(remaining_param_vals):
                self.logger.debug(
                    u"G{0}: Invalid - Not enough remaining parameters ({1} < {2})".format(
                        self.genome_id, num_gene_params, len(remaining_param_vals)))

                return False

            gene_param_vals = remaining_param_vals[:num_gene_params]
            remaining_param_vals = remaining_param_vals[num_gene_params:]

            for i, (param, val) in enumerate(zip(gene_params, gene_param_vals)):
                if not param.check(val):
                    self.logger.debug(
                        u"G{0}: Invalid - Parameter {1} failed assembly".format(
                            self.genome_id, i))

                    return False

        self.logger.debug(
            u"G{0}: Assembled successfully".format(self.genome_id))
        return True

    def get_gene_params(self, gene):
        if not hasattr(gene, '_pyvotune_params'):
            return []
        return gene._pyvotune_params
