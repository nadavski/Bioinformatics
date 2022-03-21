from itertools import permutations


def AreStringListsEqual(expected, result):
    if len(expected) != len(result):
        _print_list_difference(expected, result)
        return False
    for val in expected:
        if (val not in result) or expected.count(val) != result.count(val):
            _print_list_difference(expected, result)
            return False
    return True


def _print_list_difference(expected, result):
    print("Expected: " + str(len(expected)) + ", " + ' '.join(expected) + "\n")
    print("Result:   " + str(len(result)) + ", " + ' '.join(result) + "\n")


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []


def get_reverse_complement(dna):
    dna = str.upper(dna)
    complement = ''
    for base in dna:
        if base == 'A':
            complement += 'T'
        elif base == 'T':
            complement += 'A'
        elif base == 'C':
            complement += 'G'
        elif base == 'G':
            complement += 'C'
        else:
            raise Exception('Invalid DNA base.')
    return complement[::-1]


def transcribe_dna(dna):
    return dna.replace('T', 'U')

def reverse_transcribe_rna(rna):
    return rna.replace('U', 'T')

AMINO_ACID_MASSES = [57,71,87,97,99,101,103,113,114,115,128,129,131,137,147,156,163,186]


def translate_protein(rna):
    codon_table = _construct_RNA_codon_table()
    protein = ''
    for i in range(int(len(rna)/3)):
        pos = i*3
        protein += codon_table[rna[pos:pos+3]]
    return protein


def _construct_RNA_codon_table():
    codon_table = {}
    with open('RNA_codon_table_1.txt', 'r') as datafile:
        entries = [line.strip().split(' ') for line in datafile.readlines()]
    for entry in entries:
        codon = entry[0]
        amino_acid = entry[1] if len(entry) == 2 else ''
        codon_table[codon] = amino_acid
    return codon_table


def find_peptide_encoding(dna, peptide):
    dna_rc = get_reverse_complement(dna)
    rna = transcribe_dna(dna)
    rna_rc = transcribe_dna(dna_rc)
    rna_length = len(peptide) * 3
    results = []
    for i in range(len(rna) - rna_length + 1):
        rna_snip = rna[i:i+rna_length]
        if translate_protein(rna_snip) == peptide:
            results.append(reverse_transcribe_rna(rna_snip))
    for i in range(len(rna_rc) - rna_length + 1):
        rna_snip = rna_rc[i:i + rna_length]
        if translate_protein(rna_snip) == peptide:
            results.append(get_reverse_complement(reverse_transcribe_rna(rna_snip)))

    return results


"""
    Generating Theoretical Spectrum Problem: Generate the theoretical spectrum of a cyclic peptide.
     Input: An amino acid string Peptide.
     Output: Cyclospectrum(Peptide).
"""
def cyclospectrum_v1(peptide):
    amino_acid_mass_table = _get_amino_acid_mass_table()
    return _cyclospectrum(amino_acid_mass_table, peptide)


def _cyclospectrum(amino_acid_mass_table, peptide):
    sub_peptides = [['',0]]
    for l in range(len(peptide))[1:]:
        for pos in range(len(peptide)):
            sub_peptide = peptide[pos:pos+l] if pos+l<=len(peptide) else peptide[pos:]+peptide[:pos+l-len(peptide)]
            sub_peptides.append([sub_peptide,0])
    if (peptide):
        sub_peptides.append([peptide,0])

    for entry in sub_peptides:
        entry[1] = _get_peptide_mass(amino_acid_mass_table, entry[0])
    return sorted(sub_peptides, key=lambda entry: entry[1])

amino_acid_mass_table = {'G':57,'A':71,'S':87,'P':97,'V':99,'T':101,'C':103,'I':113,'L':113,'N':114,'D':115,'K':128,'Q':128,'E':129,'M':131,'H':137,'F':147,'R':156,'Y':163,'W':186}

def cyclospectrum(peptide):
    prefix_mass = [0]
    for i in range(len(peptide)):
        prefix_mass.append(prefix_mass[i]+amino_acid_mass_table[peptide[i]])

    theoretical_spectrum = [0]
    for i in range(len(prefix_mass)-1):
        for j in range(i+1, len(prefix_mass)):
            theoretical_spectrum.append(prefix_mass[j]-prefix_mass[i])
            if i > 0 and j < len(prefix_mass)-1:
                theoretical_spectrum.append(prefix_mass[-1] - (prefix_mass[j] - prefix_mass[i]))
    return sorted(theoretical_spectrum)

