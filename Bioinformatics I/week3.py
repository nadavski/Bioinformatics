print('CODING CHALLENGES ANSWERS:')


# Code Challenge: Implement MotifEnumeration.
#       Input: Integers k and d, followed by a collection of strings Dna.
#       Output: All (k, d)-motifs in Dna.
def HammingDistance(string_1, string_2):
    res = 0
    for val_1, val_2 in zip(string_1, string_2):
        if val_1 != val_2:
            res += 1
    return res


def Neighbors(pattern, d):
    nucleotides = {'A', 'C', 'G', 'T'}
    if d == 0:
        return {pattern}
    if len(pattern) == 1:
        return nucleotides
    neighborhood = set()
    suffix_neighbors = Neighbors(pattern[1:], d)
    for string in suffix_neighbors:
        if HammingDistance(string, pattern[1:]) < d:
            neighborhood.update([x + string for x in nucleotides])
        else:
            neighborhood.add(pattern[0] + string)
    return neighborhood


def ApproximatePatternMatching(pattern, text, d):
    positions = set()
    for i in range(len(text) - len(pattern) + 1):
        if HammingDistance(pattern, text[i:i + len(pattern)]) <= d:
            positions.add(i)
    return positions


def MotifEnumeration(dna, k, d):
    patterns = set()
    for i in range(len(dna[0]) - k + 1):
        pattern = dna[0][i: i + k]
        for neighbor in Neighbors(pattern, d):
            if len([string for string in dna if ApproximatePatternMatching(neighbor, string, d)]) == len(dna):
                patterns.add(neighbor)
    # For answer on Stepik
    # return list(patterns)
    return patterns


# Code Challenge: Implement DistanceBetweenPatternAndStrings.
#       Input: A string Pattern followed by a collection of strings Dna.
#       Output: d(Pattern, Dna).
import math


def DistanceBetweenPatternAndStrings(pattern, dna):
    distance = 0
    for string in dna:
        min_dist = math.inf
        for i in range(len(string) - len(pattern) + 1):
            cur_dist = HammingDistance(pattern, string[i: i + len(pattern)])
            if min_dist > cur_dist:
                min_dist = cur_dist
        distance += min_dist
    return distance


# Code Challenge: Implement MedianString.
#       Input: An integer k, followed by a collection of strings Dna.
#       Output: A k-mer Pattern that minimizes d(Pattern, Dna) among all possible choices of k-mers.
#       (If there are multiple such strings Pattern, then you may return any one.)
def NumberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def NumberToPattern(n, k):
    digit_to_letter = {'0': 'A', '1': 'C', '2': 'G', '3': 'T'}
    if k == 1:
        return digit_to_letter[str(n)]
    pattern = ''.join([digit_to_letter[str(digit)] for digit in NumberToBase(n, 4)])
    if len(pattern) == k:
        return pattern
    else:
        return 'A' * (k - len(pattern)) + pattern


def MedianString(dna, k):
    min_dist = math.inf
    median = ''
    for i in range(4 ** k):
        pattern = NumberToPattern(i, k)
        cur_dist = DistanceBetweenPatternAndStrings(pattern, dna)
        if min_dist > cur_dist:
            min_dist = cur_dist
            median = pattern
    return median


# Code Challenge: Solve the Profile-most Probable k-mer Problem.
# Profile-most Probable k-mer Problem: Find a Profile-most probable k-mer in a string.
#       Input: A string Text, an integer k, and a 4 × k matrix Profile (dictionary).
#       Output: A Profile-most probable k-mer in Text.
def ProfileMostProbableKmer(text, k, profile):
    max_prob = 0
    k_mer = text[: k]
    for i in range(len(text) - k + 1):
        pattern = text[i: i + k]
        prob = 1
        for n, symbol in enumerate(pattern):
            prob *= profile[symbol][n]
        if max_prob < prob:
            max_prob = prob
            k_mer = pattern
    return k_mer



# Code Challenge: Implement GreedyMotifSearch.
#       Input: Integers k and t, followed by a collection of strings Dna.
#       Output: A collection of strings BestMotifs resulting from applying GreedyMotifSearch(Dna, k, t). If at any step
#       you find more than one Profile-most probable k-mer in a given string, use the one occurring first.
def FormProfile(motifs, k):
    profile = {x: [0.] * k for x in ['A', 'G', 'C', 'T']}
    div = len(motifs)
    for i in range(k):
        for motif in motifs:
            profile[motif[i]][i] += 1
        for symbol in profile:
            profile[symbol][i] /= div
    return profile


def Score(motifs, k):
    score = 0
    for i in range(k):
        count = {x: 0 for x in ['A', 'G', 'C', 'T']}
        for motif in motifs:
            count[motif[i]] += 1
        score += k - max(count.values())
    return score


