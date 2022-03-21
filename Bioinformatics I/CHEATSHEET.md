
#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Read from STDIN
#~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys 
lines = sys.stdin.read().splitlines() # read in the input from STDIN
for i in xrange(len(lines)):
    print('Line ' + str(i+1) + ' is ' + str(len(lines[i])) + ' characters long.')
#~~~~~~~~
# Usage:
#~~~~~~~~
$ example_read_stdin.py < example_input.txt




#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Read from a text file
#~~~~~~~~~~~~~~~~~~~~~~~~~~~
f = open('sequence.txt', 'r')
file_name = f.read().strip()
lines = []
