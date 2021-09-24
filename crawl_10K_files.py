# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 09:59:10 2021

@author: trang
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
#%%
headers = { 'User-Agent': 'Mozilla/5.0', }
#%%

df = pd.read_csv("Data/NYSE/Advance Auto Parts Inc/link_10_Ks.txt",header=None)
base_path = "Data/NYSE/Advance Auto Parts Inc"
print(df)
#%%
source_url = "https://www.sec.gov/Archives/edgar/data/1158449/000115844921000036/0001158449-21-000036-index.htm"
json_file ={}
json_file["file_10_K"]=[]

#%%
for index,url_link in df.iterrows():
    response = requests.get(url = url_link[0],headers = headers)
    soup = BeautifulSoup(response.content,('html.parser'))
    json_object ={}
    report_period_title = soup.find(text="Period of Report")
    report_period = report_period_title.parent.findNext("div").text
    json_object["report_period"]=report_period
    filing_date_title = soup.find(text="Filing Date")
    filing_date = filing_date_title.parent.findNext("div").text
    json_object["filing_date"]=filing_date
    table = soup.find("table",{"summary":"Document Format Files"})
    row_10_K = table.find_all('tr')[1]
    cell_10_K_link = row_10_K.find_all('td')[2]
   # index = source_url.rfind('/')
    link_10K = "https://www.sec.gov" +cell_10_K_link.find('a')['href']
    link_10K = link_10K.replace("/ix?doc=","")
    
    index_name = link_10K.rfind('/')
    name_file = link_10K[(index_name+1):]
    
    json_object["source_url"] = link_10K
    json_file["file_10_K"].append(json_object)
    
    # create 10-K file locally
    local_path = base_path+"/annual_report_"+filing_date+"_"+name_file
    r = requests.get(link_10K, stream=True, headers = headers)
    print(r)
    with open(local_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=10240):
            f.write(chunk)
    
#%%
print(json_file)



