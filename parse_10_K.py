# imprort libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
#%%

#define the base url needed to create the file url
base_url = r"https://www.sec.gov"

# 10-K in text file: https://www.sec.gov/Archives/edgar/data/796343/0001047469-06-001601.txt
# url 10-K breakdown landing page
documents_url = r"https://www.sec.gov/Archives/edgar/data/96699/000117184320008787/index.json"

# request the url and decode it
headers = { 'User-Agent': 'Mozilla/5.0', }
content = requests.get(documents_url,headers = headers).json()
#%%
print(content)
#%%
for file in content['directory']['item']:
    if file['name'] == 'FilingSummary.xml':
        xml_summary = base_url + content['directory']['name']+'/'+file['name']
        print(file['name'])
        print(xml_summary)
#%%
# parse 10-K file
base_url_10_K = base_url + content['directory']['name']+'/'
#%%
# request and parse the content
content_xml = requests.get(xml_summary,headers = headers).content
soup = BeautifulSoup(content_xml,'lxml')

reports = soup.find('myreports')

master_reports = []
for report in reports.find_all('report')[:-1]: # the last one doesnt have same structure
    report_dict = {}
    report_dict['name_short'] = report.shortname.text
    report_dict['name_long'] = report.longname.text
    report_dict['position'] = report.position.text
    report_dict['category'] = report.menucategory.text
    report_dict['url'] = base_url_10_K  + report.htmlfilename.text
    
    master_reports.append(report_dict)
    
#%% Scrapping financial statements
    
# Define the statements we want to look for
item1 = r"Consolidated Balance Sheets"
item2 = r"Consolidated Statements of Operations and Comprehensive Income (Loss)"
item3 = r"Consolidated Statements of Cash Flows"
item4 = r"Consolidated Statements of Stockholder's (Deficit) Equity"
report_list = [item1, item2, item3, item4]
statements_url = []
for report_dict in master_reports:
    if report_dict['name_short'] in report_list:
        print('-'*100)
        print(report_dict['name_short'])
        print(report_dict['url'])
        
        statements_url.append(report_dict['url'])
#%%
print(statements_url)

#%% go through each statement and parse the data

statements_data = []
for statement in statements_url:
    # dict story different parts of statement
    # ??? will you lost connection between data and section???
    statement_data = {}
    statement_data['headers']=[]
    statement_data['sections']=[]
    statement_data['data'] = []
    
    # request statement file content
    content = requests.get(statement,headers = headers).content
    report_soup = BeautifulSoup(content,'html')
    
    for index, row in enumerate(report_soup.table.find_all('tr')):
        cols = row.find_all('td')
        
        # header
        if (len(row.find_all('th'))!=0):
            hed_row = [ele.text.strip() for ele in row.find_all('th')]
            statement_data['headers'].append(hed_row)
            
        #section
        elif (len(row.find_all('th'))==0 and len(row.find_all('strong'))!=0):
            sec_row = cols[0].text.strip()
            statement_data['sections'].append(sec_row)
            
        # regular row
        else:
            reg_row = [ele.text.strip() for ele in cols]
            statement_data['data'].append(reg_row)
    statements_data.append(statement_data)
print(statements_data)
#%%
print(statements_data[1]['headers'][1])

#%% Convert information into dataframe

income_headers = statements_data[1]['headers'][1]
income_data = statements_data[1]['data']
income_df = pd.DataFrame(income_data)
income_df.index = income_df[0]
income_df.index.name = 'Category'
income_df = income_df.drop(0,axis=1)

#%% 
# get rid of '$', '(',')'
income_df = income_df.replace('[\$,)]','',regex = True)\
    .replace('[(]','-', regex=True)\
        .replace('','NaN', regex=True)
        #%%
# convert number into float
income_df = income_df.astype(float)

#%%
# update header
income_df.columns = income_headers
income_df.to_csv('income_df.csv',index=True)

# Put the data in a DataFrame

#%%

print(income_data)