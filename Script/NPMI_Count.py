import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='The script for calculate the NPMI in two entity')
parser.add_argument('--input', '-i', help='input file name', default='Key_Result_Transform.txt')
parser.add_argument('--output', '-o', help='output file name', default='NPMI_Result.txt')

parser.add_argument('--key', '-k', help='key type for calculate the value of NPMI, eg --key="Gene Disease"', required=True)
args = parser.parse_args()

Input_List = (args.key).split()
File_report = open(args.output,'w',encoding='utf-8')

print("Start to count the entity!")

Key_Result = pd.read_csv(args.input, sep='\t', header=None)
Key_Result.columns = ['E1', 'T1', 'C1', 'E2', 'T2', 'C2', 'Sentence']
Key_Result_1 = Key_Result[['E1', 'T1', 'C1']]
Key_Result_2 = Key_Result[['E2', 'T2', 'C2']]
Key_Result_1.columns = ['Entity', 'Type', 'Code']
Key_Result_2.columns = ['Entity', 'Type', 'Code']
Key_Result_Count = pd.concat([Key_Result_1, Key_Result_2])

Entity = Key_Result[['E1', 'E2']]
Entity = Entity.groupby(['E1', 'E2']).size().reset_index(name="Count")
Entity.sort_values(by = "Count", inplace = True, ascending = False, ignore_index = True)
Entity_Dic = Entity.set_index(['E1', 'E2']).T.to_dict('list')

###获取不同类型的计数信息
Result = []
for i in Input_List:
    Count_Result = Key_Result_Count[Key_Result_Count.Type == i]
    Count_Result = Count_Result.groupby(['Entity', 'Code']).size().reset_index(name="Time")
    Count_Result.sort_values(by = "Time", inplace = True, ascending = False, ignore_index = True)
    Result.append(Count_Result)

print("Finished to count entity!")
###统计宏观量
Totol_Sentence = len(Key_Result)
Totol_Time_1 = Result[0].Time.sum()
Totol_Time_2 = Result[1].Time.sum()

###计算两个type的所有实体间的NPMI
for i in range(len(Result[0])):
    for j in range(len(Result[1])):
        try:
            Collocate_1 = Entity_Dic[(Result[0].Entity[i], Result[1].Entity[j])][0]
        except:
            Collocate_1 = 0
        try:
            Collocate_2 = Entity_Dic[(Result[1].Entity[j], Result[0].Entity[i])][0]
        except:
            Collocate_2 = 0
        Collocate = Collocate_1 + Collocate_2
        Time_1 = Result[0].Time[i]
        Time_2 = Result[1].Time[j]
        p_1 = Time_1 / Totol_Time_1
        p_2 = Time_2 / Totol_Time_2
        p_co = Collocate / Totol_Sentence
        ### 共句次数为0,NPMI会为NAN,提前处理异常值
        if p_co != 0:
            NPMI = np.log(p_co / (p_1 * p_2)) / np.log(p_co)
            Each_NPMI = Result[0].Entity[i] + "\t" + Result[0].Code[i]+ "\t" + Result[1].Entity[j] + "\t" + Result[1].Code[j] + "\t"+ str(NPMI)
            File_report.write(Each_NPMI+'\n')
    if i % 75 == 0:
        print("the previous progress lies around {:.2f}%".format(i * 100 / len(Result[0])))
print("Finished!")