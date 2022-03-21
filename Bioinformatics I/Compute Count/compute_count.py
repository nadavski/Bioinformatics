f = open("dataset_9_7.txt", 'r')

args = f.readlines()

string = args[0].strip()
k = int(args[1].strip().split(" ")[0])
d = int(args[1].strip().split(" ")[1])

bases = ['A', 'C', 'G', 'T']

def all_kmers(k):
    if k == 1:
        return bases
    
    kmers = []
    k_minus_one_mers = all_kmers(k-1)
    for base in bases:
        for i, kmer in enumerate(k_minus_one_mers):
            kmers.append(base + kmer)
    
    return kmers

kmers = all_kmers(k)

dp = {}

def get_neighborhood(string, d, index):
    if d == 0:
        return [string[index:]]

    if d > (len(string) - index):
        return None
    
    pair = (index, d)
    if pair in dp: 
        return dp[pair]
    
    neighbors = get_neighborhood(string, d, index+1)
    if neighbors is None:
        neighbors = []
    else:
        neighbors = [string[index] + neighbor for neighbor in neighbors]
    
    d_minus_1_neighbors = get_neighborhood(string, d-1, index+1)
    if d_minus_1_neighbors:
        for base in bases:
            if base == string[index]:
                continue
        
            neighbors.extend([base + neighbor for neighbor in d_minus_1_neighbors])
    
    dp[pair] = neighbors
    return neighbors

def neighborhood(string, D):
    dp.clear()
    all_neighbors = []
    for d in range(D+1):
        all_neighbors.extend(get_neighborhood(string, d, 0))
    return all_neighbors

count_occurences = {}
for pattern in kmers:
    count_occurences[pattern] = 0
    
count = 0
for i in range(len(string) - k + 1):
    search_pattern = string[i: i+k]
    neighbours = neighborhood(search_pattern, d)
    for neighbor in neighbours:
        count_occurences[neighbor] += 1

max_count = max(count_occurences.values())

result = ''

for pattern in count_occurences:
    if count_occurences[pattern] == max_count:
        result += pattern + ' '

print(result)