def PathToGenome(path):
    text = path[0]
    for i in range(1, len(path)):
        text += path[i][-1]
    return text


with open('dataset.txt') as data:
    print('\n\n')
    print(
        'String Spelled by a Genome Path Problem -',
        PathToGenome(data.read().splitlines())
    )
