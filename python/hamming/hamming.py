def distance(strand_a, strand_b):
    if len(strand_a) != len(strand_b):
        raise ValueError('The strands are different in length.')
    else:
        return sum(nuc_a != nuc_b for nuc_a, nuc_b in zip(strand_a, strand_b))
