

Minimum Skew Problem

Let's follow the 5' → 3' direction of DNA and walk along the chromosome 
from ter to ori (along a reverse half-strand), then continue on from ori to ter (along a forward half-strand). 
Skew is decreasing along the reverse half-strand and increasing along the forward half-strand. 
Thus, the skew should achieve a minimum at the position where the reverse half-strand ends and the forward half-strand begins, which is exactly the location of ori!

We have just developed an insight for a new algorithm for locating ori: it should be found where the skew attains a minimum.
-------------------------------------------------------------------------------------------------------------------------
Code challenge: Find a position in a genome where the skew diagram attains a minimum.

- Input: A DNA string Genome.
- Output: All integer(s) i minimizing Skewi (Genome) among all values of i (from 0 to |Genome|).

Sample Input:
    TAAAGACTGCCGAGAGGCCAACACGAGTGCTAGAACGAGGGGCGTAAACGCGGGTCCGAT

Sample Output:
    11 24
-------------------------------------------------------------------------------------------------------------------------



