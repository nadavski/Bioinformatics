import sys

Genome = "GCATACACTTCCCAGTAGGTACTG"
#with open(sys.argv[1], 'r') as fp:
#           Genome = fp.readline().strip('\n')


def Skew(Genome):
    
    skew = [0]

    for i in range(0, len(Genome)):
        if Genome[i] == 'C':
            skew.append(skew[i] - 1)
        elif Genome[i] == 'G':
            skew.append(skew[i] + 1)
        else:
            skew.append(skew[i])
    return skew

def max_skew(Genome):
    skew = Skew(Genome)
    maximum = max(skew)
    return [i for i, val in enumerate(skew) if val == maximum]


ans = max_skew(Genome)

for num in ans:
    print(num)