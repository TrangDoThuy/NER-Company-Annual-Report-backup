#%%
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
#%%
df = pd.read_csv('list_10_K.csv')
print(df)
#%%
base_url = r"https://www.sec.gov"
name_list=[]
master_file={}
for index,folder_url in enumerate(df.folder_url):
    if(index==0):
        print(folder_url)
        documents_url = folder_url+"/index.json"
        headers = { 'User-Agent': 'Mozilla/5.0', }
        content = requests.get(documents_url,headers = headers).json()
        for index_second,file in enumerate(content['directory']['item']):
            if(index_second==10):
                file_url = base_url + content['directory']['name']+'/'+file['name']
                print(file_url)
                content_file = requests.get(file_url,headers = headers).content
                with open(file['name'],'wb') as f:
                    f.write(content_file)
                master_file[file['name']]=content_file
                name_list.append(file['name'])
                print("="*30)
                print(content_file)
                
                time.sleep(0.1)
                
            
print(name_list)
#%%
print(master_file['0001047469-06-001601-index-headers.html'])
#%%
for key, value in master_file.items() :
    print( key)
#%%