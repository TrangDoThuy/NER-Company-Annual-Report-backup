# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:55:06 2021

@author: trang
"""

import codecs
from bs4 import BeautifulSoup
import re
import pandas as pd
#%%
file_path = 'Data/NYSE/Alcoa Inc/annual_report_2009-02-17_d10k.htm'
f=codecs.open(file_path, 'r')



file_content = f.read()

print(file_content[:1000])
#%%
# Write the regex
regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(7A|7)\.{0,1})|(ITEM\s(7A|7))')

# Use finditer to math the regex
matches = regex.finditer(file_content)

# Write a for loop to print the matches
for match in matches:
    print(match)
#%%
matches = regex.finditer(file_content)
# Create the dataframe
test_df = pd.DataFrame([(x.group(), x.start(), x.end(),file_content[x.start():x.end()]) for x in matches])

test_df.columns = ['item', 'start', 'end','content']
test_df['item'] = test_df.item.str.lower()

# Display the dataframe
print(test_df.head())
#%%
# Get rid of unnesesary charcters from the dataframe
test_df.replace('&#160;',' ',regex=True,inplace=True)
test_df.replace('&nbsp;',' ',regex=True,inplace=True)
test_df.replace(' ','',regex=True,inplace=True)
test_df.replace('\.','',regex=True,inplace=True)
test_df.replace('>','',regex=True,inplace=True)

# display the dataframe
print(test_df.head())
#%%
# Drop duplicates
pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')
# Set item as the dataframe index
pos_dat.set_index('item', inplace=True)
# Display the dataframe
print(pos_dat)
#%%
# Get Item 7
item_7_raw = file_content[pos_dat['start'].loc['item7']:pos_dat['start'].loc['item7a']]
#%%
### First convert the raw text we have to exrtacted to BeautifulSoup object 
item_7_content = BeautifulSoup(item_7_raw, 'lxml')
### By just applying .pretiffy() we see that raw text start to look oragnized, as BeautifulSoup
### apply indentation according to the HTML Tag tree structure
print(item_7_content.prettify()[0:1000])
#%%

### Our goal is though to remove html tags and see the content
### Method get_text() is what we need, \n\n is optional, I just added this to read text 
### more cleanly, it's basically new line character between sections. 
temp_result = item_7_content.get_text("hihi")[:2000]
for item in temp_result.split("hihi"):
    print('-'*10)
    print(item)