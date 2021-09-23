#%%
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import json
import os
#%%
df = pd.read_csv('cik_ticker.csv',sep="|")
df=df[:100]
print(df)
#%%
json_object ={}
endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"
headers = { 'User-Agent': 'Mozilla/5.0', }
json_object["companies"]=[]
exchange_list=[]
parent_dir = "C:/Users/trang/Documents/GitHub/NER-Company-Annual-Report/Data/"
#%%
for index, row in df.iterrows():
    company ={}
    company["CIK"] = row["CIK"]
    company["ticker"] = row["Ticker"]
    company["name"] = row["Name"]
    company["exchange"] = row["Exchange"]
    json_object["companies"].append(company)
    
    exchange = company["exchange"]
    if(type(exchange)==float):
        exchange = 'NaN'
    exchange_path = os.path.join(parent_dir, exchange)
    if not os.path.exists(exchange_path):
        os.makedirs(exchange_path)
        
    company_name = company["name"]
    company_cik = company["CIK"]
    company_path = os.path.join(exchange_path, company_name)
    if not os.path.exists(company_path):
        os.makedirs(company_path)
        
    param_dict_2 = {'action':'getcompany',
              'CIK':company_cik,
              'type':'10-k',
              'output':'atom'}
    response_10_K_list = requests.get(url = endpoint, params = param_dict_2,headers = headers)
    soup_10_K_list = BeautifulSoup(response_10_K_list.content, 'html.parser')
    link_list = []
    for each_10_K in soup_10_K_list.find_all('entry'):
        link_10_K = each_10_K.find_all('link')[0]['href']
        link_list.append(link_10_K)
    
    link_list_file = "link_10_Ks.txt"
    link_list_path = os. path. join(company_path,link_list_file)
    textFile = open(link_list_path,"w")
    for element in link_list:
        textFile.write(element + "\n")
    textFile.close()    
    exchange_list.append(company["exchange"] )
print(exchange_list) 
#%%   
print(set(exchange_list))