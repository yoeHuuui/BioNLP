# Codes developer: Sizhuo Ouyang
# HZAU BioNLP Lab
# 2022-04
# 代码目的：读取PubTator结果文件，根据关键词生成命中句及其标注。代码仅提供基础功能，欢迎试用，改写。


###########################################################
# $cat data/pubtator_blca.txt| head -7
#20301443|t|Peutz-Jeghers Syndrome
#20301443|a|CLINICAL CHARACTERISTICS: Peutz-Jeghers syndrome (PJS) is an autosomal dominant condition characterized by 
#     the association of gastrointestinal polyposis, mucocutaneous pigmentation, and cancer predisposition. Peutz-Jeghers-
#     type hamartomatous polyps are most common in the ...
#20301443        49      71      Peutz-Jeghers syndrome  Disease MESH:D010580
#20301443        73      76      PJS     Gene    6794
#20301443        149     175     gastrointestinal polyposis      Disease MESH:D005767
#20301443        177     203     mucocutaneous pigmentation      Disease MESH:D010859
#20301443        209     215     cancer  Disease MESH:D009369
###########################################################

import nltk
from nltk.tokenize import sent_tokenize
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='The script for find key word in sentence')
parser.add_argument('--input', '-i', help='input file name')
parser.add_argument('--output', '-o', help='output file name', default='../Result/Key_Result.txt')

parser.add_argument('--key', '-k', help='key type for search', required=True)
args = parser.parse_args()

Input_List = (args.key).split()
key = []
for i in Input_List:
    key += list(pd.read_csv("../Result/Entity_Count_"+i+".txt", sep = '\t')[i])

File_source_pubtator = open(args.input,'r',encoding='utf-8')
File_report = open(args.output,'w',encoding='utf-8')

def filter_sent(key):
    B_AnnPerArticle_dic = {}  #词典AnnPerArticle_dic，#句首字母off-set起始位作为Key， 标注多行结果作为Value。每读完一个Article，置空。
    B_E_SentPerArticle_list = []   #句子列表。每读完一个Article，置空。
                     #[{'begin': 0, 'end': 23, 'sent': 'Peutz-Jeghers Syndrome'}, 
                     #{'begin': 24, 'end': 232, 'sent': 'CLINICAL CHARACTERISTICS: Peutz-Jeghers bla bla.'}]
    FilteredSentCount = 0 #筛选出的句子的计数
    ArticleID = []
    CountForArticle = 0
    for line in File_source_pubtator:
        #line处理Step-1: 对title的行的处理
        if line[8:11] == '|t|':
            #title_for_print = line.strip().split('|t|')[-1] #title_for_print 用于保留打印
            #print(title_for_print)
            title = line.strip().split('|t|')[-1]
            len_title = len(title)
            B_E_SentPerArticle_list.append({"begin":0,"end":len_title+1,"sent":title})
            #[{'begin': 0, 'end': 23, 'sent': 'Peutz-Jeghers Syndrome'}]
            continue         

        #line处理Step-2: 对abstract行的处理
        if line[8:11] == '|a|':
            article = line.strip().split('|a|')[-1]
            sents = sent_tokenize(article) #依据句号分句
            start = len_title+2
            sent_start = []
            sent_end = []
            sent_start.append(start)
            for sent in sents:
                start = len(sent) + 1 + start
                sent_start.append(start)
                sent_end.append(start-1) 
                
            for i,s in enumerate(sent_start[0:-1]):
                B_E_SentPerArticle_list.append({"begin":s,"end":sent_end[i],"sent":sents[i]}) 
                
            continue   

        #line处理Step-3: #对多个标注行的处理            
        if len(line.strip().split('\t')) == 6:  #判断是否为标注行 
            B_AnnPerArticle_dic[line.strip().split('\t')[1]] = line  #off-set起始位置作为Key， 标注的多行结果作为Value， 建词典
            continue
           
        #line处理Step-4: 每读到空行+换行符，开始处理一篇摘要或者全文：把标注写入词典AnnPerSent_dic，
        if line == '\n': 
            CountForArticle += 1
            if CountForArticle % 10000 ==0:
                print("the previous progress lies around {:.2f}%".format(CountForArticle / 1800))
            Sent_AnnPerArticle_dic = {} #词典AnnPerSent_dic，Key为句子，Value为标注
            sent_annos = []  #定义一个列表，一一读取所有标注行。存入到AnnPerSent_dic后，写入报告文件File_report，再置空。
            for each_b_e_sent in B_E_SentPerArticle_list:
                for anno_start in B_AnnPerArticle_dic.keys():
                    if int(anno_start) >= int(each_b_e_sent["begin"]) and int(anno_start) < int(each_b_e_sent["end"]):
                        sent_annos.append(B_AnnPerArticle_dic[anno_start])               
                Sent_AnnPerArticle_dic[each_b_e_sent["sent"]] = sent_annos  #词典AnnPerSent_dic中，key为句子，Value为标注
                sent_annos = []
       
            for each_sent in Sent_AnnPerArticle_dic.keys():
                if len(Sent_AnnPerArticle_dic[each_sent]) >=2: #筛选至少包含两个实体的句子
                    KeyWordList = []
                    for keyword in key:
                        if keyword in each_sent:
                            KeyWordList.append(keyword)
                    if len(KeyWordList)>= 2: #有多个关键词出现的句子仅记录一遍
                        File_report.write(each_sent+'\n')
                    
                        for a in Sent_AnnPerArticle_dic[each_sent]:
                            File_report.write('{0}'.format(a))
                            ArticleID.append(a.strip().split('\t')[0])
                        File_report.write('\n')
                        FilteredSentCount = FilteredSentCount + 1    
                               
            B_E_SentPerArticle_list = []
            B_AnnPerArticle_dic = {}

    print('In total, {0} sentences are filtered from {1} articles.\n And the results are stored in {2}! Enjoy! \n'.format(FilteredSentCount, len(set(ArticleID)), args.output))      


print ("We are returning all filtered sentences which included the key words:\"{0}\", all the PubTator annotations are given as well. \n Please wait...\n".format(Input_List))
filter_sent(key)
