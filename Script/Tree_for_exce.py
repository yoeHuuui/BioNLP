import spacy
import networkx as nx

nlp = spacy.load("en_core_web_sm")

fail_count=0
success_count=0
relation=()
CountForSentance = 0

result = open("getexcept.txt",'r',encoding='utf-8')
tree = open("Link_2.txt", 'w', encoding= 'utf-8')
except_sentance = open("getexcept_2.txt", 'w', encoding= 'utf-8')
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
        print("the previous progress lies around {:.2f}%".format(CountForSentance / 600.92))
    try:
        if ' ' in text[0]:
            s=0
            for j in text[0].split(' '):
                s=s+nx.shortest_path_length(graph,source=j,target=entity2)
            distance=int((s/len(text[0].split(' ')))+0.5)
            for token in doc:
                if token.dep_ == 'ROOT':
                    relation=(token.head.text)
            x = text[0]+'\t'+text[1]+'\t'+text[2]+'\t'+relation+'\t'+text[3]+'\t'+text[4]+'\t'+text[5]+'\t'+ str(distance)
            tree.write(x+'\n')
            success_count+=1
        else:
            distance=nx.shortest_path_length(graph,source=entity1,target=entity2)
            for token in doc:
                if token.dep_ == 'ROOT':
                    relation=(token.head.text)
            x = text[0]+'\t'+text[1]+'\t'+text[2]+'\t'+relation+'\t'+text[3]+'\t'+text[4]+'\t'+text[5]+'\t'+ str(distance)
            tree.write(x+'\n')
            success_count+=1
    except:
        except_sentance.write(i)
        fail_count+=1
        continue
tree.close()
print("Finished!")
