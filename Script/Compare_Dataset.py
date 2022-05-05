import pandas as pd
from collections import Counter

Var_gene = pd.read_table("./VariCarta_Autism_gene.tsv", low_memory=False)
SFARI = pd.read_csv("./SFARI-Gene.csv")
Mine_gene = pd.read_table("Entity_Count_Gene.txt", sep = '\t')
Var_gene = Var_gene[['gene_symbol', 'chromosome']]
SFARI = SFARI[['gene-symbol', 'gene-score']]

Merge = pd.merge(SFARI, Var_gene, left_on = 'gene-symbol', right_on = 'gene_symbol')
Merge = Merge[['gene_symbol', 'gene-score']]
Merge.drop_duplicates(inplace = True)

print("The Counter result (In Database): {}.".format(Counter(Merge['gene-score'])))

Merge['gene_symbol'] = Merge.gene_symbol.str.lower()
Mine_gene['Gene'] = Mine_gene.Gene.str.lower()

Gene_Score_Mine = Counter(pd.merge(Merge, Mine_gene, left_on = 'gene_symbol', right_on = 'Gene')['gene-score'])
print("The Counter result (In mining result): {}.".format(Gene_Score_Mine))

dataset_gene = set(Merge.gene_symbol)
self_gene = set(Mine_gene.Gene)
Com_gene = dataset_gene & self_gene
dataset_only = dataset_gene - Com_gene
self_only = self_gene - Com_gene
pd.DataFrame(Com_gene).to_csv("Com_Gene.txt", index= False, sep = '\t', header = None)

print("The total number of gene in mining is {}.".format(len(self_gene)))
print("The commen gene number is {}.".format(len(Com_gene)))
print("The number of gene only in database is {}.".format(len(dataset_only)))
print("The number of gene only in mining is {}.".format(len(self_only)))