def test_cyclospectrum_dynamic_programming(peptide):
    import re
    prefix_mass = []
    for i in range(len(peptide)):
        prefix_mass.append(peptide[:i])

    theoretical_spectrum = []
    for i in range(len(prefix_mass)-1):
        for j in range(i+1, len(prefix_mass)):
            sub = re.sub(prefix_mass[i], '', prefix_mass[j])
            theoretical_spectrum.append(sub)
            #if i+j>len(prefix_mass):
            #    theoretical_spectrum.append(prefix_mass[j]-prefix_mass[i]+prefix_mass[j-i+1])
            if i > 0 and j < len(prefix_mass)-1:
                theoretical_spectrum.append(re.sub(sub, '', prefix_mass[-1]))
    print(theoretical_spectrum)



def linearspectrum(peptide):
    amino_acid_mass_table = _get_amino_acid_mass_table()
    sub_peptides = [['',0]]
    for l in range(len(peptide))[1:]:
        for pos in range(len(peptide)):
            if pos + l <= len(peptide):
                sub_peptide = peptide[pos:pos+l]
                sub_peptides.append([sub_peptide,0])
    if (peptide):
        sub_peptides.append([peptide,0])

    for entry in sub_peptides:
        entry[1] = _get_peptide_mass(amino_acid_mass_table, entry[0])
    return sorted(sub_peptides, key=lambda entry: entry[1])

def _get_peptide_mass(amino_acid_mass_table, peptide):
    mass = 0
    for pos in range(len(peptide)):
        mass += amino_acid_mass_table[peptide[pos]]
    return mass


def _get_amino_acid_mass_table():
    with open('amino_acid_mass_table.txt') as datafile:
        lines = [line.strip().split(' ') for line in datafile.readlines()]
    aas, masses = zip(*lines)
    masses = [int(mass) for mass in masses]
    return dict(zip(aas, masses))


"""
    Counting Peptides with Given Mass Problem: Compute the number of peptides of given mass. 
    (weight combinations rather than amino acid combinations)
     Input: An integer m.
     Output: The number of linear peptides having integer mass m.
"""
def count_peptide_with_given_mass(mass):
    amino_acid_mass_table = _get_amino_acid_mass_table()
    return _count_sub_peptide_with_given_mass(amino_acid_mass_table, mass)


AMINO_ACID_MASSES = [57,71,87,97,99,101,103,113,114,115,128,129,131,137,147,156,163,186]

"""
Protein Translation Problem: Translate an RNA string into an amino acid string.
     Input: An RNA string Pattern and the array GeneticCode.
     Output: The translation of Pattern into an amino acid string Peptide.
"""
def translate_protein(rna):
    codon_table = _construct_RNA_codon_table()
    protein = ''
    for i in range(int(len(rna)/3)):
        pos = i*3
        protein += codon_table[rna[pos:pos+3]]
    return protein


"""
    Peptide Encoding Problem: Find substrings of a genome encoding a given amino acid sequence.
     Input: A DNA string Text, an amino acid string Peptide, and the array GeneticCode.
     Output: All substrings of Text encoding Peptide (if any such substrings exist).
     https://stepik.org/lesson/How-Do-Bacteria-Make-Antibiotics-96/step/7?unit=8261
"""
def find_peptide_encoding(dna, peptide):
    dna_rc = get_reverse_complement(dna)
    rna = transcribe_dna(dna)
    rna_rc = transcribe_dna(dna_rc)
    rna_length = len(peptide) * 3
    results = []
    for i in range(len(rna) - rna_length + 1):
        rna_snip = rna[i:i+rna_length]
        if translate_protein(rna_snip) == peptide:
            results.append(reverse_transcribe_rna(rna_snip))
    for i in range(len(rna_rc) - rna_length + 1):
        rna_snip = rna_rc[i:i + rna_length]
        if translate_protein(rna_snip) == peptide:
            results.append(get_reverse_complement(reverse_transcribe_rna(rna_snip)))

    return results


