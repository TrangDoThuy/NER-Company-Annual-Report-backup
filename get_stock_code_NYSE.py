import pandas as pd
import json
#%%

df = pd.read_csv('NYSE_list.csv')
#%%
print(df.columns)
stock_code_json ={}
stock_code_json["companies"]=[]
#%%
for index, row in df.iterrows():
    company = {}
    company["stock_code"]=row['Symbol']
    company["name"]=row['Name']
    stock_code_json["companies"].append(company)
#%%
print(stock_code_json)
#%%
with open('NYSE_list.json','w', encoding='utf-8') as f:
    json.dump(stock_code_json, f, ensure_ascii=False, indent=4)
#%%