import pandas as pd
from collections import Counter
import argparse

parser = argparse.ArgumentParser(description='The script for subset key word in entity!')
parser.add_argument('--input', '-i', help='list of key word')
args = parser.parse_args()
Input_List = (args.input).split()

print("Start to load the file!")
Entity = pd.read_table("../Data/Entity.txt", sep = '\t', header = None)
Entity.columns = ['pmid', 'start', 'end', 'text', 'type', 'id']
Entity['text'] = Entity['text'].str.strip()

print("Start to choose the subset of dataframe!")

for i in Input_List:
    print(i+" is processing!")
    Entity_List = Entity[Entity.type == i]
    x = Counter(Entity_List.text)
    Count_Result = pd.DataFrame(list(x.items()), columns=[i, 'Time'])
    Count_Result.sort_values(by = "Time", inplace = True, ascending = False)
    print(i+ " is dropping the times lower than 20 %")
    Count_Result = Count_Result[Count_Result['Time'] >= Count_Result['Time'].quantile(0.8)]
    print(i+" is writing now!")
    Count_Result.to_csv("../Result/Entity_Count_"+i+".txt", sep = '\t', index = False)
