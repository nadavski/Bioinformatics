#!/bin/bash
#TAAAGACTGCCGAGAGGCCAACACGAGTGCTAGAACGAGGGGCGTAAACGCGGGTCCGAT
#sequence=$(cat /Users/nadav/Desktop/bioinformatics/old/scripts/lalala/sseq.txt)

sequence="GCATACACTTCCCAGTAGGTACTG"
#echo && read -p 'Sequence:' sequence && echo
counti=$(echo $sequence | wc -m)
END=counti

echo

for ((i=0;i<=END;i++)); do
	x=$i
	G=$(echo $sequence | head --bytes $x | sed 's/\(.\)/\1\n/g' | sort | uniq -c | grep G)
	C=$(echo $sequence | head --bytes $x | sed 's/\(.\)/\1\n/g' | sort | uniq -c | grep C)
	G2=$(echo $G | tr -d -c 0-9 )
	C2=$(echo $C | tr -d -c 0-9 )
	skew=$(expr $G2 - $C2)
	skewi=$(echo "$skew($i)")
	i_var=$(echo ${sequence:$i:1})
	finale=$(echo $i_var $skewi | grep -v A | grep -v T | grep [G.*C])
	echo $finale #>> temp-xd126262gn192m.txt
done
#cat temp-xd126262gn192m.txt | grep -v -e '^$' | sort
#echo $sequence && echo
#echo $sequence | sed 's/\(.\)/\1\n/g' | sort | uniq -c
#echo $counti && echo 
#rm ./temp-xd126262gn192m.txt
