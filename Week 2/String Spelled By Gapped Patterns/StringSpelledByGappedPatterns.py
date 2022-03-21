
def StringSpelledByGappedPatterns(patterns, k, d):
    first = ''
    second = ''
    for i in range(len(patterns) - 1):
        first += patterns[i][0][0]
        second += patterns[i][1][0]
    first += patterns[-1][0]
    second += patterns[-1][1]
    string_length = 2 * k + d + len(patterns) - 1
    nonoverlap_length = string_length - len(first)
    if first[nonoverlap_length:] == second[: -nonoverlap_length]:
        return first + second[-nonoverlap_length:]
    return

with open('dataset.txt') as data:
    lines = data.readlines()
    print(
        'StringSpelledByGappedPatterns Implementation -',
        StringSpelledByGappedPatterns(
            [line.strip().split('|') for line in lines[1:]],
            *map(int, lines[0].strip().split())
        )
    )
