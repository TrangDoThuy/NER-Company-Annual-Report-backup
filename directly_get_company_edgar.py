#%%
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

#%%
# base URL for the SEC EDGAR browser
endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"

# define our parameters dictionary
param_dict = {'action':'getcompany',
              'owner':'exclude',
              'company':'Westlake Chemical Partners LP Common Units representing limited partner interests',
              'output':'atom'}

# request the url, and then parse the response.
headers = { 'User-Agent': 'Mozilla/5.0', }
response = requests.get(url = endpoint, params = param_dict,headers = headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Let the user know it was successful.
print('Request Successful')
print(response.url)
#%%
print(soup)
#%%
for company in soup.find_all('entry'):
    company_cik = company.cik.find(text=True, recursive = False).strip()
    param_dict_2 = {'action':'getcompany',
              'CIK':company_cik,
              'type':'10-k',
              'output':'atom'}
    response_10_K_list = requests.get(url = endpoint, params = param_dict_2,headers = headers)
    soup_10_K_list = BeautifulSoup(response_10_K_list.content, 'html.parser')
    print("-"*30)
    print(response_10_K_list.url)
    time.sleep(0.1)
    
    for each_10_K in soup_10_K_list.find_all('entry'):
        link_10_K = each_10_K.find_all('link')[0]['href']
    
    
#%%
company_cik = 1265107
param_dict_2 = {'action':'getcompany',
              'CIK':company_cik,
              'type':'10-k',
              'output':'atom'}
response_10_K_list = requests.get(url = endpoint, params = param_dict_2,headers = headers)
soup_10_K_list = BeautifulSoup(response_10_K_list.content, 'html.parser')
print("-"*30)
print(response_10_K_list.url)
time.sleep(0.1)
    
for each_10_K in soup_10_K_list.find_all('entry'):
    print('='*10)
    print(each_10_K.find_all('link')[0]['href'])
    
    
#%%

endpoint = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1265107&type=10-k&dateb=20190101&owner=exclude&start=&output=atom&count=100"

# request the url, and then parse the response.
response = requests.get(url = endpoint, params = param_dict)
soup = BeautifulSoup(response.content, 'html.parser')
print(response.url)
#%%

# Let the user know it was successful.
print('Request Successful')
print(response.url)