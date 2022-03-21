

import sys

f = open('sequence.txt', 'r')
file_name = f.read().strip()

lines = []



with open('dataset.txt', 'r') as f:
	for line in f:
		lines.append(line[:-1])
	
seq = lines[0]
k = int(lines[1])
profile = []
for line in lines[2:]:
	profile.append([float(x) for x in line.split()])


def profile_score(pattern,profile):
	score = 1
	order = {'A':0,'C':1,'G':2,'T':3}
	if len(pattern) != len(profile[0]):
		return
	else:
		for j in range(len(pattern)):
			score *= profile[order[pattern[j]]][j]
	return score

def most_probable_kmer(seq,k,profile):
	scores = []
	for i in range(len(seq) - k + 1):
		pattern = seq[i:i+k]
		scores.append(profile_score(pattern,profile))
	pos = scores.index(max(scores))
	return seq[pos:pos+k]


if __name__ == '__main__':
	ans = most_probable_kmer(seq,k,profile)
	print(ans)