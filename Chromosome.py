class Chromosome:
    def __init__(self, gene_list):
        self.gene_list = gene_list

    def __hash__(self):
        genes_hash = hash(tuple(self.gene_list))
        return genes_hash