"""
    Generating Theoretical Spectrum Problem: Generate the theoretical spectrum of a cyclic peptide.
     Input: An amino acid string Peptide.
     Output: Cyclospectrum(Peptide).
"""
def cyclospectrum_v1(peptide):
    amino_acid_mass_table = _get_amino_acid_mass_table()
    return _cyclospectrum(amino_acid_mass_table, peptide)


def _cyclospectrum(amino_acid_mass_table, peptide):
    sub_peptides = [['',0]]
    for l in range(len(peptide))[1:]:
        for pos in range(len(peptide)):
            sub_peptide = peptide[pos:pos+l] if pos+l<=len(peptide) else peptide[pos:]+peptide[:pos+l-len(peptide)]
            sub_peptides.append([sub_peptide,0])
    if (peptide):
        sub_peptides.append([peptide,0])

    for entry in sub_peptides:
        entry[1] = _get_peptide_mass(amino_acid_mass_table, entry[0])
    return sorted(sub_peptides, key=lambda entry: entry[1])

amino_acid_mass_table = {'G':57,'A':71,'S':87,'P':97,'V':99,'T':101,'C':103,'I':113,'L':113,'N':114,'D':115,'K':128,'Q':128,'E':129,'M':131,'H':137,'F':147,'R':156,'Y':163,'W':186}
def cyclospectrum(peptide):
    prefix_mass = [0]
    for i in range(len(peptide)):
        prefix_mass.append(prefix_mass[i]+amino_acid_mass_table[peptide[i]])

    theoretical_spectrum = [0]
    for i in range(len(prefix_mass)-1):
        for j in range(i+1, len(prefix_mass)):
            theoretical_spectrum.append(prefix_mass[j]-prefix_mass[i])
            if i > 0 and j < len(prefix_mass)-1:
                theoretical_spectrum.append(prefix_mass[-1] - (prefix_mass[j] - prefix_mass[i]))
    return sorted(theoretical_spectrum)

def test_cyclospectrum_dynamic_programming(peptide):
    import re
    prefix_mass = []
    for i in range(len(peptide)):
        prefix_mass.append(peptide[:i])

    theoretical_spectrum = []
    for i in range(len(prefix_mass)-1):
        for j in range(i+1, len(prefix_mass)):
            sub = re.sub(prefix_mass[i], '', prefix_mass[j])
            theoretical_spectrum.append(sub)
            #if i+j>len(prefix_mass):
            #    theoretical_spectrum.append(prefix_mass[j]-prefix_mass[i]+prefix_mass[j-i+1])
            if i > 0 and j < len(prefix_mass)-1:
                theoretical_spectrum.append(re.sub(sub, '', prefix_mass[-1]))
    print(theoretical_spectrum)


def linearspectrum(peptide):
    amino_acid_mass_table = _get_amino_acid_mass_table()
    sub_peptides = [['',0]]
    for l in range(len(peptide))[1:]:
        for pos in range(len(peptide)):
            if pos + l <= len(peptide):
                sub_peptide = peptide[pos:pos+l]
                sub_peptides.append([sub_peptide,0])
    if (peptide):
        sub_peptides.append([peptide,0])

    for entry in sub_peptides:
        entry[1] = _get_peptide_mass(amino_acid_mass_table, entry[0])
    return sorted(sub_peptides, key=lambda entry: entry[1])

def _get_peptide_mass(amino_acid_mass_table, peptide):
    mass = 0
    for pos in range(len(peptide)):
        mass += amino_acid_mass_table[peptide[pos]]
    return mass



"""
    Counting Peptides with Given Mass Problem: Compute the number of peptides of given mass. 
    (weight combinations rather than amino acid combinations)
     Input: An integer m.
     Output: The number of linear peptides having integer mass m.
"""
def count_peptide_with_given_mass(mass):
    amino_acid_mass_table = _get_amino_acid_mass_table()
    return _count_sub_peptide_with_given_mass(amino_acid_mass_table, mass)


