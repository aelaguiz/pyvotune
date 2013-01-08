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
    def __init__(self, genome_id, initial_state={}, init_parts=[], parent=None):
        self.genome_id = genome_id

        if parent and parent.parent_id:
            self.parent_id = [parent.genome_id] + parent.parent_id
        elif parent:
            self.parent_id = [parent.genome_id]
        else:
            self.parent_id = []

        self.initial_state = initial_state
        self.state = AssemblyState(initial_state)

        self.assembled = None

        [self.add_gene(v, g) for g, p, v in init_parts]

        #log.debug(
            #u"G{0}: Instantiated new genome".format(self.genome_id))

    def add_gene(self, param_vals, gene):
        """
        Adds a gene and it's parameters to the current genome
        """
        self += [('param', p) for p in param_vals]
        self.append(('gene', gene))

        self.state.gene_update(gene)

        #log.debug(
            #u"G{0}: Added new gene {1}".format(self.genome_id, gene))

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
        except Exception as e:
            log.error(e)
            log.error(
                u"G{0}: Assembly hard excepted, failing {1}".format(
                    self.genome_id, self))
            return False

    def assemble(self):
        """
        Assembles the current genome, swallows all exceptions and
        simply fails assembly if there are problems
        """
        try:
            return self._assemble()
        except Exception as e:
            log.error(e)
            log.error(
                u"G{0}: Assembly hard excepted, failing {1}".format(
                    self.genome_id, self))
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

            #log.debug(
                #u"G{0}: Assembled successfully".format(self.genome_id))
        return True

    def group_genes(self, remove_noops=True):
        """
        Returns a list containing genes and the matching parameter values
        """
        to_assemble = []

        # Split out into params and genes
        remaining_param_vals = [g for t, g in self if t == 'param']

        if remove_noops:
            active_genes = [g for t, g in self if t == 'gene' and g != NOOP_GENE]
        else:
            active_genes = [g for t, g in self if t == 'gene']

        num_active = len(active_genes)

        if 0 == num_active:
            log.debug(u"G{0}: Invalid - contains no active genes".format(
                self.genome_id))
            return False

        self.state.clear()

        for i, gene in enumerate(active_genes):
            if gene == NOOP_GENE:
                to_assemble.append((gene, [], []))
                continue

            # We want to ensure that the final gene is validat as a terminal, so when
            # we reach the end of the genome ensure the state is updated to reflect that
            if i == (num_active - 1):
                self.state["last"] = True

            if not self.does_gene_fit(gene):
                #log.debug(
                    #u"G{0}: Invalid - Gene does not fit in current state {1} {2}".format(
                        #self.genome_id, gene, self.state))
                return False

            # Placement tests are not valid when noops are enabled.
            if remove_noops and not self.state.is_gene_placement_valid(gene):
                #log.debug(
                    #u"G{0}: Invalid - Gene does not have correct placement {1} {2}".format(
                        #self.genome_id, gene, self.state))
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

        unnamed_params = [v for p, v in zip(gene_params, param_vals) if p.name is None]
        named_params = {p.name: v for p, v in zip(gene_params, param_vals) if p.name}

        #log.debug(u"G{0}: Instantiating gene {1} with {2}, {3}".format(
            #self.genome_id, gene, unnamed_params, named_params))

        return cons(*unnamed_params, **named_params)

    def __repr__(self):
        grouped_genes = self.group_genes(False)

        strval = "Genome: %s\n" % self.genome_id
        strval += "  Parents = %s\n" % (self.parent_id)

        if not grouped_genes:
            strval += "INVALID GENOME"
        else:
            for i, (gene, gene_params, gene_param_vals) in enumerate(
                    grouped_genes):
                if gene == NOOP_GENE:
                    strval += "\tGene %d: NOOP\n" % (i)
                    continue

                strval += "\tGene %d: %s\n" % (i, gene.__name__)

                for j, (param, val) in enumerate(zip(gene_params, gene_param_vals)):
                    strval += "\t\tParam %d: %s - %s\n" % (j, param, val)

        return strval

    def __eq__(self, other):
        for val1, val2 in zip(self, other):
            if val1 != val2:
                return False

        return True

    def get_gene_params(self, gene):
        if not hasattr(gene, '_pyvotune_params'):
            return []
        return gene._pyvotune_params
