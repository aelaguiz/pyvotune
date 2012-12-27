# -*- coding: utf-8 -*-

"""
    pyvotune.genome
    --------------------------

    This module defines the Genome class which represents one genetic
    identity and can be translated (assembled) into an individual
"""

from pyvotune.log import logger
from pyvotune.assembly_state import AssemblyState

from pyvotune.pyvotune_globals import NOOP_GENE

log = logger()


class Genome(list):
    def __init__(self, genome_id):
        self.genome_id = genome_id
        self.state = AssemblyState()

        self.assembled = None

        log.debug(
            u"G{0}: Instantiated new genome".format(self.genome_id))

    def add_gene(self, param_vals, gene):
        """
        Adds a gene and it's parameters to the current genome
        """
        self += [('param', p) for p in param_vals]
        self.append(('gene', gene))

        self.state.gene_update(gene)

        log.debug(
            u"G{0}: Added new gene {1}".format(self.genome_id, gene))

    def does_gene_fit(self, gene):
        """
        Checks if a gene would fit into the current genome given the
        existing assembly state
        """
        return self.state.is_gene_avail(gene)

    def validate(self):
        """
        Validates the current genome, swallows all exceptions and
        simply fails assembly if there are problems
        """
        try:
            return self._assemble(assemble=False)
        except:
            log.exception(
                u"G{0}: Assembly hard excepted, failing".format(
                    self.genome_id))
            return False

    def assemble(self):
        """
        Assembles the current genome, swallows all exceptions and
        simply fails assembly if there are problems
        """
        try:
            return self._assemble()
        except:
            log.exception(
                u"G{0}: Assembly hard excepted, failing".format(
                    self.genome_id))
            return False

    def _assemble(self, assemble=True):
        """
        Actual work function that validates with optional assembly step
        """
        to_assemble = self.group_genes()

        if to_assemble is False:
            return False

        if assemble:
            self.assembled = [
                self.construct_gene(g, p, v) for g, p, v in to_assemble]

            log.debug(
                u"G{0}: Assembled successfully".format(self.genome_id))
        return True

    def group_genes(self):
        """
        Returns a list containing genes and the matching parameter values
        """
        to_assemble = []

        # Split out into params and genes
        remaining_param_vals = [g for t, g in self if t == 'param']
        active_genes = [g for t, g in self if t == 'gene' and g != NOOP_GENE]
        num_active = len(active_genes)

        self.state.clear()

        for i, gene in enumerate(active_genes):
            # We want to ensure that the final gene is validat as a terminal, so when
            # we reach the end of the genome ensure the state is updated to reflect that
            if i == (num_active - 1):
                self.state["last"] = True

            if not self.does_gene_fit(gene):
                log.debug(
                    u"G{0}: Invalid - Gene does not fit in current state {1} {2}".format(
                        self.genome_id, gene, self.state))
                return False

            gene_params = self.get_gene_params(gene)
            num_gene_params = len(gene_params)

            if num_gene_params > len(remaining_param_vals):
                log.debug(
                    u"G{0}: Invalid - Not enough remaining parameters ({1} < {2})".format(
                        self.genome_id, num_gene_params, len(remaining_param_vals)))

                return False

            gene_param_vals = remaining_param_vals[:num_gene_params]
            remaining_param_vals = remaining_param_vals[num_gene_params:]

            for i, (param, val) in enumerate(zip(gene_params, gene_param_vals)):
                if not param.check(val):
                    log.debug(
                        u"G{0}: Invalid - Parameter {1} failed assembly".format(
                            self.genome_id, i))

                    return False

            to_assemble.append((gene, gene_params, gene_param_vals))
            self.state.gene_update(gene)

        return to_assemble

    def construct_gene(self, gene, gene_params, param_vals):
        """
        Returns an instantiated gene given the values to pass to it's constructor/factory meth
        """
        cons = gene
        if hasattr(gene, '_pyvotune_assembly_params') and\
                'factory_fn' in gene._pyvotune_assembly_params:
            cons = gene._pyvotune_assembly_params['factory_fn']

        log.debug(u"G{0}: Instantiating gene {1} with {2}".format(
            self.genome_id, gene, param_vals))
        return cons(*param_vals)

    def get_gene_params(self, gene):
        if not hasattr(gene, '_pyvotune_params'):
            return []
        return gene._pyvotune_params
