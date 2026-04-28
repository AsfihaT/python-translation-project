import re


def vet_nucleotide_sequence(sequence):
    sequence = sequence.upper()

    if sequence == "":
        return None

    # valid DNA
    if re.match(r'^[ATCG]+$', sequence):
        return None

    # valid RNA
    if re.match(r'^[AUCG]+$', sequence):
        return None

    # mixed DNA + RNA → ERROR
    if re.match(r'^[ATUCG]+$', sequence):
        raise Exception("Mixed DNA/RNA sequence")

    # invalid characters
    return sequence


def vet_codon(codon, raise_exception=False):
    codon = codon.upper()

    # invalid cases
    is_invalid = (
        len(codon) != 3 or
        'T' in codon or
        not re.match(r'^[AUCG]+$', codon)
    )

    if is_invalid:
        if raise_exception:
            raise Exception("Invalid codon")
        return codon

    return None


def dna_to_rna(sequence):
    return sequence.upper().replace('T', 'U')


def find_first_orf(sequence, start_codons=['AUG'], stop_codons=['UAA', 'UAG', 'UGA']):
    # validate sequence
    vet_nucleotide_sequence(sequence)

    if sequence == "":
        return ""

    # convert DNA → RNA if needed
    if 'T' in sequence.upper():
        sequence = dna_to_rna(sequence)
    else:
        sequence = sequence.upper()

    n = len(sequence)

    # scan for first start codon
    for i in range(n - 2):
        codon = sequence[i:i+3]

        if codon in start_codons:
            # scan in-frame for stop codon
            for j in range(i, n - 2, 3):
                current = sequence[j:j+3]

                if current in stop_codons:
                    return sequence[i:j+3]

            return ""

    return ""
