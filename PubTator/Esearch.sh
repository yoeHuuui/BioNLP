#!/bin/bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Autism&RetMax=100000" > Autism.txt
cat Autism.txt | grep "<Id>" | sed  's/\t<Id>//g' | sed 's/<\/Id>//g' > pmid.txt
