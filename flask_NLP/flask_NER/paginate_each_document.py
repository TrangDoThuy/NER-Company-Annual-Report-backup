# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 12:27:49 2021

@author: trang
"""
import codecs
f=codecs.open("static/Data/NYSE/Agilent Technologies Inc/annual_report_2020-12-18_a-20201031.htm", 'r')

document = f.read()
# <title>a-20201031</title></head><body>
start_body_index = document.find("<body>")+6
# </body></html>
end_body_index = document.find("</body>",start_body_index )

# add whole div for pagination
if(document.find("pagination__list col-md-4 col-md-offset-4")== -1):
    whole_div = "<div id=\"pagination-1\" class=\"pagination__list col-md-4 col-md-offset-4\"><div class=\"pagination__item\">"
    document = document[:start_body_index]+ whole_div +document[start_body_index:end_body_index]+"</div></div></body>"
break_page = "<hr style=\"page-break-after: always\" />"
break_page_2 = "<hr style=\"page-break-after:always\"/>"
replace_paginate = "</div><div class=\"pagination__item\">"

document = document.replace(break_page,replace_paginate)
document = document.replace(break_page_2,replace_paginate)
#print(document)

Html_file= open("static/Data/NYSE/Agilent Technologies Inc/annual_report_2020-12-18_a-20201031.htm","w")
Html_file.write(document)
Html_file.close()
