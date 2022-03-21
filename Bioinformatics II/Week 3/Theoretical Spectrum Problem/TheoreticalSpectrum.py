
import sys

MassTable = {'A': 71, 'C': 103, 'E': 129, 'D': 115, 'G': 57, 'F': 147, \
			'I': 113, 'H': 137, 'K': 128, 'M': 131, 'L': 113, 'N': 114, \
			'Q': 128, 'P': 97, 'S': 87, 'R': 156, 'T': 101, 'W': 186, \
			'V': 99, 'Y': 163}

def theoretical_spectrum(peptide):
	k = len(peptide)
	spec = []
	while k > 0:
		for i in range(len(peptide)-k+1):
			subpep = peptide[i:i+k]
			spec.append(sum([MassTable[s] for s in subpep]))
		k -= 1
	spec.append(0)
	return sorted(spec)

def linearSpectrum(peptide):
	prefixMass = [0]*(len(peptide)+1)
	for i in range(len(peptide)):
		prefixMass[i+1] = prefixMass[i] + MassTable[peptide[i]]
	linearSpec = [0]
	for i in range(len(peptide)):
		for j in range(i+1,len(peptide)+1):
			linearSpec.append(prefixMass[j]-prefixMass[i])
	return sorted(linearSpec)

def cyclicSpectrum(peptide):
	prefixMass = [0]*(len(peptide)+1)
	for i in range(len(peptide)):
		prefixMass[i+1] = prefixMass[i] + MassTable[peptide[i]]
	peptideMass = prefixMass[-1]
	cyclicSpec = [0]
	for i in range(len(peptide)):
		for j in range(i+1,len(peptide)+1):
			cyclicSpec.append(prefixMass[j]-prefixMass[i])
			if i > 0 and j < len(peptide):
				cyclicSpec.append(peptideMass - prefixMass[j] + prefixMass[i]) #<--Nice!
	return sorted(cyclicSpec)

if __name__ == '__main__':
	if len(sys.argv) == 2:
		filename = sys.argv[1]
		with open(filename) as f:
			lines = f.read().splitlines()
		peptide = lines[0]
	else:
		peptide = 'NQEL'
	
	spec = linearSpectrum(peptide)
	print('\n\n',' '.join(map(str,spec)))


    #peptides = ["ETC", "CTV", "CTQ", "AQV", "QCV", "TCE"]
    #spectrum_set = set("0 71 99 101 103 128 129 199 200 204 227 230 231 298 303 328 330 332 333".split(' '))


# 0 71 99 101 103 128 129 199 200 204 227 230 231 298 303 328 330 332 333

## 0 101 103 129 204 230 333    ETC
## 0 99 101 103 200 204 303     CTV
# 0 101 103 128 204 229 332    CTQ
## 0 71 99 128 199 227 298      AQV
# 0 99 103 128 202 231 330     QCV
# 0 101 103 129 204 232 333    TCE

# Wanted:      0 71 101 113 131 184 202 214 232 285 303 315 345 416
# MIAT         0 71 101 113 131 172 184 232 244 285 303 315 345 416
# MTAI         0 71 101 113 131 172 184 232 244 285 303 315 345 416
# ALTM         0 71 101 113 131 184 202 214 232 285 303 315 345 416
# TAIM         0 71 101 113 131 172 184 232 244 285 303 315 345 416
# IAMT         0 71 101 113 131 184 202 214 232 285 303 315 345 416
# TMLA         0 71 101 113 131 172 184 232 244 285 303 315 345 416

