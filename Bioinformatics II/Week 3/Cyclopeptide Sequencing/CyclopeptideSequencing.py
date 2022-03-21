import sys

def cycloPeptideSequencing(spectrum):
	'''only consider those Spectrum that appear in the spectrum'''
	TheoSpectrum = [128, 129, 131, 147, 101, 103, 137, 71, 99, 113, 114, 115, 97, 163, 87, 57, 186, 156]
	Spectrum = []
	for spec in TheoSpectrum:
		if spec in spectrum:
			Spectrum.append(spec)
	'''initialize'''
	peptides = [[0]]
	parentMass = max(spectrum)
	ret = []
	while len(peptides) != 0:
		''' expand the peptide '''
		newpeptides = []
		for peptide in peptides:
			for s in Spectrum:
				newpeptide = peptide + [s]
				if sum(newpeptide) == parentMass:
					if cyclicSpectrum(newpeptide[1:]) == spectrum:
						ret.append(newpeptide[1:])
				elif notconsistent(newpeptide,spectrum):
					continue
				else:
					newpeptides.append(newpeptide)
		peptides = newpeptides
	return ret

def notconsistent(peptide,specturm):
	''' every mass in its theoretical_spectrum must be contained in Spectrum'''
	if len([i for i,p in enumerate(peptide) if p not in spectrum]) > 0:
		return 1
	for p in peptide:
		if peptide.count(p) > spectrum.count(p):
			return 1
	''' for now we can only consider the linear spectrum'''
	theo = linearSpectrum(peptide[1:])
	for p in theo:
		if theo.count(p) > spectrum.count(p):
			return 1
	return 0

def linearSpectrum(peptide):
	prefixMass = [0]*(len(peptide)+1)
	for i in range(len(peptide)):
		prefixMass[i+1] = prefixMass[i] + peptide[i]
	linearSpec = [0]
	for i in range(len(peptide)):
		for j in range(i+1,len(peptide)+1):
			linearSpec.append(prefixMass[j]-prefixMass[i])
	return sorted(linearSpec)

def cyclicSpectrum(peptide):
	prefixMass = [0]*(len(peptide)+1)
	for i in range(len(peptide)):
		prefixMass[i+1] = prefixMass[i] + peptide[i]
	peptideMass = prefixMass[-1]
	cyclicSpec = [0]
	for i in range(len(peptide)):
		for j in range(i+1,len(peptide)+1):
			cyclicSpec.append(prefixMass[j]-prefixMass[i])
			if i > 0 and j < len(peptide):
				cyclicSpec.append(peptideMass - prefixMass[j] + prefixMass[i]) #<--SUPER SMART
	return sorted(cyclicSpec)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		spectrum = [0,87,87,115,115,128,129,131,131,163,163,186,202,218,246,246,250,257,259,273,278,292,333,333,346,349,361,379,388,409,420,436,436,448,461,464,464,475,507,524,551,551,565,579,590,592,595,599,611,638,638,682,693,707,710,714,721,725,728,742,753,797,797,824,836,840,843,845,856,870,884,884,911,928,960,971,971,974,987,999,999,1015,1026,1047,1056,1074,1086,1089,1102,1102,1143,1157,1162,1176,1178,1185,1189,1189,1217,1233,1249,1272,1272,1304,1304,1306,1307,1320,1320,1348,1348,1435]
	else:
		filename = sys.argv[1]
		with open(filename) as f:
			lines = f.read().splitlines()
		spectrum = map(int,lines[0].split(' '))
		
	peptides = cycloPeptideSequencing(spectrum)
	ret = []
	for pep in sorted(peptides):
		ret.append('-'.join(map(str,pep)))
	print(' '.join(ret))