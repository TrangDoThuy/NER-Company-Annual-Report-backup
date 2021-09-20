import os
import pandas as pd

# List of years to be searched
years = [2000 + x for x in range(6,21)]

# List of quarters to be searched
quarters = ['QTR1', 'QTR2', 'QTR3', 'QTR4']

# The absolute path to the folder for saving the index files 
base_path = 'C:/Users/trang/Documents/GitHub/NER-Company-Annual-Report/edgar'

# Get a list of the folders in the base path.
current_dirs = os.listdir(path=base_path)
master_dict_data =[]
master_data = []

for yr in years:
    current_files = os.listdir('/'.join([base_path, str(yr)]))
    for qtr in quarters:
        local_filename =  f'xbrl-index-{yr}-{qtr}.txt'
        local_file_path = '/'.join([base_path, str(yr), local_filename])
        with open(local_file_path,'r') as f:
            lines = f.readlines()
            if(len(lines)>10):
                data_format = lines[10:]
                
                # loop through the data list
                for index, item in enumerate(data_format):
                    clean_item = item.replace('\n','').split('|')
                    clean_item[4] = "https://www.sec.gov/Archives/"+clean_item[4]
                    if(clean_item[2]=='10-K'):
                        
                        document_dict = {}
                        document_dict['cik_number'] = clean_item[0]
                        document_dict['company_name'] = clean_item[1]
                        document_dict['form_type'] = clean_item[2]
                        document_dict['date'] = clean_item[3]
                        document_dict['filename'] = clean_item[4] 
                        master_dict_data.append(document_dict)
                        master_data.append(clean_item)
df = pd.DataFrame(master_data,columns=['cik_number','company_name','form_type','date','filename'])
df.to_csv('list_10_K.csv',index=False)
            
        