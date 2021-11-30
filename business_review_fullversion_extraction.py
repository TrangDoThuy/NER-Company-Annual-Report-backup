# -*- coding: utf-8 -*-
def info_extraction(): 
    import codecs
    import re
    import pandas as pd
    import json
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
            input_string = re.sub(remove_re,' ', input_string)
            
        input_string = input_string.replace('.\n',"hihi")
        
        remove_items = ["&nbsp;","&nbsp","nbsp;","nbsp","   ","\n"] 
        for item in remove_items:
            input_string = input_string.replace(item," ")
        input_string = input_string.replace("tem&#160;","tem ")
        input_string = input_string.replace("&middot;","\n\t &middot;")
        input_string = input_string.replace("hihi",'.\n')
        input_string = input_string.strip()  
        return input_string
    
    #%%
    def extract_item_1_business(file_path):
        f=codecs.open(file_path, 'r')
        file_content = f.read()
        regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(1A|2|1.)\.{0,1})|(>Item(1A|2|1.)\.{0,1})|(>(\s)+Item(\s|&#160;|&nbsp;)(1A|2|1.)\.{0,1})|(>(\s)+Item(1A|2|1.)\.{0,1})|(>ITEM(\s|&#160;|&nbsp;)(1A|2|1.)\.{0,1})|(>ITEM(1A|2|1.)\.{0,1})|(>(\s)+ITEM(\s|&#160;|&nbsp;)(1A|2|1.)\.{0,1})|(>(\s)+ITEM(1A|2|1.)\.{0,1})')
        matches = regex.finditer(file_content)
        item_1_raw = ""
        # Create the dataframe
        if(len(list(matches))>0):
            matches = regex.finditer(file_content)
            test_df = pd.DataFrame(columns=[ 'start', 'end','header'])
            data = []
            for match in matches:
                header = file_content[match.start()+1:match.end()]
                header = remove_unnecessary_letter(header).lower()
                regex = re.compile('[^a-zA-Z0-9\s]')
                #First parameter is the replacement, second parameter is your input string
                header = regex.sub('', header) 
                if (header not in ["item 1","item 1a","item 2"]):
                    continue
                new_row = {'start':match.start()+1,'end':match.end(),'header':header}
                data.append(new_row)
            test_df = pd.DataFrame(data)
            i = len(test_df["header"])-1
            while (i>=0):
                if("item 2" in test_df["header"][i].lower()):
                    test_df = test_df[:(i+1)]
                    break
                else:
                    i -= 1
            if("item 1a" in list(test_df["header"])):
                i = len(test_df["header"])-1
                while (i>=0):
                    if("item 1a" in test_df["header"][i].lower()):
                        test_df = test_df[:(i+1)]
                        break
                    else:
                        i -= 1
            for index, row in test_df.iterrows():
                if row['header'] == "item 2":
                    test_df.drop(index, inplace=True)            
            # Drop duplicates
            pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['header'], keep='last')
            # Set item as the dataframe index
            pos_dat.set_index('header', inplace=True)
            # Get Item 1
            item_1_raw = file_content[pos_dat['start'][0]:pos_dat['start'][1]]
            # remove uncenessary break line:
            item_1_raw = item_1_raw.replace('.\n',"hihi")
            item_1_raw = item_1_raw.replace('\n'," ")
            item_1_raw = item_1_raw.replace("hihi",'.\n')
        return item_1_raw
    
    #%%
    def extract_item_7_financial_analyse(file_path):
        f=codecs.open(file_path, 'r')
        file_content = f.read()
        regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(7A|7|7.)\.{0,1})|(>Item(7A|8|7.)\.{0,1})|(>(\s)+Item(\s|&#160;|&nbsp;)(7A|8|7.)\.{0,1})|(>(\s)+Item(7A|8|7.)\.{0,1})|(>ITEM(\s|&#160;|&nbsp;)(7A|8|7.)\.{0,1})|(>ITEM(7A|8|7.)\.{0,1})|(>(\s)+ITEM(\s|&#160;|&nbsp;)(7A|8|7.)\.{0,1})|(>(\s)+ITEM(7A|8|7.)\.{0,1})')
        matches = regex.finditer(file_content)
        item_7_raw = ""
        # Create the dataframe
        if(len(list(matches))>0):
            matches = regex.finditer(file_content)
            test_df = pd.DataFrame(columns=[ 'start', 'end','header'])
            data = []
            for match in matches:
                header = file_content[match.start()+1:match.end()]
                header = remove_unnecessary_letter(header).lower()
                regex = re.compile('[^a-zA-Z0-9\s]')
                #First parameter is the replacement, second parameter is your input string
                header = regex.sub('', header) 
                if (header not in ["item 7","item 7a","item 8"]):
                    continue
                new_row = {'start':match.start()+1,'end':match.end(),'header':header}
                data.append(new_row)
            test_df = pd.DataFrame(data)
            i = len(test_df["header"])-1
            while (i>=0):
                if("item 2" in test_df["header"][i].lower()):
                    test_df = test_df[:(i+1)]
                    break
                else:
                    i -= 1
            if("item 1a" in list(test_df["header"])):
                i = len(test_df["header"])-1
                while (i>=0):
                    if("item 1a" in test_df["header"][i].lower()):
                        test_df = test_df[:(i+1)]
                        break
                    else:
                        i -= 1
            for index, row in test_df.iterrows():
                if row['header'] == "item 2":
                    test_df.drop(index, inplace=True)            
            # Drop duplicates
            pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['header'], keep='last')
            # Set item as the dataframe index
            pos_dat.set_index('header', inplace=True)
            # Get Item 1
            item_7_raw = file_content[pos_dat['start'][0]:pos_dat['start'][1]]
            # remove uncenessary break line:
            item_7_raw = item_7_raw.replace('.\n',"hihi")
            item_7_raw = item_7_raw.replace('\n'," ")
            item_7_raw = item_7_raw.replace("hihi",'.\n')
        return item_7_raw
    #%%
    def generate_header_content(raw_text):
        while "<TABLE" in raw_text:
            start_index = raw_text.index("<TABLE")
            if "</TABLE>" in raw_text[start_index:]:
                end_index = raw_text.index("</TABLE>",start_index)
                #raw_text = raw_text[:start_index]+raw_text[end_index+8:] 
                raw_text = raw_text.replace(raw_text[start_index:(end_index+8)],' ')
            else:
                break
            
        while "<table" in raw_text:
            start_index = raw_text.index("<table")
            if "</table>" in raw_text[start_index:]:
                end_index = raw_text.index("</table>",start_index)
                #raw_text = raw_text[:start_index]+raw_text[end_index+8:] 
                raw_text = raw_text.replace(raw_text[start_index:(end_index+8)],' ')
            else:
                break
        
        # Write the regex
        regex = re.compile(r'(<B><U>[^<]+</U></B>)|(<B><I>(.*)</I></B>)|(<B>(.*)</B>)|(<B>[^<]+</B>)|(<b>(.*)</b>)|(<b><u>(.*)</u></b>)|(<b><i>(.*)</i></b>)|(bold[^<]+</)|(font-weight:700[^<]+</)|(font-weight: 700[^<]+</)')
        # Use finditer to math the regex
        matches = regex.finditer(raw_text)
        # Create the dataframe
        data = []
        matches = regex.finditer(raw_text)
        test_df = pd.DataFrame(columns=[ 'start', 'end','header'])
        for match in matches:
            start_index = raw_text.index('>',match.start(),match.end())+1
            end_index = raw_text.index('</',start_index,match.end())
            header = raw_text[start_index:end_index]
            header = remove_unnecessary_letter(header).lower()
            new_row = {'start':start_index,'end':end_index,'header':header}
            data.append(new_row)
        test_df = pd.DataFrame(data)
        
        list_content =[]
        print("------------")
        for i in range(1, len(test_df["start"])):
            content = raw_text[test_df.end[i-1]:test_df.start[i]]
            list_content.append(content)
        list_content.append(raw_text[test_df.end[len(test_df.end)-1]:len(raw_text)])
        test_df["content"] = list_content
        # first json object
        first_part = raw_text[:test_df.iloc[0]['start']]
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
        with open('header_content.json', 'w', encoding='utf-8') as f:
            json.dump(object_list, f, ensure_ascii=True, indent=4)
        return object_list
    #%%
    def extract_overview_and_business_review(object_list):
        # extract business review:
        has_business_review_title = False
        for i in range(1,len(object_list)):
            
            if (("business" in object_list[i]["header"].lower()) and (len(object_list[i]["header"].lower())>10)):
                #print()
                has_business_review_title = True
                if(len(object_list[i]["content"])>0):
                    #print(object_list[i])
                    business_review = object_list[i]["content"]
                    break
                else:
                    #print(object_list[i+1])
                    business_review = object_list[i+1]["content"]
                    break
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
            while((i<len(object_list)-1) and len(object_list[i]["content"])==0):
                i +=1
            overview = object_list[i]["content"]
            i +=1
            while((i<len(object_list)-1) and len(object_list[i]["content"])==0):
                i +=1
            business_review =  object_list[i]["content"] 
        return overview,business_review
    
    def performance_extraction(object_list):
        nlp = spacy.load("en_core_web_sm")
        max_ratio = 0
        performance = ""
        for item in object_list:
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
                ratio = (count_money*count_date*count_revenue_income)/len(paragraph)
                if(ratio>max_ratio):
                    performance = paragraph
                    max_ratio = ratio
        return performance
    #%%
    def get_subject_phrase(doc):
        for token in doc:
            if ("subj" in token.dep_):
                subtree = list(token.subtree)
                start = subtree[0].i
                end = subtree[-1].i + 1
                return doc[start:end]
    #%%
    def prospects_extraction(object_list):
        future_word_list = ["anticipates","believes","feels","expects","estimates","seeks","strives","plans","intends",
                            "outlook","forecast","position","target","mission","assume","achievable","potential",
                            "strategy","goal","aspiration","outcome","continue","remain","maintain",
                            "trend","objective","will ","would","should","could","might"," can ","may"]
       
        current_count = 0
        max_count = 0
        prospects_paragraph = []
        for item in object_list:
            content = item['content']
            if(len(content)==0):
                continue
            paragraphs = content.split("\n")
            for paragraph in paragraphs:
                if(("forward-looking statements" in paragraph)):
                    continue
                doc = nlp(paragraph)
                sentences = list(doc.sents)
                for i in range(len(sentences)):
                    sentence = sentences[i]
                    
                    subject_phrase = get_subject_phrase(nlp(sentence.text))
                    if(str(subject_phrase).lower() not in ["we","the company"]):
                        continue
                    elif(("will be" in sentence.text)or("if" in sentence.text)):
                        continue
                    current_count = 0
                    current_word_list=[]
                    for word in future_word_list:
                        current_count += sentence.text.count(word)
                        if(sentence.text.count(word)>0):
                            current_word_list.append(word)
                    if(current_count > max_count):
                        max_count = current_count
                        if((("their" in sentence.text)or("such" in sentence.text))and(i>0)):
                            sentence_content = sentences[i-1].text +" "+  sentence.text
                        else:
                            sentence_content = sentence.text
                        prospects_paragraph.append(sentence_content)
        print('&'*10)
        return prospects_paragraph  
    #%%
    def fine_tune_paragraph(paragraph):
        # sub_words = ["See Note","following table"]
        # for sub_word in sub_words:
        #     if(sub_word in paragraph):
        #         finding_point = paragraph.index(sub_word)
        #         starting_point = paragraph.rindex(".", 0, finding_point)
        #         if("." in paragraph[starting_point+1:]):
        #             ending_point = paragraph.index(".",starting_point+2)
        #             paragraph = paragraph.replace(paragraph[starting_point:ending_point],"")
        #         else:
        #             paragraph = paragraph[:starting_point+1]
        map_quotes = [{
            "long_name":"&rsquo;",
            "short_name":"\'",
        },
        { "long_name":"&#146;",
            "short_name":"\'",
        },
        {
            "long_name":"&ldquo;",
            "short_name":"\"",
        },
        {
            "long_name":"&rdquo;",
            "short_name":"\"",
        },
        {
            "long_name":"&#8220;",
            "short_name":"\"",
        },
        {
            "long_name":"&#8221;",
            "short_name":"\"",
        },
        {
            "long_name":"&#147;",
            "short_name":"\"",
        },
        {
            "long_name":"&#148;",
            "short_name":"\"",
        },
        {
            "long_name":"&ndash;",
            "short_name":"–",
        },
        {
            "long_name":"&amp;",
            "short_name":"&",
        },
        ]
        for quote in map_quotes:
            paragraph = paragraph.replace(quote["long_name"],quote["short_name"])
        sentence_list = paragraph.replace('. ','.  ').replace('\n','  ').split("  ")
        return sentence_list    
    #%%
    
    #file_path = 'Data/NYSE/Alcoa Inc/annual_report_2009-02-17_d10k.htm'
    file_path = 'Data/NYSE/Agilent Technologies Inc/annual_report_2020-12-18_a-20201031.htm'
    #file_path = 'Data/NYSE/Agilent Technologies Inc/annual_report_2010-12-20_a2201423z10-k.htm'
    #file_path = 'Data/NASDAQ/Sinocoking Coal & Coke Chemical Industries Inc/annual_report_2013-09-30_v355550_10k.htm'
    #file_path = 'Data/OTCBB/Auburn Bancorp Inc/annual_report_2010-09-28_t68978_10k.htm'
    #file_path = 'Data/NaN/Asset Acceptance Capital Corp/annual_report_2010-03-12_d10k.htm'
    #file_path = 'Data/OTC/All American Gold Corp/annual_report_2013-11-06_form10ka.htm' 
    ###file_path = 'Data/OTC/Aaipharma Inc/annual_report_2004-06-15_g87794e10vk.htm'
    #file_path = 'Data/OTC/Avantair Inc/annual_report_2010-09-28_v197483_10k.htm'
    #file_path = 'Data/NASDAQ/American Airlines Group Inc/annual_report_2016-02-24_d78287d10k.htm'
    #file_path = 'Data/NASDAQ/American Airlines Group Inc/annual_report_2020-02-19_a10k123119.htm'
    #file_path = 'Data/OTC/Altisource Asset Management Corp/annual_report_2020-02-28_aamc10k12312019.htm'
    #file_path = 'Data/NASDAQ/Atlantic American Corp/annual_report_2010-03-26_g22608e10vk.htm'
    #file_path = 'Data/NYSE/Aarons Inc/annual_report_2014-02-24_a10k4q2013.htm'
    #file_path = 'Data/NASDAQ/Apple Inc/annual_report_2016-10-26_a201610-k9242016.htm'
    raw_text_item_1 = extract_item_1_business(file_path)
    object_list_item_1 = generate_header_content(raw_text_item_1)
    overview, business_review =  extract_overview_and_business_review(object_list_item_1)
    json_object = {}
    
    print("&"*15)
    print("Overview")
    overview = fine_tune_paragraph(overview)
    json_object["overview"] = overview
    for sen in overview:
        print(sen)
        print("\n")
    # print("*"*10)
    # print("Business Review")
    # business_review = fine_tune_paragraph(business_review)
    # json_object["business_review"] = business_review
    # print(business_review)
    # print('*'*10)
    
    # raw_text_item_7 = extract_item_7_financial_analyse(file_path)
    
    # object_list_item_7 = generate_header_content(raw_text_item_7)
    # performance = performance_extraction(object_list_item_7)
    # print("Performace:")
    # performance = fine_tune_paragraph(performance)
    # json_object["performance"] = performance
    # print(performance)
    # print('*'*10)
    # print("Prospect: ")
    
    # prospect_paragraph = ""
    # for item in prospects_extraction(object_list_item_7):
    #     prospect_paragraph = prospect_paragraph+item+"  "
        
    # prospect_paragraph = fine_tune_paragraph(prospect_paragraph)
    # print(prospect_paragraph)
    # json_object["prospects"] = prospect_paragraph
    with open('flask_NLP/flask_NER/extration_Asset_2010.json', 'w', encoding='utf-8') as f:
        json.dump(json_object, f, ensure_ascii=False, indent=4)  
#%%
info_extraction()
    
        
