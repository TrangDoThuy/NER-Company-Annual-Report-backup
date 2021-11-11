# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 11:14:14 2021

@author: emma
"""

import pandas as pd
import numpy as np
import requests
import xlsxwriter
import math
#%%
IEX_CLOUD_API_TOKEN = 'pk_736250c2dbfa43f1ab473c831116b4c3'
#%%
stocks = pd.read_csv('sp_500_stocks.csv')
#%%
symbol='AAPL'

api_url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={IEX_CLOUD_API_TOKEN}' 
data = requests.get(api_url).json()
#%%
price = data['latestPrice']
market_cap = data['marketCap']
#%%
my_columns = ['Ticker','Stock Price','Market Capitalization','Number of Shares to Buy']
final_dataframe = pd.DataFrame(columns = my_columns)
#%%
s=pd.Series([symbol,price,market_cap,'N/A'],index=my_columns)
print(s)
#%%
final_dataframe=final_dataframe.append(s,ignore_index=True)
#%%
print(final_dataframe)
#%%
final_dataframe = pd.DataFrame(columns = my_columns)
for stock in stocks['Ticker'][:5]:
    api_url = f'https://cloud.iexapis.com/stable/stock/{stock}/quote?token={IEX_CLOUD_API_TOKEN}' 
    data = requests.get(api_url).json()
    final_dataframe = final_dataframe.append(pd.Series([stock,data['latestPrice'],data['marketCap'],'N/A'],index=my_columns),ignore_index=True)
print(final_dataframe)
#%%
# using batch API
def chunks(lst,n):
    for i in range(0,len(lst),n):
        yield lst[i:i+n]
#%%
symbol_groups = list(chunks(stocks['Ticker'],100))
symbol_strings = []
final_dataframe = pd.DataFrame(columns = my_columns)
for i in range(0,len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(pd.Series([symbol,data[symbol]['quote']['latestPrice'],data[symbol]['quote']['marketCap'],'N/A'],index=my_columns),ignore_index=True)
#%%
portfolio_size = 10000000
position_size = portfolio_size/len(final_dataframe.index)
for i in range(0,len(final_dataframe.index)):
    final_dataframe.loc[i,'Number of Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i,'Stock Price'])
print(final_dataframe)

