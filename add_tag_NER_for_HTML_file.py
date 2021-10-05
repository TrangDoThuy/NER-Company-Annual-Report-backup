

import os
import re
from boilerpy3 import extractors
import spacy
from spacy import displacy
from random import randrange
nlp = spacy.load("en_core_web_sm")
import ahocorasick
A = ahocorasick.Automaton()
import json
#%%

# Condenses all repeating newline characters into one single newline character
def condense_newline(text):
    return '\n'.join([p for p in re.split('\n|\r', text) if len(p) > 0])

# Returns the text from a HTML file
def parse_html(html_path):
    # Text extraction with boilerpy3
    html_extractor = extractors.ArticleExtractor()
    return condense_newline(html_extractor.get_content_from_file(html_path))


html_path = ("Data/NYSE/Alcoa Inc/annual_report_2004-02-27_d10k.htm")
new_html_path = ("Data/NYSE/Alcoa Inc/new_annual_report_2004-02-27_d10k.htm")
text = parse_html(html_path)
#%%
print(text)
doc = nlp(text)
#doc = nlp("I bought some apples near Apple Store")

#%%
color_dict = dict()
count = randrange(10)
color_list = ["#ca9bf7","#ff694f","#cb99c9","#befd73","#b39eb5","#aa9499","#89cff0"]

ent_text_dict = dict()


for ent in doc.ents:
    if(ent.text.isnumeric()):
        continue
    if((ent.label_ =="CARDINAL") or (ent.label == "ORDINAL")):
        continue
    text_item = " "+ent.text+" "
    print (text_item, ent.label_)
    if(ent.label_ not in color_dict):
        color_dict[ent.label_] = color_list[count % len(color_list)]
        count +=1
    ent_text_dict[text_item] = [ent.label_,color_dict[ent.label_]]

#%%
import codecs
f=codecs.open(html_path, 'r')
html_file = f.read()
print(html_file[1000:])
#%%

start_index = 0

index = html_file.find("<BODY",start_index)
if(index != -1):
    start_index = index
index = html_file.find(">",start_index)
if(index != -1):
    start_index = index
    html_file = html_file[:(index+1)]+"<DIV class=\"entities\" style=\"line-height: 2.5; direction: ltr\">"+html_file[(index+1):]

index = html_file.find("</BODY>",start_index)
if(index != -1):
    start_index = index
    html_file = html_file[:index]+"</DIV>"+html_file[index:]

#%%
for idx, key in enumerate(ent_text_dict.keys()):    
    A.add_word(key, (idx, key))
A.make_automaton()

json_object={}
item_list =[]

for end_index, (insert_order, text_item) in A.iter(html_file):
    item_object = {}
    item_object["text"] = text_item
    
    print("*"*10)
    print(text_item)
    index = end_index - len(text_item) + 1
    item_object["start_index"] = index
    item_object["end_index"] = end_index
    item_object["color"] = ent_text_dict[text_item][1]
    item_object["label"]= ent_text_dict[text_item][0]
    item_list.append(item_object) 
json_object["list"] = item_list
#%%
shift_amount = 0
for item_object in item_list:
    index = item_object["start_index"]+shift_amount
    new_text = "<mark class=\"entity\" style=\"background:"+item_object["color"]+";padding: 0.45em 0.6em;margin: 0 0.25em;line-height: 1;border-radius: 0.35em;\">"+item_object["text"]+"<span style=\"font-size: 0.8em;font-weight: bold;line-height: 1;border-radius: 0.35em;vertical-align: middle;margin-left: 0.5rem;\">"+item_object["label"]+"</span></mark>"
    
    html_file = html_file[:index]+new_text+html_file[(index+len(item_object["text"])):]
    shift_amount += (len(new_text)-len(item_object["text"]))

with open(new_html_path,'wb') as f:
    f.write(html_file.encode())



