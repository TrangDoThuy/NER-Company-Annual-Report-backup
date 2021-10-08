# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:34:53 2021

@author: trang
"""
import json
import spacy
nlp = spacy.load("en_core_web_sm")
 
# Opening JSON file
f = open('header_content_Aarons_Inc.json',)
 
# returns JSON object as
# a dictionary
data = json.load(f)
 
# Iterating through the json
# list
max_ratio = 0



for item in data:
    print('*'*10)
    content = item['content']
    if(len(content)==0):
        continue
    paragraphs = content.split("\n")
    for paragraph in paragraphs:
        
        doc = nlp(paragraph)
        count_money = 0
        count_date = 0
        count_revenue_income = 0
        for ent in doc.ents:
            if(ent.label_=="MONEY"):
                count_money+=1
            if(ent.label_ == "DATE"):
                count_date+=1
        count_revenue_income += paragraph.lower().count('revenue')
        count_revenue_income += paragraph.lower().count('income')
        count_revenue_income -= paragraph.lower().count('fee')
        count_revenue_income -= paragraph.lower().count('expenses')
        count_revenue_income -= paragraph.lower().count('tax')
        ratio = (count_money*count_date*count_revenue_income+2*count_revenue_income)/len(paragraph)
        if(ratio>max_ratio):
            print(paragraph)
            max_ratio = ratio

 
# Closing file
f.close()