def _count_sub_peptide_with_given_mass(amino_acid_mass_table, m):
    """
    sum = 0
    for amino_acid in amino_acid_mass_table.keys():
        amino_acid_mass = amino_acid_mass_table[amino_acid]
        if mass == amino_acid_mass:
            sum += 1
        elif mass > amino_acid_mass:
            sum += _count_sub_peptide_with_given_mass(amino_acid_mass_table, mass - amino_acid_mass)
    return sum
    """
    masses = [0] * (m+1)
    masses[0] = 1
    for i in range(m+1):
        for j in range(len(AMINO_ACID_MASSES)):
            if i >= AMINO_ACID_MASSES[j]:
                masses[i] += masses[i-AMINO_ACID_MASSES[j]]
    return masses[m]

def AreStringListsEqual(expected, result):
    if len(expected) != len(result):
        _print_list_difference(expected, result)
        return False
    for val in expected:
        if (val not in result) or expected.count(val) != result.count(val):
            _print_list_difference(expected, result)
            return False
    return True


def _print_list_difference(expected, result):
    print("Expected: " + str(len(expected)) + ", " + ' '.join(expected) + "\n")
    print("Result:   " + str(len(result)) + ", " + ' '.join(result) + "\n")


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []


def get_reverse_complement(dna):
    dna = str.upper(dna)
    complement = ''
    for base in dna:
        if base == 'A':
            complement += 'T'
        elif base == 'T':
            complement += 'A'
        elif base == 'C':
            complement += 'G'
        elif base == 'G':
            complement += 'C'
        else:
            raise Exception('Invalid DNA base.')
    return complement[::-1]


def transcribe_dna(dna):
    return dna.replace('T', 'U')

def reverse_transcribe_rna(rna):
    return rna.replace('U', 'T')
def _count_sequence_of_sub_peptide_with_given_mass_by_brutal_force(amino_acid_mass_table, m):
    sum = 0
    for amino_acid in amino_acid_mass_table.keys():
        amino_acid_mass = amino_acid_mass_table[amino_acid]
        if m == amino_acid_mass:
            sum += 1
#        elif m > amino_acid_mass:
#            sum += _count_sub_peptide_with_given_mass(amino_acid_mass_table, mass - amino_acid_mass)
    return sum


"""
    CyclopeptideSequencing(Spectrum)
        Peptides ← a set containing only the empty peptide
        while Peptides is nonempty
            Peptides ← Expand(Peptides)
            for each peptide Peptide in Peptides
                if Mass(Peptide) = ParentMass(Spectrum)
                    if Cyclospectrum(Peptide) = Spectrum
                        output Peptide
                    remove Peptide from Peptides
                else if Peptide is not consistent with Spectrum
                    remove Peptide from Peptides
    - Cyclospectrum(Peptide): https://stepik.org/lesson/Sequencing-Antibiotics-by-Shattering-Them-into-Pieces-98/step/4?course=Stepic-Interactive-Text-for-Week-3&unit=8263
    - Mass(Peptide): the total mass of an amino acid string Peptide
    - ParentMass(Spectrum): equal to the largest mass in Spectrum
"""
def cyclopeptide_sequencing_v1(spectrum):
    spectrum = [int(amino) for amino in spectrum.split(' ')]
    sequences = []
    candidates = ['']
    amino_acid_mass_table = _get_amino_acid_mass_table()
    spectrum_set = set(spectrum)
    while candidates:
        peptides = _expand(candidates, amino_acid_mass_table)
        candidates = list(peptides)
        for peptide in peptides:
            mass = _get_peptide_mass(amino_acid_mass_table, peptide)
            parent_mass = spectrum[-1]
            cs = [entry[1] for entry in cyclospectrum(peptide)]
            if mass == parent_mass:
                if cs == spectrum:
                    sequences.append([amino_acid_mass_table[amino_acid] for amino_acid in peptide])
                candidates.remove(peptide)
            elif cs[-1] > spectrum[-1] or not set(cs).issubset(spectrum_set):
                candidates.remove(peptide)
    return sequences


def _expand(peptides, amino_acid_mass_table):
    return [peptide + amino_acid for amino_acid in amino_acid_mass_table.keys() for peptide in peptides]


