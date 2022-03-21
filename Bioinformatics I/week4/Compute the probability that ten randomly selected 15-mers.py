# Compute the probability that ten randomly selected 15-mers
# from the ten 600-nucleotide long strings in the Subtle Motif
# Problem capture at least one implanted 15-mer. 
# (Allowable error: 0.000001)
from functools import reduce

num_kmers = 600 - 15 + 1

prob_of_one = 1 / num_kmers

def probReducer(acc, curr):
    newProb = 1 / (num_kmers - curr)
    return acc + newProb

prob = reduce(probReducer, range(1,11), prob_of_one)

print(prob)