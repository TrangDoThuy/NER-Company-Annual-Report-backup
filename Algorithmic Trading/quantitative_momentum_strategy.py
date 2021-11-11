# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 15:07:50 2021

@author: emma
"""

#%%
import numpy as np
import pandas as pd
import requests
import math
from scipy.stats import percentileofscore as score
#%%
stocks = pd.read_csv('sp_500_stocks.csv')
IEX_CLOUD_API_TOKEN = 'pk_736250c2dbfa43f1ab473c831116b4c3'
symbol = 'AAPL'
api_url = f'https://cloud.iexapis.com/stable/stock/{symbol}/stats?token={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url).json()
print(data)
#%%
# using batch API
def chunks(lst,n):
    for i in range(0,len(lst),n):
        yield lst[i:i+n]
#%%
symbol_groups = list(chunks(stocks['Ticker'],100))
symbol_strings = []
my_columns = ['Ticker','Price','One-Year Price Return','Number of Shares to Buy']
final_dataframe = pd.DataFrame(columns = my_columns)
for i in range(0,len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
# for symbol_string in symbol_strings:
#     batch_api_call_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote,stats&token={IEX_CLOUD_API_TOKEN}'
#     data = requests.get(batch_api_call_url).json()
#     for symbol in symbol_string.split(','):
#         final_dataframe = final_dataframe.append(pd.Series([symbol,data[symbol]['quote']['latestPrice'],data[symbol]['stats']['year1ChangePercent'],'N/A'],index=my_columns),ignore_index=True)
# #%%
# final_dataframe.sort_values('One-Year Price Return', ascending = False, inplace = True)
# final_dataframe = final_dataframe[:50]
# final_dataframe.reset_index(inplace=True,drop=True)
# #%%
# portfolio_size = 10000000
# position_size = portfolio_size/len(final_dataframe.index)
# for i in range(len(final_dataframe.index)):
#     final_dataframe.loc[i,'Number of Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i,'Price'])
# print(final_dataframe)
#%%
# Build high quality momentum stock
hqm_columns = [
    'Ticker',
    'Price',
    'Number of Shares to Buy',
    'One-Year Price Return',
    'One-Year Return Percentile',
    'Six-Month Price Return',
    'Six-Month Return Percentile',
    'Three-Month Price Return',
    'Three-Month Return Percentile',
    'One-Month Price Return',
    'One-Month Return Percentile'
    ]
hqm_dataframe = pd.DataFrame(columns = hqm_columns)
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote,stats&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json() 
    for symbol in symbol_string.split(','):
        data_series = pd.Series([symbol,data[symbol]['quote']['latestPrice'],'N/A',data[symbol]['stats']['year1ChangePercent'],'N/A',data[symbol]['stats']['month6ChangePercent'],'N/A',data[symbol]['stats']['month3ChangePercent'],'N/A',data[symbol]['stats']['month1ChangePercent'],'N/A'],index=hqm_columns)
        hqm_dataframe = hqm_dataframe.append(data_series,ignore_index=True)
#%%
time_periods = ['One-Year','Six-Month','Three-Month','One-Month']
print(type(hqm_dataframe['One-Year Price Return'].to_numpy()))
print(hqm_dataframe.loc[0,'One-Year Price Return'])
print(score(hqm_dataframe['One-Year Price Return'].to_numpy(),hqm_dataframe.loc[0,'One-Year Price Return']))
for row in hqm_dataframe.index:
    print(row)
    for time_period in time_periods:
        change_col = f'{time_period} Price Return'
        percentile_col = f'{time_period} Return Percentile'
        #hqm_dataframe.loc[row,percentile_col]= 
        print(score(hqm_dataframe['One-Year Price Return'],hqm_dataframe.loc[0,'One-Year Price Return']))
#print(hqm_dataframe)