from functools import reduce

def profileMostProbableKmer(text, k, profile):
    
    profileCols = []
    for j in range(len(profile[0])):
        col = []
        for i in range(len(profile)):
            col.append(profile[i][j])
        profileCols.append(col)

    maxProb = -1
    maxProbPattern = ''
    for i in range(len(text)-k+1):
        pattern = text[i:i+k]
        probabilities = []
        for j in range(len(pattern)):
            if pattern[j] == 'A':
                probabilities.append(profileCols[j][0])
            elif pattern[j] == 'C':
                probabilities.append(profileCols[j][1])
            elif pattern[j] == 'G':
                probabilities.append(profileCols[j][2])
            elif pattern[j] == 'T':
                probabilities.append(profileCols[j][3])
        prob = reduce((lambda x, y: x * y), probabilities)
        if prob > maxProb:
            maxProb = prob
            maxProbPattern = pattern
        elif maxProb == -1:
            maxProbPattern = pattern
    return maxProbPattern
    
def createProfileMatrix(lstMotifs):
    probMatrix = {'A': [], 'C': [], 'G': [], 'T': []}
    for j in range(len(lstMotifs[0])):
        colNucs = []
        for i in range(len(lstMotifs)):
            colNucs.append(lstMotifs[i][j])
        ANucCount = colNucs.count('A')
        CNucCount = colNucs.count('C')
        GNucCount = colNucs.count('G')
        TNucCount = colNucs.count('T')
        NucCountSum = ANucCount + CNucCount + GNucCount + TNucCount
        ANucProb = ANucCount / NucCountSum
        CNucProb = CNucCount / NucCountSum
        GNucProb = GNucCount / NucCountSum
        TNucProb = TNucCount / NucCountSum
        probMatrix['A'].append(ANucProb)
        probMatrix['C'].append(CNucProb)
        probMatrix['G'].append(GNucProb)
        probMatrix['T'].append(TNucProb)
    return probMatrix

def hammingDistance(str1, str2):
    hamDist = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            hamDist += 1
    return hamDist

def getConsensus(motifs):
    consensus = ''
    for j in range(len(motifs[0])):
        col = []
        for i in range(len(motifs)):
            col.append(motifs[i][j])
        consensus += max(col, key = col.count)
    return consensus
    
def score(motifs):
    consensus = getConsensus(motifs)
    score = 0
    for motif in motifs:
        score += hammingDistance(consensus, motif)
    return score

def greedyMotifSearch(dna, k, t):
    bestMotifs = []
    for seq in dna:
        bestMotifs.append(seq[0:k])
    bestMotifScore = score(bestMotifs)
    for i in range(len(dna[0])-k+1):
        lstMotifs = []
        motif1 = dna[0][i:i+k]
        lstMotifs.append(motif1)
        for j in range(1, t):
            profileMatrix = createProfileMatrix(lstMotifs)
            profileMatrixEdited = []
            profileMatrixEdited.append(profileMatrix['A'])
            profileMatrixEdited.append(profileMatrix['C'])
            profileMatrixEdited.append(profileMatrix['G'])
            profileMatrixEdited.append(profileMatrix['T'])
            motifi = profileMostProbableKmer(dna[j], k, profileMatrixEdited)
            lstMotifs.append(motifi)
        lstMotifsScore = score(lstMotifs)
        if lstMotifsScore < bestMotifScore:
            bestMotifs = lstMotifs
            bestMotifScore = lstMotifsScore
    bestMotifsStr = '\n'.join(bestMotifs)
    return bestMotifsStr

f = open("dataset.txt", "r")
data = f.readlines()
k = 0
t = 0
dnaStrings = []
for i in range(len(data)):
    line = data[i]
    lineEdit = line
    if line[-1:] == '\n':
        lineEdit = line[:-1]
    if i == 0:
        lstVals = lineEdit.split(' ')
        k = int(lstVals[0])
        t = int(lstVals[1])
    else:
        dnaStrings.append(lineEdit)
        
print(greedyMotifSearch(dnaStrings, k, t))