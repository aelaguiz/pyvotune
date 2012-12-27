# -*- coding: utf-8 -*-

from pyvotune.log import logger

log = logger()


class AssemblyState(dict):
    """
    AssemblyState is a simple key/value store which is used to
    track the state of a genome as it is being assembled. It is used
    for creation of genomes as well as assembly of existing genomes
    """
    def __init__(self, initial_state={}):
        if 'empty' not in initial_state:
            initial_state['empty'] = True
        if 'last' not in initial_state:
            initial_state['last'] = False

        self.initial_state = initial_state
        self.clear()

    def __setitem__(self, key, val):
        if key == 'empty':
            return

        super(AssemblyState, self).__setitem__('empty', False)
        super(AssemblyState, self).__setitem__(key, val)

    def clear(self):
        super(AssemblyState, self).clear()
        self.update(self.initial_state)

    def is_gene_avail(self, gene):
        """
        Checks a gene to ensure that the input requirements
        are met by this assembly state
        """

        if hasattr(gene, '_pyvotune') and 'input' in gene._pyvotune:
            input_requirements = gene._pyvotune['input']

            for req, val in input_requirements.iteritems():
                if req == '_fn':
                    if not val(gene, self):
                        log.debug(
                            u"Gene {0} failed validation function {1}".format(
                                gene, val))
                        return False
                elif val is None and req not in self:
                    continue
                elif req not in self:
                    log.debug(
                        u"Gene {0} is missing requirement {1}:{2} in state {3}".format(
                            gene, req, val, self))
                    return False
                elif isinstance(val, list) or isinstance(val, set):
                    if self[req] not in val:
                        log.debug(
                            u"Gene {0} requirement {1} failed {2} not in {3}".format(
                                gene, req, self[req], val))
                        return False
                elif self[req] != val:
                    log.debug(
                        u"Gene {0} requirement {1} failed {2} != {3}".format(
                            gene, req, self[req], val))
                    return False

        return True

    def gene_update(self, gene):
        """
        Updates the state to match the state provided by a gene
        on addition to a genome (output state)
        """

        if hasattr(gene, '_pyvotune') and 'output' in gene._pyvotune:
            output_updates = gene._pyvotune['output']

            for key, val in output_updates.iteritems():
                if key == '_fn':
                    self = val(gene, self)
                else:
                    self[key] = val

        self['empty'] = False
        return self
