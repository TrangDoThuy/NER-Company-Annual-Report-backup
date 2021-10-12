# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 11:56:43 2021

@author: trang
"""
# -*- coding: utf-8 -*-

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
    
   
    list_remove_re = [TABLE_CONTENT_RE,SPACE_RE,TABLE_CONTENT_RE_2,TABLE_CONTENT_RE_3]
    input_string = re.sub(TAG_RE,'\n', input_string)
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
#file_path = 'Data/NYSE/Aarons Inc/annual_report_2014-02-24_a10k4q2013.htm'
file_path = 'Data/NASDAQ/Apple Inc/annual_report_2016-10-26_a201610-k9242016.htm' 
f=codecs.open(file_path, 'r')
file_content = f.read()
#print(file_content)
#%%

#%%
# Write the regex
regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(1A|2|1.)\.{0,1})|(>Item(1A|2|1.)\.{0,1})|(>(\s)+Item(\s|&#160;|&nbsp;)(1A|2|1.)\.{0,1})|(>(\s)+Item(1A|2|1.)\.{0,1})|(>ITEM(\s|&#160;|&nbsp;)(1A|2|1.)\.{0,1})|(>ITEM(1A|2|1.)\.{0,1})|(>(\s)+ITEM(\s|&#160;|&nbsp;)(1A|2|1.)\.{0,1})|(>(\s)+ITEM(1A|2|1.)\.{0,1})')

matches = regex.finditer(file_content)
# Write a for loop to print the matches
count = 0
for match in matches:
    count +=1
    print('*'*10)
    print(file_content[match.start():match.end()])
print(count)
if(count == 0):
    print("This documents doesnt have item business")

#%%
matches = regex.finditer(file_content)
# Create the dataframe
if(len(list(matches))>0):
    matches = regex.finditer(file_content)
    
    test_df = pd.DataFrame(columns=[ 'start', 'end','header'])
    data = []
    for match in matches:
        print(match)
        match_content = file_content[match.start():match.end()]
        start_index = match.start()
        header = file_content[match.start()+1:match.end()]
        header = remove_unnecessary_letter(header).lower()
        regex = re.compile('[^a-zA-Z0-9\s]')
        #First parameter is the replacement, second parameter is your input string
        header = regex.sub('', header) 
        
        print(header)
        if (header not in ["item 1","item 1a","item 2"]):
            continue
        new_row = {'start':match.start()+1,'end':match.end(),'header':header}
        data.append(new_row)
    test_df = pd.DataFrame(data)
print(test_df)
#%%

i = len(test_df["header"])-1
while (i>=0):
    print(test_df["header"][i])
    if("item 2" in test_df["header"][i].lower()):
        test_df = test_df[:(i+1)]
        break
    else:
        i -= 1
print("after remove item 2")
print(test_df)
    
if("item 1a" in list(test_df["header"])):
    i = len(test_df["header"])-1
    while (i>=0):
        print(test_df["header"][i])
        if("item 1a" in test_df["header"][i].lower()):
            test_df = test_df[:(i+1)]
            break
        else:
            i -= 1
            
print("after remove item 1a")
print(test_df)
#%%
# remove item 2 in the datafram
for index, row in test_df.iterrows():
    if row['header'] == "item 2":
        test_df.drop(index, inplace=True)
        
#%%
print(test_df)
    
    
#%%
# Drop duplicates
pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['header'], keep='last')
# Set item as the dataframe index
pos_dat.set_index('header', inplace=True)
print(pos_dat)
#%%
# Get Item 1
item_1_raw = file_content[pos_dat['start'][0]:pos_dat['start'][1]]
# remove uncenessary break line:
item_1_raw = item_1_raw.replace('.\n',"hihi")
item_1_raw = item_1_raw.replace('\n'," ")
item_1_raw = item_1_raw.replace("hihi",'.\n')

print(item_1_raw[:1000])

#%%
#remove table
count_table = 0
while "<TABLE" in item_1_raw:
    count_table +=1
    start_index = item_1_raw.index("<TABLE")
    if "</TABLE>" in item_1_raw[start_index:]:
        end_index = item_1_raw.index("</TABLE>",start_index)
        #item_1_raw = item_1_raw[:start_index]+item_1_raw[end_index+8:] 
        item_1_raw = item_1_raw.replace(item_1_raw[start_index:(end_index+8)],'')
    else:
        break
#%%


# Write the regex
regex = re.compile(r'(<B><U>[^<]+</U></B>)|(<B><I>(.*)</I></B>)|(<B>(.*)</B>)|(<b>(.*)</b>)|(<b><u>(.*)</u></b>)|(<b><i>(.*)</i></b>)')

# Use finditer to math the regex
matches = regex.finditer(item_1_raw)
# Create the dataframe
if(len(list(matches))>0):
    matches = regex.finditer(item_1_raw)
    test_df = pd.DataFrame(columns=[ 'start', 'end','header'])
    for match in matches:
        start_index = item_1_raw.index('>',match.start(),match.end())+1
        end_index = item_1_raw.index('</',start_index,match.end())
        header = item_1_raw[start_index:end_index]
        print(header)
        header = remove_unnecessary_letter(header).lower()
        new_row = {'start':start_index,'end':end_index,'header':header}
        data.append(new_row)
    test_df = pd.DataFrame(data)
else:
    data = []
    regex = re.compile(r'(bold[^<]+</)')
    matches = regex.finditer(item_1_raw)
    test_df = pd.DataFrame(columns=[ 'start', 'end','header'])
    for match in matches:
        start_index = item_1_raw.index('>',match.start(),match.end())+1
        end_index = item_1_raw.index('</',start_index,match.end())
        header = item_1_raw[start_index:end_index]
        header = remove_unnecessary_letter(header).lower()
        new_row = {'start':start_index,'end':end_index,'header':header}
        data.append(new_row)
    test_df = pd.DataFrame(data)
print("*"*10 )
print(test_df)
list_content =[]
for i in range(1, len(test_df["start"])):
    content = item_1_raw[test_df.end[i-1]:test_df.start[i]]
    list_content.append(content)
list_content.append(item_1_raw[test_df.end[len(test_df.end)-1]:len(item_1_raw)])
test_df["content"] = list_content
# first json object
first_part = item_1_raw[:test_df.iloc[0]['start']]
title = first_part[:(first_part.index('</'))]
title = remove_unnecessary_letter(title)
body = first_part[(first_part.index('</')):]
if("<P>" in body):
    body = body[:(body.index('<P>'))]
body = remove_unnecessary_letter(body)
object_list = []
json_object = {}
json_object["header"] = title
json_object["content"] = body
object_list.append(json_object)

for index, row in test_df.iterrows():

    json_object = {}
    json_object["header"] = remove_unnecessary_letter(row['header'])
    json_object["content"] = remove_unnecessary_letter(row['content'])

    object_list.append(json_object)
#%%
# extract business review:
has_business_review_title = False
for i in range(1,len(object_list)):
    
    if (("business" in object_list[i]["header"].lower()) and (len(object_list[i]["header"].lower())>10)):
        #print()
        has_business_review_title = True
        if(len(object_list[i]["content"])>0):
            #print(object_list[i])
            business_review = object_list[i]
            break
        else:
            #print(object_list[i+1])
            business_review = object_list[i+1]
            break
#%%
common_title =["our company","the company","overview"]
not_true_title = ["industry overview"]
checking = True
has_overview_title = False
for i in range(len(object_list)):
    if (not checking):
        break
    if any(title in object_list[i]["header"].lower() for title in not_true_title):
        continue
    for title in common_title:
        if title in object_list[i]["header"].lower():            
            has_overview_title = True
            while((i<len(object_list))and(len(object_list[i]["content"])==0)):
                i +=1
            overview = object_list[i]["content"]
            if(not has_business_review_title):
                i +=1
                while((i<len(object_list))and(len(object_list[i]["content"])==0)):
                    i +=1
                business_review =  object_list[i]["content"]  
            checking = False
            break

if(not has_overview_title):
    i = 0
    overview_content = ''
    while(len(object_list[i]["content"])==0):
        i +=1
    overview = object_list[i]["content"]
    i +=1
    while(len(object_list[i]["content"])==0):
        i +=1
    business_review =  object_list[i]["content"] 

#%%
print("&"*15)
print("Overview")
print(overview)
print("*"*10)
print("Business Review")
print(business_review)

    
#%%
with open('header_content_Aarons_Inc.json', 'w', encoding='utf-8') as f:
    json.dump(object_list, f, ensure_ascii=True, indent=4)