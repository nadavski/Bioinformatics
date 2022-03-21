import math

def HammingDistance(string_1, string_2):
    res = 0
    for val_1, val_2 in zip(string_1, string_2):
        if val_1 != val_2:
            res += 1
    return res

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