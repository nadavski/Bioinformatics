#STDIN


import sys


f = open('dataset.txt', 'r')
file_name = f.read()


lines = file_name.splitlines() 
Pattern = lines[0]
Dna = lines[1].split(" ")


def distanceBetweenPatternAndStrings(Pattern, Dna): #distanceBetweenPatternAndStrings(Pattern, Dna)
    k = len(Pattern) #k ← |Pattern|
    Distance = 0 #distance ← 0
    for string in  Dna: 
        hammingDistance = float("inf") #HammingDistance ← ∞
        for i in range(0, len(string)-k+1): 
            if hammingDistance > HammingDistance(Pattern, string[i:i+k]): #if HammingDistance > HammingDistance(Pattern, Pattern’)
                hammingDistance = HammingDistance(Pattern, string[i:i+k]) #HammingDistance ← HammingDistance(Pattern, Pattern’)
        Distance = Distance + hammingDistance#distance ← distance + HammingDistance
    return Distance



def HammingDistance(p, q):
    count = 0
    for i in range(len(p)):
        if p[i] != q[i]:
            count += 1
    return count



print (distanceBetweenPatternAndStrings(Pattern, Dna))
