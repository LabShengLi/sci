#!/bin/bash 


infile=$1
outfile=$2
res=$3
for ((i=1;i<=22;i++)); do 
	for ((j=$((i))+1;j<=22;j++)); do 
		c1=chr${i}
		c2=chr${j}
		java -jar ${JUICERTOOLS} dump observed KR ${infile} chr${i} chr${j}  BP ${res} | awk -v c1=chr${i} -v c2=chr${j} -v res=${res} '{OFS="\t"}{print c1,$1,$1+res,c2,$2,$2+res,$3}' >> ${outfile};
	done 
done


