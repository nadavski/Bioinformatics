import sys,Code1_8_HammingDistance as hd


def approximate_pattern_match(pattern,text,d):
	idx = []
	k = len(pattern)
	for i in range(len(text)-k+1):
		if hd.hamming_distance(text[i:i+k],pattern) <= d:
			idx.append(i)
	return idx

if __name__ == '__main__':
	if len(sys.argv) == 2:
		filename = sys.argv[1]
		with open(filename) as f:
			lines = f.read().splitlines()
		pattern = lines[0]
		text = lines[1]
		d = int(lines[2])
	else:
		pattern = 'AA'
		text = 'TACGCATTACAAAGCACA'
		d = 1
		
	idx = approximate_pattern_match(pattern,text,d)
	print(' '.join(map(str,idx)))

# - Sample Input: ATTCTGGA  CGCCCGAATCCAGAACGCATTCCCATATTTCGGGACCACTGGCCTCCACGGTACGGACGTCAATCAAAT  3
# - Sample Output: 6 7 26 27
#file = open('/Users/fuckoff.', 'r')
#fullSet = file.read()
