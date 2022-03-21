file = open('sequence.txt', 'r')
fullSet = file.read()

dataset = []
counter = 0

dataset = fullSet.split()

print("\n\n")
print(dataset[0])
print(dataset[1])

hammingDistance = 0

index = 0
for letter in dataset[0]:
    if letter != dataset[1][index]:
        hammingDistance += 1
    index += 1

print("Hamming Distance:", end=" "),
print(hammingDistance)
