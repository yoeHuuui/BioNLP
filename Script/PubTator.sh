#!/bin/bash
f_out="Result_PubTator.txt"

echo -e "Result!\n" > $f_out
for i in $(cat Pmid.txt)
do
        url=https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids=$i
	curl --max-time 5 $url >> $f_out
	#echo $url
	echo -e "\n" >> $f_out
	printf "\n $i is in  processing!"
	sleep 4.5s
done
printf "Finish!"

printf "Get the Entity!"
grep -E "^[0-9]{8}\s" Result_PubTator.txt > Entity.txt

printf "Get the Abstract!"
grep -E "^[0-9]{8}\|a" Result_PubTator.txt > Abstract.txt
