def LinearSpectrum(Peptide, Aminoacid, AminoAcidMass):
    PrefixMass=[0]*(len(Peptide))
    for i  in range(0,len(Peptide)):
        for j in range(0,20):
            if Aminoacid[j] == Peptide[i]:
                PrefixMass[i]=PrefixMass[i-1] + AminoAcidMass[Aminoacid[j]]
    null=[0]
    null.extend(PrefixMass)
    PrefixMass=null
    LinearSpectrum = [0]
    for i in range(0,len(PrefixMass)-1): 
        for j in range(i + 1, len(PrefixMass)):
            LinearSpectrum.append(PrefixMass[j]-PrefixMass[i])
    LinearSpectrum.sort()
    return LinearSpectrum
Aminoacid = ['G', 'A', 'S', 'P', 'V', 'T', 'C', 'I', 'L', 'N', 'D', 'K', 'Q', 'E', 'M', 'H', 'F', 'R', 'Y', 'W']
aminoacid = ['G', 'A', 'S', 'P', 'V', 'T', 'C', 'I', 'N', 'D', 'K', 'E', 'M', 'H', 'F', 'R', 'Y', 'W']
aminoAcidMass = {
    'G': 57,
    'A': 71,
    'S': 87,
    'P': 97,
    'V': 99,
    'T': 101,
    'C': 103,
    'I': 113,
    'L': 113,
    'N': 114,
    'D': 115,
    'K': 128,
    'Q': 128,
    'E': 129,
    'M': 131,
    'H': 137,
    'F': 147,
    'R': 156,
    'Y': 163,
    'W': 186
}
revamino={
    57:'G',
    71:'A',
    87:'S',
    97:'P',
    99:'V',
    101:'T',
    103:'C',
    113:'I',
    114:'N',
    115:'D',
    128:'K',
    129:'E',
    131:'M',
    137:'H',
    147:'F',
    156:'R',
    163:'Y',
    186:'W'
}

def cyclopeptide(peptide):
    A=LinearSpectrum(peptide[1:],Aminoacid,aminoAcidMass)
    peptidemass=(LinearSpectrum(peptide,Aminoacid,aminoAcidMass)[-1])
    diffspec=[]
    for i in A:
        diffspec.append(peptidemass-i)
    A.extend(diffspec)
    A.sort()
    return(A)

def PeptideScore(peptide,spectrum):
    if len(peptide)>0:
        pepSpec = cyclopeptide(peptide)
        score = 0
        for m in set(spectrum):
            score += min(pepSpec.count(int(m)),spectrum.count(str(m)))
        return score
    else:
        return 0

def linearScore(peptide,spectrum):
    pepSpec = LinearSpectrum(peptide,Aminoacid,aminoAcidMass)
    score = 0
    for m in set(spectrum):
        score += min(pepSpec.count(int(m)),spectrum.count(str(m)))
    return score

def scores(elem):
    return elem[1]


def Trim(Leaderboard, Spectrum, N, Alphabet, AminoAcidMass):
    N=N-1
    linearScores=[0]*len(Leaderboard)
    for j in range(0,len(Leaderboard)): 
        Peptide =  Leaderboard[j]
        linearScores[j] = linearScore(Peptide, Spectrum)
    for i in range(0,len(Leaderboard)):
        Leaderboard[i]=[Leaderboard[i],linearScores[i]]
    Leaderboard.sort(key=scores,reverse=True) 
    linearScores.sort(reverse=True)
    for j in range(N+1,len(Leaderboard)): 
        if linearScores[j] < linearScores[N]:
            Leaderboard=Leaderboard[:j]
            return Leaderboard
    return Leaderboard

def first(Leaderboard):
    leaderboard=[0]*len(Leaderboard)
    for i in range(0,len(Leaderboard)):
        leaderboard[i]=Leaderboard[i][0]
    return leaderboard

#print(first(Trim())
def expand(candidatePeptides,Spectrum,aminoAcidMass,Aminoacid,amin):
    canpep=[]
    Bnew=[]
    for i in Spectrum:
        Bnew.append(int(i)) 
    for i in candidatePeptides:
        for j in amin:
            canpep.append(str(i)+j)
    return canpep

def Mass(peptide):
    listed=[]
    for i in peptide:
        listed.append(aminoAcidMass[i])
    return sum(listed)

def consistent(peptide,Spectrum):
    spec=LinearSpectrum(peptide,Aminoacid,aminoAcidMass)
    Bnew=[]
    for i in Spectrum:
        Bnew.append(int(i)) 
    spectrum=set(spec)
    for l in spectrum:
        if spec.count(int(l)) <= Bnew.count(int(l)):
            pass
        else:
            return False
    return True

def singlepep(Spectrum):
    peptides=[]
    for i in aminoAcidMass:
        if Spectrum.count(str(aminoAcidMass[i]))>0:
            peptides.append(i)
    return peptides