def GreedyMotifSearch(dna, k, t):
    best_motifs = [string[: k] for string in dna]
    for i in range(len(dna[0]) - k + 1):
        motifs = [dna[0][i: i + k]]
        for n in range(1, t):
            profile = FormProfile(motifs, k)
            motifs.append(ProfileMostProbableKmer(dna[n], k, profile))
        if Score(motifs, k) < Score(best_motifs, k):
            best_motifs = motifs
    return best_motifs



# Code Challenge: Implement GreedyMotifSearch with pseudocounts.
#       Input: Integers k and t, followed by a collection of strings Dna.
#       Output: A collection of strings BestMotifs resulting from applying GreedyMotifSearch(Dna, k, t)
#       with pseudocounts. If at any step you find more than one Profile-most probable k-mer in a given string,
#       use the one occurring first.
def FormProfileWithPseudocounts(motifs, k, pseudocount):
    profile = {x: [float(pseudocount)] * k for x in ['A', 'G', 'C', 'T']}
    div = len(motifs)
    for i in range(k):
        for motif in motifs:
            profile[motif[i]][i] += 1
        for symbol in profile:
            profile[symbol][i] /= div
    return profile


def GreedyMotifSearchWithPseudocounts(dna, k, t, pseudocount):
    best_motifs = [string[: k] for string in dna]
    for i in range(len(dna[0]) - k + 1):
        motifs = [dna[0][i: i + k]]
        for n in range(1, t):
            profile = FormProfileWithPseudocounts(motifs, k, pseudocount)
            motifs.append(ProfileMostProbableKmer(dna[n], k, profile))
        if Score(motifs, k) < Score(best_motifs, k):
            best_motifs = motifs
    return best_motifs


# ---------------------------------------------------------------------------------------------------------------------
# QUIZ 3
# Question 1: Which type of algorithm selects the most attractive choice at each step?
print('-----------------------------\n'
      'QUIZ 3 ANSWERS:\nQ1 -', 'Greedy algorithm')


# Question 2: True or false: a motif of lowest score with respect to a collection of strings must appear as a substring
# of one of the strings.
print('Q2 -', 'False')


# Question 3: Order the following probability distributions from lowest to highest entropy:
# A: (0.5, 0, 0, 0.5)
# B: (0.25, 0.25, 0.25, 0.25)
# C: (0, 0, 0, 1)
# D: (0.25, 0, 0.5, 0.25)
print('Q3 -', 'C, A, D, B')


# Question 4: Consider the following profile matrix:
# A: 0.4 0.3 0.0 0.1 0.0 0.9
# C: 0.2 0.3 0.0 0.4 0.0 0.1
# G: 0.1 0.3 1.0 0.1 0.5 0.0
# T: 0.3 0.1 0.0 0.4 0.5 0.0
# Which of the following strings is a consensus string for this profile matrix? (Select all that apply.)
print('Q4 -', 'ACGCGA AAGTGA ACGTTA')


# Question 5: Consider the following motif matrix:
# CTCGATGAGTAGGAAAGTAGTTTCACTGGGCGAACCACCCCGGCGCTAATCCTAGTGCCC
# GCAATCCTACCCGAGGCCACATATCAGTAGGAACTAGAACCACCACGGGTGGCTAGTTTC
# GGTGTTGAACCACGGGGTTAGTTTCATCTATTGTAGGAATCGGCTTCAAATCCTACACAG
# Which of the following 7-mers is a median string for this motif matrix? (Select all that apply.)
seven_mers = ['GATGAGT', 'GTAGGAA', 'TCTGAAG', 'TAGTTTC', 'ATAACGG', 'CGTGTAA']
distances = [DistanceBetweenPatternAndStrings(
        x,
        [
            'CTCGATGAGTAGGAAAGTAGTTTCACTGGGCGAACCACCCCGGCGCTAATCCTAGTGCCC',
            'GCAATCCTACCCGAGGCCACATATCAGTAGGAACTAGAACCACCACGGGTGGCTAGTTTC',
            'GGTGTTGAACCACGGGGTTAGTTTCATCTATTGTAGGAATCGGCTTCAAATCCTACACAG'
        ]
    ) for x in seven_mers]
indexes = [i for i, x in enumerate(distances) if x == 0]
print('Q5 -', *[seven_mers[i] for i in indexes])


# Question 5: Consider the following profile matrix Profile:
# A: 0.4 0.3 0.0 0.1 0.0 0.9
# C: 0.2 0.3 0.0 0.4 0.0 0.1
# G: 0.1 0.3 1.0 0.1 0.5 0.0
# T: 0.3 0.1 0.0 0.4 0.5 0.0
print('Q6 -', '0.4 * 0.3 * 1 * 0.4 * 0.5 * 0.1 = {}'.format(round(0.4 * 0.3 * 1 * 0.4 * 0.5 * 0.1, 4)))