"""
Version 2 of cyclopeptide_sequencing which iterates amino acid mass list instead of amino acid list
"""
def cyclopeptide_sequencing(spectrum):
    spectrum = [int(amino) for amino in spectrum.split(' ')]
    sequences = []
    candidate_peptides = [[]]
    spectrum_set = set(spectrum)
    while candidate_peptides:
        #peptides = [peptide.append(aa_mass) for aa_mass in AMINO_ACID_MASSES for peptide in candidate_peptides]
        peptides = []
        for peptide in candidate_peptides:
            for aa_mass in AMINO_ACID_MASSES:
                if aa_mass not in spectrum_set:
                    continue
                candidate = list(peptide)
                candidate.append(aa_mass)
                peptides.append(candidate)
        candidate_peptides = list(peptides)
        for peptide in peptides:
            if not peptide:
                candidate_peptides.remove(peptide)
            mass = sum(peptide)
            parent_mass = spectrum[-1]
            if mass == parent_mass:
                cs = _cyclospectrum_mass(peptide)
                if cs == spectrum:
                    sequences.append(peptide)
                candidate_peptides.remove(peptide)
            else:
                #TODO: should use linearspectrum() here
                cs = _cyclospectrum_mass(peptide)
                if cs[-1] > spectrum[-1]:
                    candidate_peptides.remove(peptide)
                else:
                    cs_set = set(cs)
                    if (not cs_set.issubset(spectrum_set)):
                        candidate_peptides.remove(peptide)
    return sequences

def _cyclospectrum_mass(peptide):
    spectrum = [0]
    for l in range(len(peptide))[1:]: #exclude length 0
        for pos in range(len(peptide)):
            sub_peptide = peptide[pos:pos+l] if pos+l<=len(peptide) else peptide[pos:]+peptide[:pos+l-len(peptide)]
            spectrum.append(sum(sub_peptide))
            #if pos + l <= len(peptide):
            #    sub_peptide = peptide[pos:pos + l]
            #    spectrum.append(sum(sub_peptide))
    if (peptide):
        spectrum.append(sum(peptide))
    return sorted(spectrum)

def _count_sub_peptide_with_given_mass(amino_acid_mass_table, m):
    '''
    sum = 0
    for amino_acid in amino_acid_mass_table.keys():
        amino_acid_mass = amino_acid_mass_table[amino_acid]
        if mass == amino_acid_mass:
            sum += 1
        elif mass > amino_acid_mass:
            sum += _count_sub_peptide_with_given_mass(amino_acid_mass_table, mass - amino_acid_mass)
    return sum
    '''
    masses = [0] * (m+1)
    masses[0] = 1
    for i in range(m+1):
        for j in range(len(AMINO_ACID_MASSES)):
            if i >= AMINO_ACID_MASSES[j]:
                masses[i] += masses[i-AMINO_ACID_MASSES[j]]
    return masses[m]


def _count_sequence_of_sub_peptide_with_given_mass_by_brutal_force(amino_acid_mass_table, m):
    sum = 0
    for amino_acid in amino_acid_mass_table.keys():
        amino_acid_mass = amino_acid_mass_table[amino_acid]
        if m == amino_acid_mass:
            sum += 1
#        elif m > amino_acid_mass:
#            sum += _count_sub_peptide_with_given_mass(amino_acid_mass_table, mass - amino_acid_mass)
    return sum


"""
    CyclopeptideSequencing(Spectrum)
        Peptides ← a set containing only the empty peptide
        while Peptides is nonempty
            Peptides ← Expand(Peptides)
            for each peptide Peptide in Peptides
                if Mass(Peptide) = ParentMass(Spectrum)
                    if Cyclospectrum(Peptide) = Spectrum
                        output Peptide
                    remove Peptide from Peptides
                else if Peptide is not consistent with Spectrum
                    remove Peptide from Peptides
    - Cyclospectrum(Peptide): https://stepik.org/lesson/Sequencing-Antibiotics-by-Shattering-Them-into-Pieces-98/step/4?course=Stepic-Interactive-Text-for-Week-3&unit=8263
    - Mass(Peptide): the total mass of an amino acid string Peptide
    - ParentMass(Spectrum): equal to the largest mass in Spectrum
"""
def cyclopeptide_sequencing_v1(spectrum):
    spectrum = [int(amino) for amino in spectrum.split(' ')]
    sequences = []
    candidates = ['']
    amino_acid_mass_table = _get_amino_acid_mass_table()
    spectrum_set = set(spectrum)
    while candidates:
        peptides = _expand(candidates, amino_acid_mass_table)
        candidates = list(peptides)
        for peptide in peptides:
            mass = _get_peptide_mass(amino_acid_mass_table, peptide)
            parent_mass = spectrum[-1]
            cs = [entry[1] for entry in cyclospectrum(peptide)]
            if mass == parent_mass:
                if cs == spectrum:
                    sequences.append([amino_acid_mass_table[amino_acid] for amino_acid in peptide])
                candidates.remove(peptide)
            elif cs[-1] > spectrum[-1] or not set(cs).issubset(spectrum_set):
                candidates.remove(peptide)
    return sequences


