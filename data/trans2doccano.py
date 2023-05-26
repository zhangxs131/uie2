import json
from tqdm import tqdm
import pandas as pd
import os
def read_txt_list(file_name):
    with open(file_name,'r',encoding='utf-8') as f:
        content=f.read().splitlines()
    return content


def combine_csv(file_dir):
    file_list=os.listdir(file_dir)
    file_list=[i for i in file_list if i.split('.')[-1]=='csv']

    if len(file_list)>0:
        print(file_list[0])
        file_name=os.path.join(file_dir,file_list[0])
        df=pd.read_csv(file_name)

    for i in file_list[1:]:
        print(i)
        file_name=os.path.join(file_dir,i)
        df=df.append(pd.read_csv(file_name))

    return df

def trans_uie_format(df,save_file='ner_doccano_ext.json'):
    """

    原文件 query ,label ,label [{start,end,text,labels}
    to {id:id,text:query,relation=[],entities:["id": 0, "start_offset": 0, "end_offset": 6, "label": "时间" ]}

    """
    label_en=read_txt_list('label.txt')
    label_cn=read_txt_list('label_cn_simple.txt')
    label_en2cn={en:cn for en,cn in zip(label_en,label_cn)}


    with open(save_file,'w',encoding='utf-8') as f:
        for id,data in tqdm(df.iterrows()):
            query=data['query']
            label=data['label']
            try:

                entities=[]
                label=json.loads(label.replace("'",'"'))
                for lid,j in enumerate(label):
                    entities.append({"id":lid,"start_offset":j["start"],"end_offset":j["end"],"label":label_en2cn[j["labels"]]})

                f.write(json.dumps({"id":id,"text":query,"relations": [],"entities":entities},ensure_ascii=False)+'\n')

            except:
                continue


def main():
    file_dir='.'
    df=combine_csv(file_dir)
    trans_uie_format(df)

if __name__=='__main__':
    main()





