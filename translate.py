#! /usr/bin/env python3

import sys

def translate_sequence(rna_sequence, genetic_code):
    rna_sequence = rna_sequence.upper()
    protein = ""

    for i in range(0, len(rna_sequence) - 2, 3):
        codon = rna_sequence[i:i+3]
        aa = genetic_code.get(codon, "")

        if aa == "*":
            break
       
        protein += aa

    return protein


def get_all_translations(rna_sequence, genetic_code):
    rna_sequence = rna_sequence.upper()
    peptides = []

    for frame in range(3):
        i = frame
        while i <= len(rna_sequence) - 3:
            codon = rna_sequence[i:i+3]

            if codon == "AUG":  # start codon
                protein = ""
                j = i

                while j <= len(rna_sequence) - 3:
                    codon = rna_sequence[j:j+3]
                    aa = genetic_code.get(codon, "")

                    if aa == "*":
                        break

                    protein += aa
                    j += 3

                if protein:
                    peptides.append(protein)

            i += 3

    return peptides


def get_reverse(sequence):
    sequence = sequence.upper()
    return sequence[::-1]


def get_complement(sequence):
    sequence = sequence.upper()

    comp = {
        "A": "U",
        "U": "A",
        "C": "G",
        "G": "C"
    }

    return "".join(comp.get(base, base) for base in sequence)


def reverse_and_complement(sequence):
    return get_complement(get_reverse(sequence))


def get_longest_peptide(rna_sequence, genetic_code):
    rna_sequence = rna_sequence.upper()

    peptides = []

    # forward strand
    peptides += get_all_translations(rna_sequence, genetic_code)

    # reverse complement strand
    rev_comp = reverse_and_complement(rna_sequence)
    peptides += get_all_translations(rev_comp, genetic_code)

    if not peptides:
        return ""

    return max(peptides, key=len)