def _expand(peptides, amino_acid_mass_table):
    return [peptide + amino_acid for amino_acid in amino_acid_mass_table.keys() for peptide in peptides]


"""
Version 2 of cyclopeptide_sequencing which iterates amino acid mass list instead of amino acid list
"""
def cyclopeptide_sequencing(spectrum):
    spectrum = [int(amino) for amino in spectrum.split(' ')]
    sequences = []
    candidate_peptides = [[]]
    spectrum_set = set(spectrum)
    while candidate_peptides:
        #peptides = [peptide.append(aa_mass) for aa_mass in AMINO_ACID_MASSES for peptide in candidate_peptides]
        peptides = []
        for peptide in candidate_peptides:
            for aa_mass in AMINO_ACID_MASSES:
                if aa_mass not in spectrum_set:
                    continue
                candidate = list(peptide)
                candidate.append(aa_mass)
                peptides.append(candidate)
        candidate_peptides = list(peptides)
        for peptide in peptides:
            if not peptide:
                candidate_peptides.remove(peptide)
            mass = sum(peptide)
            parent_mass = spectrum[-1]
            if mass == parent_mass:
                cs = _cyclospectrum_mass(peptide)
                if cs == spectrum:
                    sequences.append(peptide)
                candidate_peptides.remove(peptide)
            else:
                #TODO: should use linearspectrum() here
                cs = _cyclospectrum_mass(peptide)
                if cs[-1] > spectrum[-1]:
                    candidate_peptides.remove(peptide)
                else:
                    cs_set = set(cs)
                    if (not cs_set.issubset(spectrum_set)):
                        candidate_peptides.remove(peptide)
    return sequences

def _cyclospectrum_mass(peptide):
    spectrum = [0]
    for l in range(len(peptide))[1:]: #exclude length 0
        for pos in range(len(peptide)):
            sub_peptide = peptide[pos:pos+l] if pos+l<=len(peptide) else peptide[pos:]+peptide[:pos+l-len(peptide)]
            spectrum.append(sum(sub_peptide))
            #if pos + l <= len(peptide):
            #    sub_peptide = peptide[pos:pos + l]
            #    spectrum.append(sum(sub_peptide))
    if (peptide):
        spectrum.append(sum(peptide))
    return sorted(spectrum)


def protein_translation_problem():
    with open('quiz.txt', 'r') as datafile:
        rna = datafile.readline().strip()
    print(translate_protein(rna))


def peptide_encoding_problem():
    with open('quiz.txt', 'r') as datafile:
        dna = datafile.readline().strip()
        peptide = datafile.readline().strip()
    print('\n'.join(find_peptide_encoding(dna, peptide)))


def theoretical_spectrum_problem():
    with open('quiz.txt', 'r') as datafile:
        peptide = datafile.readline().strip()
    print(' '.join([str(entry[1]) for entry in cyclospectrum(peptide)]))


def count_peptide_with_given_mass_problem():
    print(count_peptide_with_given_mass(1360))


