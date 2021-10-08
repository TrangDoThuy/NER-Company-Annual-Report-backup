# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:55:06 2021

@author: trang
"""

import codecs
import re
import pandas as pd
import json
from bs4 import BeautifulSoup
import spacy
nlp = spacy.load("en_core_web_sm")
#%%
def remove_unnecessary_letter(input_string):
    
    TAG_RE = re.compile(r'<[^>]+>')
    TABLE_CONTENT_RE = re.compile(r'[0-9]+\s+Table of Contents')
    TABLE_CONTENT_RE_2 = re.compile(r'[0-9]\(table of contents\)')
    TABLE_CONTENT_RE_3 = re.compile(r'[0-9]+Table of Contents')
    SPACE_RE = re.compile(r'(\s\s)+')
    
   
    list_remove_re = [TAG_RE,TABLE_CONTENT_RE,SPACE_RE,TABLE_CONTENT_RE_2,TABLE_CONTENT_RE_3]
    for remove_re in list_remove_re:
        input_string = re.sub(remove_re,'', input_string)
        
    input_string = input_string.replace('.\n',"hihi")
    
    remove_items = ['&#160;',"&nbsp;","&nbsp","nbsp;","nbsp","   ","\n"] 
    for item in remove_items:
        input_string = input_string.replace(item," ")
    input_string = input_string.replace("&middot;","\n\t &middot;")
    input_string = input_string.replace("hihi",'.\n')
    input_string = input_string.strip()  
    return input_string

#%%
#file_path = 'Data/NYSE/Alcoa Inc/annual_report_2009-02-17_d10k.htm'
#file_path = 'Data/NYSE/Agilent Technologies Inc/annual_report_2010-12-20_a2201423z10-k.htm'
#file_path = 'Data/NASDAQ/Sinocoking Coal & Coke Chemical Industries Inc/annual_report_2013-09-30_v355550_10k.htm'
#file_path = 'Data/OTCBB/Auburn Bancorp Inc/annual_report_2010-09-28_t68978_10k.htm'
#file_path = 'Data/NaN/Asset Acceptance Capital Corp/annual_report_2010-03-12_d10k.htm'
#file_path = 'Data/OTC/All American Gold Corp/annual_report_2013-11-06_form10ka.htm' 
#file_path = 'Data/OTC/Aaipharma Inc/annual_report_2004-06-15_g87794e10vk.htm'
#file_path = 'Data/OTC/Avantair Inc/annual_report_2010-09-28_v197483_10k.htm'
#file_path = 'Data/NASDAQ/American Airlines Group Inc/annual_report_2016-02-24_d78287d10k.htm'
#file_path = 'Data/NASDAQ/American Airlines Group Inc/annual_report_2020-02-19_a10k123119.htm'
#file_path = 'Data/OTC/Altisource Asset Management Corp/annual_report_2020-02-28_aamc10k12312019.htm'
#file_path = 'Data/NASDAQ/Atlantic American Corp/annual_report_2010-03-26_g22608e10vk.htm'
file_path = 'Data/NYSE/Aarons Inc/annual_report_2014-02-24_a10k4q2013.htm'
f=codecs.open(file_path, 'r')
file_content = f.read()
print(file_content)
#%%

#%%
# Write the regex
regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(7A|7)\.{0,1})|(>Item(7A|7)\.{0,1})|(>(\s)+Item(\s|&#160;|&nbsp;)(7A|7)\.{0,1})|(>(\s)+Item(7A|7)\.{0,1})|(>ITEM(\s|&#160;|&nbsp;)(7A|7)\.{0,1})|(>ITEM(7A|7)\.{0,1})|(>(\s)+ITEM(\s|&#160;|&nbsp;)(7A|7)\.{0,1})|(>(\s)+ITEM(7A|7)\.{0,1})')
matches = regex.finditer(file_content)
#%%
# Write a for loop to print the matches
count = 0
for match in matches:
    count +=1
    print(file_content[match.start()-10:match.end()+10])
print(count)
if(count == 0):
    print("This documents doesnt have item 7")

#%%
# Create the dataframe
matches = regex.finditer(file_content)
test_df = pd.DataFrame([(x.group(), x.start(), x.end(),file_content[x.start()-10:x.end()]) for x in matches])

test_df.columns = ['item', 'start', 'end','content']
test_df['item'] = test_df.item.str.lower()
print(test_df)

#%%
# Get rid of unnesesary charcters from the dataframe
test_df.replace('&#160;',' ',regex=True,inplace=True)
test_df.replace('&nbsp;',' ',regex=True,inplace=True)
test_df.replace(' ','',regex=True,inplace=True)
test_df.replace('\.','',regex=True,inplace=True)
test_df.replace('>','',regex=True,inplace=True)
test_df.replace('\n','',regex=True,inplace=True)
print(test_df)
#%%
# Drop unnecessary row
while(test_df.iloc[-1]['item'] == 'item7'):
    test_df = test_df[:-1]
print(test_df)
    
#%%
# Drop duplicates
pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')
# Set item as the dataframe index
pos_dat.set_index('item', inplace=True)
print(pos_dat)
#%%
# Get Item 7
item_7_raw = file_content[pos_dat['start'].loc['item7']:pos_dat['start'].loc['item7a']]

#%%
#remove table
count_table = 0
while "<TABLE" in item_7_raw:
    count_table +=1
    start_index = item_7_raw.index("<TABLE")
    if "</TABLE>" in item_7_raw[start_index:]:
        end_index = item_7_raw.index("</TABLE>",start_index)
        #item_7_raw = item_7_raw[:start_index]+item_7_raw[end_index+8:] 
        item_7_raw = item_7_raw.replace(item_7_raw[start_index:(end_index+8)],'')
    else:
        break
#%%
# print(item_7_raw.count('</TABLE>'))
# table_regex = re.compile(r'(</TABLE>)')
# item_7_raw = re.sub(table_regex,'', item_7_raw)
# print('+'*10)
# print(item_7_raw.count('</TABLE>'))
# print('+'*10)

#%%
# Write the regex
#regex = re.compile(r'((<b)|(<B))')

regex = re.compile(r'(<B><U>(.*)</U></B>)|(<B><I>(.*)</I></B>)|(<B>[^<]+</B>)|(<b>(.*)</b>)|(<b><u>(.*)</u></b>)|(<b><i>(.*)</i></b>)')

# Use finditer to math the regex
matches = regex.finditer(item_7_raw)

# Write a for loop to print the matches
# count = 0
# for match in matches:
#     count +=1
#     print(item_7_raw[match.start()-10:match.end()+10])
# print(count)
#%%

matches = regex.finditer(item_7_raw)
# Create the dataframe
if(len(list(matches))>0):
    matches = regex.finditer(item_7_raw)
    test_df = pd.DataFrame([( x.start(), x.end(),item_7_raw[x.start():x.end()]) for x in matches])
    test_df.columns = [ 'start', 'end','header']
    print("="*18)
else:
    print("{"*18)
    data = []
    regex_bold = regex = re.compile(r'(bold[^<]+</)')
    matches = regex.finditer(item_7_raw)
    test_df = pd.DataFrame(columns=[ 'start', 'end','header'])
    for match in matches:
        print(match)
        match_content = item_7_raw[match.start():match.end()]
        start_index = item_7_raw.index('>',match.start(),match.end())+1
        end_index = item_7_raw.index('</',start_index,match.end())
        new_row = {'start':start_index,'end':end_index,'header':item_7_raw[start_index:end_index]}
        data.append(new_row)
    test_df = pd.DataFrame(data)
print(test_df)


#%%

list_content =[]
for i in range(1, len(test_df["start"])):
    content = item_7_raw[test_df.end[i-1]:test_df.start[i]]
    list_content.append(content)
list_content.append(item_7_raw[test_df.end[len(test_df.end)-1]:len(item_7_raw)])
test_df["content"] = list_content


# Display the dataframe

#%%
test_df.to_csv("test_df.csv")
#%%
object_list = []
TAG_RE = re.compile(r'<[^>]+>')
TABLE_CONTENT_RE = re.compile(r'[0-9](.*)Table of Contents')

#%%
# first json object
first_part = item_7_raw[:test_df.iloc[0]['start']]
title = first_part[:(first_part.index('</'))]
title = remove_unnecessary_letter(title)
body = first_part[(first_part.index('</')):]
if("<P>" in body):
    body = body[:(body.index('<P>'))]
body = remove_unnecessary_letter(body)
json_object = {}
json_object["header"] = title
json_object["content"] = body
object_list.append(json_object)
#%%


for index, row in test_df.iterrows():

    json_object = {}
    json_object["header"] = remove_unnecessary_letter(row['header'])
    json_object["content"] = remove_unnecessary_letter(row['content'])

    object_list.append(json_object)



#%%
has_overview_title = False
common_title =["our company","the company","overview"]
checking = True
for i in range(len(object_list)):
    if (not checking):
        break
    for title in common_title:
        if title in object_list[i]["header"].lower():
            has_overview_title = True
            if(len(object_list[i]["content"])>0):
                print(object_list[i])
                checking = False
                break
            else:
                print(object_list[i+1])
                checking = False
                break

if(not has_overview_title):
    first_part = 0
    overview_content = ''
    while(len(overview_content)==0):
        object_overview = object_list[first_part]
        overview_content = object_overview["content"]
        first_part += 1
    print(object_list[first_part-1])
    
#%%
with open('header_content_Aarons_Inc.json', 'w', encoding='utf-8') as f:
    json.dump(object_list, f, ensure_ascii=True, indent=4)

