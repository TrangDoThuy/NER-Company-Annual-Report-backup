
import os
import re
from boilerpy3 import extractors
import spacy
from spacy import displacy
from random import randrange
nlp = spacy.load("en_core_web_sm")
#%%

# Condenses all repeating newline characters into one single newline character
def condense_newline(text):
    return '\n'.join([p for p in re.split('\n|\r', text) if len(p) > 0])

# Returns the text from a HTML file
def parse_html(html_path):
    # Text extraction with boilerpy3
    html_extractor = extractors.ArticleExtractor()
    return condense_newline(html_extractor.get_content_from_file(html_path))


html_path = ("Data/NYSE/Agilent Technologies Inc/annual_report_2002-02-01_f78349a1e10-ka.htm")
new_html_path = ("Data/NYSE/Agilent Technologies Inc/new_annual_report_2002-02-01_f78349a1e10-ka.htm")
text = parse_html(html_path)
#%%
print(text)
doc = nlp(text)
#doc = nlp("I bought some apples near Apple Store")

#%%
color_dict = dict()
count = randrange(10)
color_list = ["#ca9bf7","#ff694f","#cb99c9","#befd73","#b39eb5","#aa9499","#89cff0"]

for ent in doc.ents:
    print (ent.text, ent.label_)
    if(ent.label_ not in color_dict):
        color_dict[ent.label_] = color_list[count % len(color_list)]
        count +=1


#%%
print(len(set(doc.ents)))
#%%
displacy.render(doc, style="ent")
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
start_index = 0
for ent in doc.ents:
    print (ent.text, ent.label_,color_dict[ent.label_])
    index = html_file.find(ent.text,start_index)
    if(index != -1):
        html_file = html_file[:index]+"<mark class=\"entity\" style=\"background:"+color_dict[ent.label_]+";padding: 0.45em 0.6em;margin: 0 0.25em;line-height: 1;border-radius: 0.35em;\">"+ent.text+"<span style=\"font-size: 0.8em;font-weight: bold;line-height: 1;border-radius: 0.35em;vertical-align: middle;margin-left: 0.5rem;\">"+ent.label_+"</span></mark>"+html_file[(index+len(ent.text)):]
        start_index = index

with open(new_html_path,'wb') as f:
    f.write(html_file.encode())