def cyclopeptide_sequencing_problem():
    #spectrum = "0 71 97 99 103 113 113 114 115 131 137 196 200 202 208 214 226 227 228 240 245 299 311 311 316 327 337 339 340 341 358 408 414 424 429 436 440 442 453 455 471 507 527 537 539 542 551 554 556 566 586 622 638 640 651 653 657 664 669 679 685 735 752 753 754 756 766 777 782 782 794 848 853 865 866 867 879 885 891 893 897 956 962 978 979 980 980 990 994 996 1022 1093"
    spectrum = "0 101 103 113 113 113 114 114 114 131 186 204 215 217 227 227 227 244 245 299 299 318 318 328 330 341 358 358 412 413 430 431 431 432 444 471 472 514 526 543 544 545 545 545 575 585 617 627 657 657 657 658 659 676 688 730 731 758 770 771 771 772 789 790 844 844 861 872 874 884 884 903 903 957 958 975 975 975 985 987 998 1016 1071 1088 1088 1088 1089 1089 1089 1099 1101 1202"
    sequences = cyclopeptide_sequencing_v1(spectrum)
    sequence_strings = ['-'.join(map(str, sequence)) for sequence in sequences]
    print(' '.join(sequence_strings))

# protein_translation_problem()
# peptide_encoding_problem()
# theoretical_spectrum_problem()
# count_peptide_with_given_mass_problem()
#cyclopeptide_sequencing_problem()


def quiz1():
    print("\n\n----- Quiz 1 -----")
    print("\nTyrocidine B1 is synthesized by NRP synthetase. ~~~~ True. ~~~~ 100%")
    print("Tyrocidine B1 is synthesized by the ribosome. ~~~~ False. ~~~~ 100%\n")

def quiz2():
    print("----- Quiz 2 -----")
    print("100%")
    rnas = ["CCAAGUACAGAGAUUAAC", "CCGAGGACCGAAAUCAAC", "CCAAGAACAGAUAUCAAU", "CCUCGUACAGAAAUCAAC"]
    for rna in rnas:
        if translate_protein(rna) == "PRTEIN":
            print(str(rnas.index(rna)+1))


def quiz3():
    print("\n----- Quiz 3 -----")
    print("How many DNA strings transcribe and translate into the amino acid string LEADER?")
    rnas = permutations(['A','C','G','U'], 5)
    print(len([rna for rna in rnas if translate_protein(rna) == 'LEADER']))
    print("The answer isn't 0.")

    print(6*2*4*2*2*6, "Is the correct answer.\n")  # LEADER
    #print(1*4*6*6)  # MASS


def quiz4():
    print("----- Quiz 4 -----")
    print("What is the integer mass of tryptophan?")
    print("186.2 Isn't the answer.")
    print("What is the integer mass of glycine?")
    table = _get_amino_acid_mass_table()
    print(sum([table[amino_acid] for amino_acid in "GLY"]))
    print("Wrong. (333) ")


def quiz5():
    print("----- Quiz 5 -----")
    print("Which of the following cyclic peptides could have generated the theoretical spectrum")
    print("Use the code below to get the correct answer.")
    print("Theoretical Spectrum Problem")
    #peptides = ["IAMT", "TAIM", "ALTM", "MIAT", "TMLA", "MTAI"]
    #for peptide in peptides:
    #    spectrum = [str(item[1]) for item in cyclospectrum(peptide)]
    #    if ' '.join(spectrum) == "0 71 101 113 131 184 202 214 232 285 303 315 345 416":
    #        print(str(peptides.index(peptide)+1))





def quiz6():
    print("----- Quiz 6 -----")
    print("Incorrect.")
    print("Which of the following linear peptides is consistent with Spectrum = ")
    #peptides = ["TCE", "AQV", "VAQ", "ETC", "CTV", "CET"]
    peptides = ["ETC", "CTV", "CTQ", "AQV", "QCV", "TCE"]
    spectrum_set = set("0 71 99 101 103 128 129 199 200 204 227 230 231 298 303 328 330 332 333".split(' '))
    for peptide in peptides:
        sub_spectrum = [str(item[1]) for item in linearspectrum(peptide)]
        if set(sub_spectrum).issubset(spectrum_set):
            print(str(peptides.index(peptide)+1))

# 0 71 99 101 103 128 129 199 200 204 227 230 231 298 303 328 330 332 333

## 0 101 103 129 204 230 333    ETC
## 0 99 101 103 200 204 303     CTV
# 0 101 103 128 204 229 332    CTQ
## 0 71 99 128 199 227 298      AQV
# 0 99 103 128 202 231 330     QCV
# 0 101 103 129 204 232 333    TCE




quiz1()
quiz2()
quiz3()
quiz4()
quiz5()
quiz6()
