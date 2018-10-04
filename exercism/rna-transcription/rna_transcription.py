def to_rna(dna_strand):
    rna_strand = ''
    transcription = {
        'A': 'U',
        'T': 'A',
        'G': 'C',
        'C': 'G'
    }
    for letter in dna_strand.upper():
        if letter not in 'ACTG':
            raise ValueError('Letter ' + letter + ' is not accepted.')
        else:
            rna_strand += transcription[letter]
    return rna_strand
