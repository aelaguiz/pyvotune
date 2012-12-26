class AssemblyState(dict):
    """
    AssemblyState is a simple key/value store which is used to
    track the state of a genome as it is being assembled. It is used
    for creation of genomes as well as assembly of existing genomes
    """
    def __init__(self):
        super(AssemblyState, self).__setitem__('empty', True)

    def __setitem__(self, key, val):
        if key == 'empty':
            return

        super(AssemblyState, self).__setitem__('empty', False)
        super(AssemblyState, self).__setitem__(key, val)

    def clear(self):
        super(AssemblyState, self).clear()
        super(AssemblyState, self).__setitem__('empty', True)

    def is_gene_avail(self, gene):
        """
        Checks a gene to ensure that the input requirements
        are met by this assembly state
        """
        input_requirements = gene._pyvotune['input']

        for req, val in input_requirements.iteritems():
            if req == '_fn':
                if not val(gene, self):
                    return False
            elif req not in self:
                return False
            elif self[req] != val:
                return False

        return True

    def gene_update(self, gene):
        """
        Updates the state to match the state provided by a gene
        on addition to a genome (output state)
        """
        output_updates = gene._pyvotune['output']

        for key, val in output_updates.iteritems():
            if key == '_fn':
                self = val(gene, self)
            else:
                self[key] = val

        self['empty'] = False
        return self
