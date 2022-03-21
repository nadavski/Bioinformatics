

f = open('sequence.txt', 'r')

string = f.read().strip()
skew = 0
values = []



for i in string:
    if i == 'T' or i == 'A': 
        values.append(skew)
        continue
        
    if i == 'G':
        skew += 1
    else:
        skew -= 1
    
    values.append(skew)

min_value = max(values)
result = ''


for i in range(len(values)):
    if values[i] == min_value:
        result += str(i+1) + ' '


print("\n\n")
print(result)

