import requests
import os
import time

# List of years to be searched
years = [2000 + x for x in range(6,21)]

# List of quarters to be searched
quarters = ['QTR1', 'QTR2', 'QTR3', 'QTR4']

# The absolute path to the folder for saving the index files 
base_path = 'C:/Users/trang/Documents/GitHub/NER-Company-Annual-Report/edgar'

# Get a list of the folders in the base path.
current_dirs = os.listdir(path=base_path)

# Loop over the years and quarters. For each year/quarter combination, get the corresponding
# index file from EDGAR, and save it to the local machine as a text file.
for yr in years:
 
    # Check current_dirs for a folder labeled 'yr' (i.e. 2009, 2015, etc)
    # If the folder does not exist, then create it.
    if str(yr) not in current_dirs:
        os.mkdir('/'.join([base_path, str(yr)]))
    
    # Get a list of the files inside the year folder.
    current_files = os.listdir('/'.join([base_path, str(yr)]))
    
    for qtr in quarters:
        # Use the following filename pattern to store the index files locally.
        local_filename =  f'xbrl-index-{yr}-{qtr}.txt'
        
        # Create the absolute path for storing the index file. (e.g.
        
        local_file_path = '/'.join([base_path, str(yr), local_filename])
        
        # Check to see if the index file for the current year/quarter combination is already
        # saved locally. If it is, then skip to the next year/quarter combination.
        if local_filename in current_files:
            print(f'Skipping index file for {yr}, {qtr} because it is already saved.')
            continue
        
        # Define the url at which to get the index file.
        url = f'https://www.sec.gov/Archives/edgar/full-index/{yr}/{qtr}/xbrl.idx'
        
        # Get the index file from EDGAR and save it to a text file. Note that to save a file
        # rather than bringing it into memory, set stream=True and use r.iter_content() 
        # to break the incoming stream into chunks (here arbitrarily of size 10240 bytes)
        headers = { 'User-Agent': 'Mozilla/5.0', } 
        r = requests.get(url, stream=True, headers = headers)
        
        with open(local_file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=10240):
                f.write(chunk)
                
        # Wait one-tenth of a second before sending another request to EDGAR.
        time.sleep(0.1)