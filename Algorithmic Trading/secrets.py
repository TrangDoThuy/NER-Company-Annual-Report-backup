# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 16:02:40 2021

@author: trang
"""
IEX_CLOUD_API_TOKEN = 'pk_766a1646b48d45b98678eddfa4a0219b'
#%%
import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
symbol = 'AAPL'
api_url = f'https://sandbox.iexapis.comstock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'

data = requests.get(api_url, timeout=50)
#%%
import bs4 as bs
import requests
import pandas as pd
import re

company = 'Facebook Inc'
filing = '10-Q'
year = 2020
quarter = 'QTR3'
#get name of all filings 
download = requests.get(f'https://www.sec.gov/Archives/edgar/full-index/{year}/{quarter}/master.idx').content
download = download.decode("utf-8").split('\n')
print(download)
#%%