import sys
import numpy as np

def main():
    try:
        M = int(sys.argv[1])
    except Exception:
        print("Usage: %s M" % sys.argv[0])
        print("    M = total mass")
        sys.exit()

    PEP_NAMES      =          ['G', 'A', 'S', 'P', 'V', 'T', 'C', 'I', 'N', 'D', 'K', 'E', 'M', 'H', 'F', 'R', 'Y', 'W']
    # random data
    PEP_MASSES     = np.array([ 71,  99,  14,  37,  61,  63,  83,   3,  52,  43,   2,  80,  18,  37,  56,  36,  96,  13])
    LEN_PEP_MASSES = len(PEP_MASSES)
    NUM_COMB       = 2**LEN_PEP_MASSES-1

    # numpy array containing all possible coeficients
    C = np.array([[int(x) for x in np.binary_repr(K, width=LEN_PEP_MASSES)] for K in range(NUM_COMB)])
    # each element is an array of coefficients representing a number between 0 and NUM_COMB in binary form
    print ("type(C)      = %s" % type(C))
    print ("type(C[0])   = %s" % type(C[0]))
    print ("C.shape      = %s" % str(C.shape))
    print ("C[0].shape   = %s" % str(C[0].shape))
    print ("C[0]         = %s" % C[0])
    print ("C[15]        = %s" % C[15])
    print ("C[255]       = %s" % C[255])

    # Calculate sum of all combinations
    PROD = C.dot(PEP_MASSES)

    # find the ones that match M
    valid_combinations = [(i,x) for i,x in enumerate(PROD) if x == M]
    print ('Found %d possibilities with total mass = %d:' % (len(valid_combinations), M))
    print (valid_combinations)
    for comb_index, comb_mass in valid_combinations:
        # work back the combinations in string format
        comb_str = [PEP_NAMES[i] for i,x in enumerate(C[comb_index]) if x==1]
        print('%10d --> %s' % (comb_index, ''.join(comb_str)))

if __name__ == '__main__':
    main()
