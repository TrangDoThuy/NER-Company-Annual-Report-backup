# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 12:27:49 2021

@author: trang
"""
import codecs
from bs4 import BeautifulSoup
import re

file_directory = "static/Data/OTC/All American Gold Corp/annual_report_2012-08-22_form10k.htm"

soup = BeautifulSoup(open(file_directory, 'r'), 'html.parser')
body = soup.body
body = soup.find('body')

children_count = len(body.contents)
while(children_count == 1):
    body = body.contents[0]
    children_count = len(body.contents)
document = str(body)
#print(document)

if(document.find("pagination__item")== -1):
    
    # <title>a-20201031</title></head><body>
    start_body = document.find("<body")
    start_body_index = document.find(">",start_body)+1
    # </body></html>
    end_body_index = document.find("</body>",start_body_index )

    if(document.find("pagination__list col-md-4 col-md-offset-4")== -1):
        if(children_count>1):
            # add whole div for pagination
            whole_div = "<div id=\"pagination-1\" class=\"pagination__list col-md-4 col-md-offset-4\"><div class=\"pagination__item\">"
            document = document[:start_body_index]+ whole_div +document[start_body_index:end_body_index]+"</div></div></body>"
        else:
            sub_start = document.find(">",start_body_index)+1
            whole_div = "<div id=\"pagination-1\" class=\"pagination__list col-md-4 col-md-offset-4\"><div class=\"pagination__item\">"
            document = document[:sub_start]+ whole_div +document[sub_start:end_body_index]+"</div></div></body>"
        
    # replace horizontal line by page-break
    regex = re.compile(r'<hr[^>]+>')
    matches = list(regex.finditer(document))
    replace_paginate = "</div><div class=\"pagination__item\">"
    break_page_list = ["<!-- Field: /Page -->"]
    if len(matches)>0:
        for match in matches:
            break_page = document[match.start():match.end()]
            if break_page not in break_page_list:
                break_page_list.append(break_page)
                 
    for break_page in break_page_list:
        document = document.replace(break_page,replace_paginate)

    Html_file= open("static/all_america_annual_report_2012-08-22_form10k.htm","w", encoding="utf-8")
    Html_file.write(document)
    Html_file.close()
