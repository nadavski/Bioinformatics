with open('integer_mass_table.txt') as f:
    mass_by_acid = dict([(lambda c, w: (c, int(w)))(*line.split()) for line in f.readlines()])
acid_by_mass = dict([(m, s) for s, m in mass_by_acid.items()])
masses = all_acids = sorted(list(set(mass_by_acid.values())))


def peptides_of_mass(max_mass):
    storage = [0] * max_mass
    def put(combs, i):
        i += 1
        print(i)
        new_combs = []
        for comb in combs:
            storage[comb] += 1
            for mass in masses:
                new_comb = comb + mass
                if new_comb <= max_mass:
                    storage[new_comb] += 1
                    new_combs.append(comb + mass)
        put(new_combs, i)

    put(masses, 0)
    print(storage)
#
    return 0


#def peptides_of_mass(max_mass):
#    table = [1] + [None] * max_mass
#    roots = [None] * (max_mass + 1)

#    def _get_mass(mass, level):
#        if mass < 0:
#            return 0
        #print '    ' * level, 'finding for', mass
#        if table[mass] is not None:
#            count = table[mass]
#        else:
#            count = sum(_get_mass(mass - m, level + 1) for m in masses)
#            table[mass] = count
#        if count > 0:
#            if mass > 0:
#                roots[mass] = count ** (1.0 / float(mass))
#            print('    ' * level, mass, ':', count)
#        return count

#    mass = _get_mass(max_mass, 0)
#    print(' '.join(map(str, roots)))
#    return mass


print(peptides_of_mass(24))