def equal(A,B):
    Bnew=[]
    for i in B:
        Bnew.append(int(i)) 
    A1=set(A)
    Bnew1=set(Bnew)
    if A1==Bnew1:
        return True
    else:
        return False

import math
def CyclopeptideSequencing(Spectrum):
    Spectrum=Spectrum.split(' ')
    CandidatePeptides=singlepep(Spectrum)
    amin=convolution(Spectrum,14)
    FinalPeptides = []
    n=0
    while n < ((1+math.sqrt(1+4*(len(Spectrum)*(len(Spectrum)-1)-2)))/2)-1:
        CandidatePeptides = expand(CandidatePeptides,Spectrum,aminoAcidMass,Aminoacid,amin)
        temppep=CandidatePeptides[:]
        for i in temppep: 
            if int(Mass(i)) == int(Spectrum[-1]):
                if equal(cyclopeptide(i),Spectrum) :
                    if i in FinalPeptides:
                        pass
                    else:                     
                        FinalPeptides.append(i)
                CandidatePeptides.remove(i) 
            else: 
                peptide=i
                if  consistent(peptide,Spectrum)==True:
                    pass
                else:
                    CandidatePeptides.remove(peptide)
        n=n+1
    Ultpep=[]
    for i in FinalPeptides:
        Finalepeptides=[]
        for j in i:
            Finalepeptides.append(str(aminoAcidMass[j]))
        Ultpep.append('-'.join(Finalepeptides))          
    return Ultpep 

aminoacidMass = {
    'G': 57,
    'A': 71,
    'S': 87,
    'P': 97,
    'V': 99,
    'T': 101,
    'C': 103,
    'I': 113,
    'N': 114,
    'D': 115,
    'K': 128,
    'E': 129,
    'M': 131,
    'H': 137,
    'F': 147,
    'R': 156,
    'Y': 163,
    'W': 186
}
def scoress(Leaderboard,Spectrum, Alphabet, AminoAcidMass):
    linearScores=[0]*len(Leaderboard)
    for j in range(0,len(Leaderboard)): 
        Peptide =  Leaderboard[j]
        linearScores[j] = linearScore(Peptide, Spectrum)
    Leaderboardi=[0]*len(Leaderboard)
    for i in range(0,len(Leaderboard)):
        Leaderboardi[i]=[Leaderboard[i],linearScores[i]]
    Leaderboardi.sort(key=scores,reverse=True) 
    return Leaderboardi

def convolution(Spectrum,M):
    Spectrum = [int(i) for i in Spectrum]
    Spectrum.sort()
    List=[]
    for i in range(0,len(Spectrum)-1):
        for j in range (i+1,len(Spectrum)):
            List.append(int(Spectrum[j])-int(Spectrum[i]))
    List = [i for i in List if i != 0]
    List.sort()
    Times=[0]*143
    List1=list(set(List))
    for j in range(0,len(List1)):
        i=List1[j]
        if i>57 and i<200:
            if i in aminoacidMass.values():
                Times[j]=[i,List.count(i)]
    Times = [i for i in Times if i != 0]
    Times.sort(key=scores,reverse=True)
    Times=Times[:M]
    Times=first(Times)
    Timesone=Times
    for i in range(0,len(Times)):
        Timesone[i]=revamino[Times[i]]
    return Timesone
    
def LeaderboardCyclopeptideSequencing(Spectrum, N):
    Spectrum=Spectrum.split(' ')
    Leaderboard=singlepep(Spectrum)
    LeaderPeptide=''
    Score=0
    n=0
    k=0
    amin=convolution(Spectrum,14)
    while len(Leaderboard)>0:
        if k>5:
            N=100
        Leaderboard = expand(Leaderboard,Spectrum,aminoAcidMass,Aminoacid,amin)
        if n==0:
            Leaderboards=scoress(Leaderboard,Spectrum,Aminoacid,aminoAcidMass)
        n=1
        temppep=Leaderboards[:]
        print(Leaderboard)
        for i in range(0,len(temppep)):
            Peptide=temppep[i][0]
            if Mass(Peptide) == int(Spectrum[-1]):
                if temppep[i][1] > Score:
                    LeaderPeptide = Peptide
                    Score=temppep[i][1]
            else:
                if Mass(Peptide) > int(Spectrum[-1]):
                    Leaderboard.remove(Peptide)
        Leaderboards = Trim(Leaderboard, Spectrum, N,Aminoacid,aminoAcidMass)
        Leaderboard= first(Leaderboard)
        k=k+1   
    Ultpep=[]
    for i in LeaderPeptide:
        Finalepeptides=[]
        for j in i:
            Finalepeptides.append(str(aminoacidMass[j]))
        Ultpep.append('-'.join(Finalepeptides))          
    return Ultpep 

print(LeaderboardCyclopeptideSequencing('0 71 113 129 147 200 218 260 313 331 347 389 460',100))



