from itertools import product

def generatePatterns(k):
    bases = ['A', 'C', 'G', 'T']
    basesComb = [''.join(base) for base in product(bases, repeat = k)]
    return basesComb

def hammingDistance(str1, str2):
    hamDist = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            hamDist += 1
    return hamDist

def calculateDistance(pattern, dna):
    dist = 0
    for seq in dna:
        allDists = []
        for i in range(len(seq)-len(pattern)+1):
            allDists.append(hammingDistance(seq[i:i+len(pattern)], pattern))
        dist += min(allDists)
    return dist

def medianString(dna, k):
    distance = 999999999.
    median = ''
    allPossibleKmers = generatePatterns(k)
    for pattern in allPossibleKmers:
        if distance > calculateDistance(pattern, dna):
             distance = calculateDistance(pattern, dna)
             median = pattern
    return median


f = open("dataset.txt", "r")
data = f.readlines()
k = 0
lstDNAPatterns = []
for i in range(len(data)):
    line = data[i]
    lineEdit = line
    if line[-1:] == '\n':
        lineEdit = line[:-1]
    if i == 0:
        k = int(lineEdit)
    else:
        lstDNAPatterns.append(lineEdit)
print(medianString(lstDNAPatterns, k))


