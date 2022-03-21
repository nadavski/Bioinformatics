# CODING CHALLENGES
print('CODING CHALLENGES ANSWERS:')


# Code Challenge: Implement RandomizedMotifSearch.
#       Input: Integers k and t, followed by a collection of strings Dna.
#       Output: A collection BestMotifs resulting from running RandomizedMotifSearch(Dna, k, t) 1,000 times.
#       Remember to use pseudocounts!
def FormProfileWithPseudocounts(motifs, k, pseudocount=1.):
    profile = {x: [float(pseudocount)] * k for x in ['A', 'G', 'C', 'T']}
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


def FormMotifs(profile, dna, k):
    return [ProfileMostProbableKmer(string, k, profile) for string in dna]


import random


def RandomizedMotifSearch(dna, k, t):
    random_numbers = random.sample(range(len(dna[0]) - k + 1), t)
    motifs = [string[i: i + k] for i, string in zip(random_numbers, dna)]
    best_motifs = motifs[:]
    while True:
        profile = FormProfileWithPseudocounts(motifs, k)
        motifs = FormMotifs(profile, dna, k)
        if Score(motifs, k) < Score(best_motifs, k):
            best_motifs = motifs[:]
        else:
            return best_motifs


with open('dataset_161_5.txt') as data:
    lines = data.readlines()
    dna = [line.rstrip('\n') for line in lines[1:]]
    k, t = map(int, lines[0].rstrip('\n').split())
    best_motifs = RandomizedMotifSearch(dna, k, t)
    for _ in range(1000):  # 1000 iterations to maximize probability of convergence
        new = RandomizedMotifSearch(dna, k, t)
        if Score(new, k) < Score(best_motifs, k):
            best_motifs = new[:]
    print(
        'RandomizedMotifSearch Implementation -',
        *best_motifs,
        sep='\n'
    )


# Code Challenge: Implement GibbsSampler.
#       Input: Integers k, t, and N, followed by a collection of strings Dna.
#       Output: The strings BestMotifs resulting from running GibbsSampler(Dna, k, t, N) with 20 random starts.
#       Remember to use pseudocounts!
def GibbsSampler(dna, k, t, n):
    random_numbers = random.sample(range(len(dna[0]) - k + 1), t)
    motifs = [string[i: i + k] for i, string in zip(random_numbers, dna)]
    best_motifs = motifs[:]
    for j in range(n):
        i = random.randint(0, t - 1)
        motifs.pop(i)
        profile = FormProfileWithPseudocounts(motifs, k)
        motifs.insert(i, ProfileMostProbableKmer(dna[i], k, profile))
        if Score(motifs, k) < Score(best_motifs, k):
            best_motifs = motifs[:]
    return best_motifs


with open('dataset_163_4.txt') as data:
    lines = data.readlines()
    dna = [line.rstrip('\n') for line in lines[1:]]
    k, t, n = map(int, lines[0].rstrip('\n').split())
    best_motifs = GibbsSampler(dna, k, t, n)
    for _ in range(20):  # 20 iterations
        new = GibbsSampler(dna, k, t, n)
        if Score(new, k) < Score(best_motifs, k):
            best_motifs = new[:]
    print(
        'GibbsSampler Implementation -',
        *best_motifs,
        sep='\n'
    )


# ---------------------------------------------------------------------------------------------------------------------
# QUIZ 4
# Question 1: True or False: RandomizedMotifSearch performs poorly when given a uniform profile matrix.
print('-----------------------------\n'
      'QUIZ 4 ANSWERS:\nQ1 -', 'True')


# Question 2: True or False:
# RandomizedMotifSearch and GibbsSampler are usually run on only one choice of initial k-mers.
print('Q2 -', 'False')


# Question 3: True or False: it is not possible for RandomizedMotifSearch
# to move from a collection of motifs with lower score to a collection of motifs with higher score.
print('Q3 -', 'True')


# Question 4: Which of the following motif-finding algorithms is guaranteed to find an optimum solution?
# In other words, which of the following are not heuristics? (Select all that apply.)
print('Q4 -', 'MedianString')


# Question 5: Assume we are given the following strings Dna:
# TGACGTTC
# TAAGAGTT
# GGACGAAA
# CTGTTCGC
# Then, assume that RandomizedMotifSearch begins by randomly choosing the following 3-mers Motifs of Dna:
# TGA
# GTT
# GAA
# TGT
# What are the 3-mers after one iteration of RandomizedMotifSearch?
# In other words, what are the 3-mers Motifs(Profile(Motifs), Dna)?
# Please enter your answer as four space-separated strings.
profile = FormProfileWithPseudocounts(['TGA', 'GTT', 'GAA', 'TGT'], 3)
dna = ['TGACGTTC', 'TAAGAGTT', 'GGACGAAA', 'CTGTTCGC']
print('Q5 -', *[ProfileMostProbableKmer(string, 3, profile) for string in dna])