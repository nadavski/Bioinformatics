

print('\n\n') 
print('------- Question 1 -------')
print('There is a unique longest common subsequence of the strings TGTACG and GCTAGT.  What is it? \n')
print('**** Check Out LCS from Week 1 (BIoinfo III). ****\n')

print('------- Question 2 -------')
print('True or False: There are some coin denominations for which GreedyChange does not solve the Change Problem \n(i.e., does not find a minimum number of coins making change) .\n')
print('A2: True')
print("Verified and true.\n")

print('------- Question 3 -------')
print('Imagine a hypothetical world in which there are two amino acids, X and Z, having respective masses 2 and 3. \n How many linear peptides can be formed from these amino acids having mass equal to 25? \n(Remember that the order of amino acids matters.)\n')

import operator
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(operator.mul, range(n, n-r, -1))
    denom = reduce(operator.mul, range(1, r+1))
    return numer//denom

#print(ncr(12,1) + ncr(11,3) + ncr(10,5) + ncr(9,7))



print("Verified and true.\n")

print('------- Question 4 -------')
print('True or False: All recursive algorithms are inefficient.')
print('A4: False\n')
print("Verified and true.\n")


print('------- Question 5 -------')
print('Consider the following adjacency list of a DAG:')

print('a -> b: 5 \na -> c: 6 \na -> d: 5 \nb -> c: 2 \nb -> f: 4 \nc -> e: 4 \nc -> f: 3 \nc -> g: 7 \nd -> e: 4 \nd -> f: 5 \ne -> g: 2 \nf -> g: 1\n')


print('What is the longest path in this graph?  Give your answer as a sequence of nodes separated by spaces.  (Note: a, b, c, d, e, f, g is a topological order for this graph.)\n')



print('------- Question 6 -------')
print('Here is the adjacency list of a graph with six nodes and ten edges: \n')
print('a -> b, c, d, e, f \nb -> c, f \nc -> d \nd ->  \ne -> d, f \nf -> \n')
print('Which of the following are topological orderings of the nodes in this graph? (Select all that apply.)\n')

print('------- Question 7 -------')
print('True or False: \nThe dynamic programming algorithm we introduced for finding a longest path in a DAG has runtime \nproportional to the number of nodes in the graph.')
print('A7 : False')
print("Verified and true.\n")
