import codecs
import re
import pandas as pd
import spacy

def remove_unnecessary_letter(input_string):
    
    TAG_RE = re.compile(r'<[^>]+>')
    TABLE_CONTENT_RE = re.compile(r'[0-9]+\s+Table of Contents') 
    SPACE_RE = re.compile(r'(\s\s)+')
    list_remove_re = [TAG_RE,TABLE_CONTENT_RE,SPACE_RE]
    for remove_re in list_remove_re:
        input_string = re.sub(remove_re,'', input_string)
    
    remove_items = ['&#160;',"&nbsp;","\n","   "] 
    for item in remove_items:
        input_string = input_string.replace(item,' ')
    input_string = input_string.replace("&middot;","\n\t &middot;")
    input_string = input_string.strip()  
    return input_string

def generate_header_content(file_path):
    f=codecs.open(file_path, 'r')
    file_content = f.read()
    # Write the regex
    regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(7A|7)\.{0,1})|(>Item(7A|7)\.{0,1})|(>ITEM(\s|&#160;|&nbsp;)(7A|7)\.{0,1})|(>ITEM(7A|7)\.{0,1})')
    matches = regex.finditer(file_content)
    if(len(list(matches))==0):
        return ("This documents doesn't have item 7")
    
    # Create the dataframe
    matches = regex.finditer(file_content)
    test_df = pd.DataFrame([(x.group(), x.start(), x.end(),file_content[x.start()-10:x.end()]) for x in matches])

    test_df.columns = ['item', 'start', 'end','content']
    test_df['item'] = test_df.item.str.lower()

    # Get rid of unnesesary charcters from the dataframe
    test_df.replace('&#160;',' ',regex=True,inplace=True)
    test_df.replace('&nbsp;',' ',regex=True,inplace=True)
    test_df.replace(' ','',regex=True,inplace=True)
    test_df.replace('\.','',regex=True,inplace=True)
    test_df.replace('>','',regex=True,inplace=True)
    test_df.replace('\n','',regex=True,inplace=True)

    # Drop unnecessary row
    while(test_df.iloc[-1]['item'] == 'item7'):
        test_df = test_df[:-1]

    # Drop duplicates
    pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')
    # Set item as the dataframe index
    pos_dat.set_index('item', inplace=True)

    # get item 7
    item_7_raw = file_content[pos_dat['start'].loc['item7']:pos_dat['start'].loc['item7a']]
    print(item_7_raw)

    # Write the regex
    regex = re.compile(r'(<B><U>(.*)</U></B>)|(<B><I>(.*)</I></B>)|(<B>[^<]+</B>)|(<b>(.*)</b>)|(<b><u>(.*)</u></b>)|(<b><i>(.*)</i></b>)')

    # Use finditer to math the regex
    matches = regex.finditer(item_7_raw)
    # Create the dataframe
    if(len(list(matches))>0):
        matches = regex.finditer(item_7_raw)
        test_df = pd.DataFrame([( x.start(), x.end(),item_7_raw[x.start():x.end()]) for x in matches])
        test_df.columns = [ 'start', 'end','header']
    else:
        data = []
        regex = re.compile(r'(bold[^<]+</)')
        matches = regex.finditer(item_7_raw)
        test_df = pd.DataFrame(columns=[ 'start', 'end','header'])
        for match in matches:
            start_index = item_7_raw.index('>',match.start(),match.end())+1
            end_index = item_7_raw.index('</',start_index,match.end())
            new_row = {'start':start_index,'end':end_index,'header':item_7_raw[start_index:end_index]}
            data.append(new_row)
        test_df = pd.DataFrame(data)
    print("*"*10 )
    print(test_df)
    list_content =[]
    for i in range(1, len(test_df["start"])):
        content = item_7_raw[test_df.end[i-1]:test_df.start[i]]
        list_content.append(content)
    list_content.append(item_7_raw[test_df.end[len(test_df.end)-1]:len(item_7_raw)])
    test_df["content"] = list_content
    # first json object
    first_part = item_7_raw[:test_df.iloc[0]['start']]
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
    return (object_list)
        
def overview_extraction(object_list):
    has_overview_title = False
    common_title =["our company","the company","overview"]
    checking = True
    for i in range(len(object_list)):
        if (not checking):
            break
        for title in common_title:
            if title in object_list[i]["header"].lower():
                has_overview_title = True
                if(len(object_list[i]["content"])>0):
                    return (object_list[i])
                    
                else:
                    return(object_list[i+1])
    if(not has_overview_title):
        first_part = 0
        overview_content = ''
        while(len(overview_content)==0):
            object_overview = object_list[first_part]
            overview_content = object_overview["content"]
            first_part += 1
        return(object_list[first_part-1])
    
def performance_extraction(object_list):
    nlp = spacy.load("en_core_web_sm")
    max_ratio = 0
    performance = ""



    for item in object_list:
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
                performance = paragraph
                max_ratio = ratio
    return performance

def main():
    
    file_path = 'Data/NASDAQ/Applied Optoelectronics Inc/annual_report_2019-02-26_aaoi-20181231x10k.htm'
    file_path = 'Data/NASDAQ/Apple Inc/annual_report_2013-10-30_d590790d10k.htm'
    file_path = 'Data/NaN/Patriot Minefinders Inc/annual_report_2019-10-29_form-10k.htm' 
    file_path = 'Data/OTC/All American Sportpark Inc/annual_report_2015-03-30_aasp12-31201410k.htm' 
    file_path = 'Data/NaN/Ushealth Group Inc/annual_report_2005-03-09_f120410k.htm' 
    header_content_list = generate_header_content(file_path)
    print(overview_extraction(header_content_list))
    print(performance_extraction(header_content_list))

if __name__ == "__main__":
    main()
    