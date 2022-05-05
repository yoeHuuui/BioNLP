InputList = ['Gene', 'Chemical', 'Disease']

result = open("Key_Result.txt",'r',encoding='utf-8')
File_report = open('Key_Result_Transform.txt','w',encoding='utf-8')
Line_Entity = []
for line in result:
    if len(line.strip().split('\t')) != 6 and line != '\n':
        doc = line
        continue
    if len(line.strip().split('\t')) == 6:
        if (line.strip().split('\t')[4]) in InputList:
            Line_Entity.append(line)
        continue

    if line == "\n":
        #print(Line_Entity)
        if len(Line_Entity) >=2:
            for i in range(len(Line_Entity)):
                for j in range(len(Line_Entity)):
                    if i < j:
                        result = Line_Entity[i].strip().split('\t')[3] + '\t' + Line_Entity[i].strip().split('\t')[4]+ '\t' +Line_Entity[i].strip().split('\t')[5] +'\t'+ Line_Entity[j].strip().split('\t')[3]+ '\t' + Line_Entity[j].strip().split('\t')[4] + "\t" + Line_Entity[j].strip().split('\t')[5]+"\t" + doc
                        File_report.write(result)
        Line_Entity = []
