import spacy
import networkx as nx
import argparse

nlp = spacy.load("en_core_web_sm")

parser = argparse.ArgumentParser(description='The script for calculate the NPMI in two entity')
parser.add_argument('--input', '-i', help='input file name', default='Key_Result_Transform.txt')
parser.add_argument('--output', '-o', help='output file name', default='Tree_Link.txt')
parser.add_argument('--key', '-k', help='key type for calculate the value of NPMI, eg --key="Gene Disease"', required=True)
args = parser.parse_args()

fail_count=0
success_count=0
relation=()
CountForSentance = 0

result = open(args.input,'r',encoding='utf-8')
tree = open(args.output, 'w', encoding= 'utf-8')
except_sentance = open("getexcept.txt", 'w', encoding= 'utf-8')
for i in result:
    text = i.split("\t")
    doc = nlp(text[6])
    edges=[]
    for token in doc:
        for child in token.children:
            edges.append(('{0}'.format(token),'{0}'.format(child)))
    graph=nx.Graph(edges)
    entity1=text[0]
    entity2=text[3]
    CountForSentance += 1
    if CountForSentance % 1500 == 0:
        print("the previous progress lies around {:.2f}%".format(CountForSentance / 1057.092))
    try:
        if ' ' in text[3]:
            s=0
            for j in text[3].split(' '):
                s=s+nx.shortest_path_length(graph,source=entity1,target=j)
            distance=int((s/len(text[3].split(' ')))+0.5)
            for token in doc:
                if token.dep_ == 'ROOT':
                    relation=(token.head.text)
            sentence = text[0]+'\t'+text[1]+'\t'+text[2]+'\t'+relation+'\t'+text[3]+'\t'+text[4]+'\t'+text[5]+'\t'+distance
            tree.write(sentence + "\n")
            success_count+=1
        else:
            distance=nx.shortest_path_length(graph,source=entity1,target=entity2)
            for token in doc:
                if token.dep_ == 'ROOT':
                    relation=(token.head.text)
            sentence = text[0]+'\t'+text[1]+'\t'+text[2]+'\t'+relation+'\t'+text[3]+'\t'+text[4]+'\t'+text[5]+'\t'+distance
            tree.write(sentence + "\n")
            success_count+=1
    except:
        except_sentance.write(i)
        fail_count+=1
        continue
tree.close()
print("Finished!")