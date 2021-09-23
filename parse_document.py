# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 14:40:15 2021

@author: Emma Do
"""

#%%
import re
import requests
import unicodedata
from bs4 import BeautifulSoup
#%%
# text normalization
def restore_windows_1252_characters(restore_string):
    """
        Replace C1 control characters in the Unicode string s by the
        characters at the corresponding code points in Windows-1252,
        where possible.
    """

    def to_windows_1252(match):
        try:
            return bytes([ord(match.group(0))]).decode('windows-1252')
        except UnicodeDecodeError:
            # No character at the corresponding code point: remove it.
            return ''
        
    return re.sub(r'[\u0080-\u0099]', to_windows_1252, restore_string)
#%%
    
new_html_text = r"https://www.sec.gov/Archives/edgar/data/1166036/000110465904027382/0001104659-04-027382.txt"
headers = { 'User-Agent': 'Mozilla/5.0', }
response = requests.get(new_html_text,headers = headers)
soup = BeautifulSoup(response.content,'lxml')

#%%
master_filings_dict = {}

#define a unique key for each filing
accession_number = '0001104659-04-027382' 

# add the key to the dictionary and add a new level
master_filings_dict[accession_number]={}
master_filings_dict[accession_number]['sec_header_content'] = {}
master_filings_dict[accession_number]['filing_documents'] = None

#%%
# grab the sec-header document
sec_header_tag = soup.find('sec-header')
master_filings_dict[accession_number]['sec_header_content']['sec_header_code'] = sec_header_tag

#%%
# parse the document
# initialise master document dictionary
master_document_dict ={}
# loop through each document in the filing
for filing_document in soup.find_all('document'):
    # define document id
    document_id = filing_document.type.find(text=True, recursive = False).strip()
    
    #document sequence
    document_sequence = filing_document.sequence.find(text=True, recursive = False).strip()
    #document filename
    document_filename = filing_document.filename.find(text=True, recursive = False).strip()
    #document description
    document_description = filing_document.description.find(text=True, recursive = False).strip()
    
    #insert the key
    master_document_dict[document_id] = {}
    #add different parts of the document
    master_document_dict[document_id]['document_sequence'] = document_sequence
    master_document_dict[document_id]['document_filename'] = document_filename
    master_document_dict[document_id]['document_description'] = document_description
    
    # add the document content itself
    master_document_dict[document_id]['document_code'] = filing_document.extract()
    
    filing_doc_text = filing_document.find('text').extract()
    
    # get all the thematic breaks
    all_thematic_breaks = filing_doc_text.find_all('hr',{'width':'100%'})
    
    #convert all the breaks into a string
    all_thematic_breaks = [str(thematic_break) for thematic_break in all_thematic_breaks]
    
    #prep the document for being split
    filing_doc_string = str(filing_doc_text)
    
    if len(all_thematic_breaks)>0:
        # create our pattern
        regex_delimited_pattern = '|'.join(map(re.escape,all_thematic_breaks))
        
        # split the document along the thematic breaks
        split_filing_string = re.split(regex_delimited_pattern,filing_doc_string)
        
        #store the document in the dictionary
        master_document_dict[document_id]['pages_code']=split_filing_string
    else:
        master_document_dict[document_id]['pages_code']=[filing_doc_string]
        
    print('-'*50)
    print('The document {} was parsed.'.format(document_id))
    print('There was {} page(s) found.'.format(len(all_thematic_breaks)))

#Store the documents in the master_filing_dictionany
    
#%%
master_filings_dict[accession_number]['filing_documents']=  master_document_dict
