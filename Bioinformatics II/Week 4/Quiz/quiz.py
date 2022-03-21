

def total_mass(sub_peptide):
    mass_table = integer_mass()
    total_mass = 0
    for i in sub_peptide:
        total_mass += mass_table[i]
    return total_mass

def integer_mass():
    D = {}
    file = open('integer_mass_table.txt','r')
    L = []
    for line in file.readlines():
        L = line.rstrip().split()
        D[L[0]] = int(L[1])
    return D
mass_table = integer_mass()



def cyclic_spectra(peptide):
    out_spectrum = [0, total_mass(peptide)]
    peptide_2 = peptide + peptide
    for k in range(1, len(peptide)):
        for n in range(len(peptide)):
            subpep = peptide_2[n:n+k]
            out_spectrum.append(total_mass(subpep))
    return sorted(out_spectrum)

spectrum = []
L = []
file = open('quiz3_dataset.txt','r')
L = file.readlines()
peptide = L[0].rstrip()
for item in L[1:]:
    spectrum += item.rstrip().split()
ex_spectrum = [int(x) for x in spectrum]
th_spectrum = cyclic_spectra(peptide)       # For cyclic mass spectrum
count = 0



def quiz1():
    print('\n\n')
    print("----- Quiz 1 -----")
    print("True or False: In practice, we need to account for the charge of a fragment ion when dealing with real spectra. \n\nAnswer: True")
    

def quiz2():
    print("----- Quiz 2 -----")
    print("True or False: When sequencing antibiotics, \nbiologists can safely assume that all amino acids derive from the standard 20 amino acid alphabet. \n\nAnswer: False ")


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

def _expand(peptides):
    return [peptide + amino_acid for amino_acid in amino_acid_mass_table.keys() for peptide in peptides]

def _get_peptide_mass(peptide):
    return sum([amino_acid_mass_table[amino_acid] for amino_acid in peptide])

def _get_parent_mass(spectrum):
    return spectrum[-1]

def linear_spectrum(peptide):
    prefix_mass = [0]
    for i in range(len(peptide)):
        prefix_mass.append(prefix_mass[i]+amino_acid_mass_table[peptide[i]])

    theoretical_spectrum = [0]
    for i in range(len(prefix_mass)-1):
        for j in range(i+1, len(prefix_mass)):
            theoretical_spectrum.append(prefix_mass[j]-prefix_mass[i])
    return sorted(theoretical_spectrum)

def _linear_score_slow(peptide, spectrum):
    theoretical_spectrum = linear_spectrum(peptide)
    all = set(theoretical_spectrum).union(set(spectrum))
    return sum([min(theoretical_spectrum.count(mass), spectrum.count(mass)) for mass in all])

def _linear_score(peptide, spectrum):
    ls = linear_spectrum(peptide)
    cs = spectrum.copy()
    score = 0
    for c in ls:
        if c in cs:
            score += 1
            cs.remove(c)
    return score

def trim(leaderboard, spectrum, n):
    if len(leaderboard) <= n:
        return leaderboard
    sorted_leaderboard = [(peptide, _linear_score(peptide, spectrum)) for peptide in leaderboard]
    sorted_leaderboard = sorted(sorted_leaderboard, key=lambda entry: entry[1], reverse=True)
    trim_pos = n-1
    for trim_pos in range(n-1, len(leaderboard)-1):
        if sorted_leaderboard[trim_pos][1] > sorted_leaderboard[trim_pos+1][1]:
            break
    return [entry[0] for entry in sorted_leaderboard[:trim_pos+1]]

def leaderboard_cyclopeptide_sequencing(spectrum, n):
    leaderboard = ['']
    leader_peptide = ''
    leader_peptide_score = 0
    while leaderboard:
        leaderboard = _expand(leaderboard)
        loop = list(leaderboard)
        for peptide in loop:
            mass = _get_peptide_mass(peptide)
            parent_mass = _get_parent_mass(spectrum)
            if mass == parent_mass:
                score = _linear_score(peptide, spectrum)
                if score > leader_peptide_score:
                    leader_peptide = peptide
                    leader_peptide_score = score
            elif mass > parent_mass:
                leaderboard.remove(peptide)
        leaderboard = trim(leaderboard, spectrum, n)
    return leader_peptide


def leaderboard_cyclopeptide(spectrum, n):
    leader_peptide = leaderboard_cyclopeptide_sequencing(spectrum, n)
    return [amino_acid_mass_table[amino_acid] for amino_acid in leader_peptide]

def spectral_convolution(spectrum):
    spectrum = sorted(spectrum)
    convolution_dict = {}
    for i in range(len(spectrum)-1):
        for j in range(i, len(spectrum)):
            mass = spectrum[j] - spectrum[i]
            if mass == 0: continue
            if mass in convolution_dict:
                convolution_dict[mass] += 1
            else:
                convolution_dict[mass] = 1
    convolution = []
    for mass in convolution_dict.keys():
        for k in range(convolution_dict[mass]):
            convolution.append(mass)
    return convolution

def score(cyclic_peptide, spectrum):
    theoretical_spectrum = cyclospectrum(cyclic_peptide)
    all = set(theoretical_spectrum).union(set(spectrum))
    return sum([min(theoretical_spectrum.count(mass), spectrum.count(mass)) for mass in all])


def print_score(peptide, spectrum_string):
    print(score(peptide, [int(mass) for mass in spectrum_string.split(' ')]))

def quiz3():
    print("------ Quiz 3 ------")
    print(score("MAMA", [int(mass) for mass in "0 71 98 99 131 202 202 202 202 202 299 333 333 333 503".split(' ')]))


def quiz4():
    print("------ Quiz 4 ------")
    print(_linear_score("PEEP", [int(mass) for mass in "0 97 129 129 129 194 226 323 323 355 452".split(' ')]))


def quiz5():
    print("------ Quiz 5 ------")
    print(spectral_convolution([int(mass) for mass in "0 57 118 179 236 240 301".split(' ')]))





quiz1()
quiz2()
quiz3()
quiz4()
quiz5()