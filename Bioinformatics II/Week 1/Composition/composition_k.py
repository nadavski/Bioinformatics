def StringComposition(text, k):
    k_mers = []
    for i in range(len(text) - k + 1):
        k_mers.append(text[i: i + k])
    return sorted(k_mers)


with open('dataset.txt') as data:
    lines = data.readlines()
    k_mers = StringComposition(
        lines[1].rstrip('\n'),
        int(lines[0].rstrip('\n'))
    )
with open('string_composition_answer.txt', 'w') as data:
    data.writelines("%s\n" % k_mer for k_mer in k_mers)

print('String Composition Problem -', 'In file "string_composition_answer.txt"')
