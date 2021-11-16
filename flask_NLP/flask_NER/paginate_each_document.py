# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 12:27:49 2021

@author: trang
"""
import codecs
from bs4 import BeautifulSoup

file_directory = "static/Data/NYSE/Agilent Technologies Inc/annual_report_2018-12-20_a-10312018x10k.htm"

soup = BeautifulSoup(open(file_directory, 'r'), 'html.parser')
body = soup.body
body = soup.find('body')

children_count = len(body.contents)
while(children_count == 1):
    body = body.contents[0]
    children_count = len(body.contents)
document = str(body)

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
    break_page = "<hr style=\"page-break-after: always\" />"
    break_page_2 = "<hr style=\"page-break-after:always\"/>"
    break_page_3 = "<hr style=\"page-break-after:always\"></hr>"
    replace_paginate = "</div><div class=\"pagination__item\">"

    document = document.replace(break_page,replace_paginate)
    document = document.replace(break_page_2,replace_paginate)
    document = document.replace(break_page_3,replace_paginate)

    Html_file= open("static/annual_report_2018-12-20_a-10312018x10k.htm","w", encoding="utf-8")
    Html_file.write(document)
    Html_file.close()
