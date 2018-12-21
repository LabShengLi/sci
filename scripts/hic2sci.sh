#!/bin/bash 


infile=$1
outfile=$2
res=$3
for ((i=1;i<=22;i++)); do 
	for ((j=$((i));j<=22;j++)); do 
		c1=chr${i}
		c2=chr${j}
		java -jar ${JUICERTOOLS} dump observed NONE ${infile} chr${i} chr${j}  BP ${res} | awk -v c1=chr${i} -v c2=chr${j} -v res=${res} '{OFS="\t"}{print c1,$1,$1+res,c2,$2,$2+res,$3}' >> ${outfile};
	done 
done


#dump <observed/oe> <NONE/VC/VC_SQRT/KR> <hicFile(s)> <chr1>[:x1:x2] <chr2>[:y1:y2] <BP/FRAG> <binsize> [outfile]