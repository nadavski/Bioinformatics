
##########################################################################
#######    Bioinformatics II - Genome Sequencing - Week 5          #######
#######    Bioinformatics Application Challenge: Genome Assembly   #######
##########################################################################

####### Q1 #######
N75 is the maximal contig length for which all contigs of at least that length comprise at least 75% of the sum of the lengths of all contigs.
0 pts - The learner's response does not match the one given above.
2 pts - The learner gives a reasonable response but neglects to include "maximal"
3 pts - The learner's response more or less matches the one given above.
####### Q1 #######
Q1: Based on the above definition of N50, define N75.

A1: N75 is a statistic that is used to measure the quality of an assembly, as well as N50. The difference is that the length is set at 75% of total base content instead of 50%.

####### Q2 #######
Q2:N50 and N75 for the nine contigs with the following lengths: [20, 20, 30, 30, 60, 60, 80, 100, 200].
A2: N50 = 100, N75 = 60


####### Q3 #######
Q3: Say that we know that the genome length is 1000. What is NG50?
A3: NG50 = 60


####### Q4 #######
Q4: If the contig in our dataset of length 100 had a misassembly breakpoint in the middle of it, what would be the value of NGA50?
A4:  NGA50 = 50


####### Q5 #######
Q5: Based on the definition of scaffolds, what information could we use to construct scaffolds from contigs?  Justify your answer.
A5: Would mainly need the gap lengths from the mate-pair reads to accurately determine the gaps in the genome.
Coursera answer: 
Additional long reads could be generated in an attempt to find reads that bridge 
the gaps in contigs.  In other words, if we find a long read that begins
 at the end of contig A, and ends at the beginning of contig B, then we 
can conclude that the read extends across the gap between the contigs.
My answer: If you find long reads, that is beginning with the ending of contig(A) and ends with the beginning of contig(B),  we 
could assume that the read increases across the gap between Contigs.


####### Q6 #######
Q6: First, fill in the 9 missing values in the following 3 x 3 table:
A6: 
k N50 # long contigs total length of long contigs
25 59,595 110 2,802,857
55 159,616 38 2,821,839
85 188,896 37 2,825,752

####### Q7 #######
Q7: Which assembly performed the best in terms of each of these statistics?  Justify your answer. Why do you think that the value you chose performed the best?
A7: The k=85 assembly appears to be the best because it gives the largest length out of the long contigs and the largest N50 value. This indicates that you can create a larger scaffold and a recreate a larger amount of the genome in question with this k value compared to the others.

My answer: k = 85 seems to be the best because its N50 value is the largest, and it has less contigs than k=25.
Which is indicating that we could recreate a larger amount of the genome with k=85 compared to the others.

Coursera answer: The total length of long contigs is about the same for all three values of k.  Accordingly, we conclude that the assembly using k = 85 performed the best because it has a  larger value of N50 and fewer contigs than k = 25, while having the same number of contains as k = 55.
k = 85 performs the best because  if the reads are too short (k  = 25 or 55), then the reads contain too little information, and repeats may  make it difficult to identify where a read came from.

1 point for identifying k = 85;
1 point for a reasonable justification of why k = 85 was the best choice according to statistics;
2 points for attempting a reasonable explanation of why k = 85 wound up being the best value of k.



####### Q8 #######
Q8: (Multiple choice) When you increase the length of k-mers, the de Bruijn graph ____________.  Justify your answer.
A8: When the k-mer length increases we reduce the number of nodes in the graph in doing so we also reduce the overall number of edges thus making the graph less tangled. So for this question C (the de Brujin praph becomes less tangled) is the right answer.

Coursera answer: The correct answer is C).
We saw in the class text (and lecture) that increasing the value of k used to generate k-mer reads led to a less tangled de Bruijn graph because the larger the value of k,
 the greater the amount of information contained in our reads, and the 
lesser the effects of repeats.   More details are available in the 
course text.



####### Q9 #######
Q9: A​answer the following two questions using the QUAST reports. 
1. How many misassemblies were there?
2. 2. How significant is the effect of misassemblies on the resulting assembly?
A9: 
1. When k=25; misassemblies = 23
When k=55; misassemblies = 27
When k=85; misassemblies = 29
2. It looks like the missassemblies increase as k-mer length also increases and it negatively impacts the recreated genome. So there must be a sweet spot between increasing the k length to obtain more of the genome and decreasing the number of misassemblies.
Coursera answer: 1. There were 27 misassemblies. (number may vary slightly depending on the version used.)

2. For k  = 85 there were only about 37 long contigs (number may vary slightly depending on the version used), meaning that the misassemblies  are likely causing most of the long contigs to have been broken into  pieces.


####### Q10 #######
Q10: 
1. What are NG50 and NGA50 for the QUAST run?
2. How do they compare with the value of N50 that you previously calculated?  Why?
A10: 
1. In reference to the k = 25 run; the NG50 = 77760 and NGA50 = 35824
In reference to the k = 55 run; the NG50 = 176512 and NGA50 = 92194
In reference to the k = 85 run; the NG50 = 202267 and NGA50 = 87161
2. For all the runs, the N50 value are larger than the NG50 values, and indicates that the quality of assembly increases with k-length. However, when considering misassemblies the NGA value do seem to be lower than the N50 values from before. Morever, the NGA value is highest for k=55 and decreases when k=85. This would indicate that k=55 may be a better assembly than k=85 after all.

Coursera answer: 
(​Note: values may vary slightly based on updates to the software.)
(1 point): NG50 = 202,267.
(1 point): NGA50 = 87,161.
N50 values are larger than NG50 values. The quality of assembly increases along K(length). 
When considering misassemblies the NGA value is lower than  N50  from before. 
NGA value is the highest for k=55 and start decreasing where k=85. 
This indicates that k=55 may be a better assembly than k=85 after all.

