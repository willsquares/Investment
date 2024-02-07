#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 17:09:59 2024

@author: will
"""

pip install yfinance
"""Install the library"""

import yfinance as yf
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

start_date = datetime(1990, 1, 1) #set start date

end_date=datetime(2023,12,31)

#read index price information from yahoo finance

index_w1 = yf.download(['KO', 'PEP','MNST'], start = start_date, end=end_date)['Adj Close']

#Adds back index
index_w1.reset_index(inplace=True)

index_w1['Year']=index_w1['Date'].dt.year

index_w1['Month']=index_w1['Date'].dt.month


index_w1.rename(columns={'KO':'Coca-Cola','PEP':'Pepsi','MNST':'Monster'},inplace=True)

index_w1.sort_values(by=['Date'], inplace=True)


#find the daily return

index_w1[['Coca-Cola_ret_d','Pepsi_ret_d','Monster_ret_d']]=index_w1[['Coca-Cola','Pepsi','Monster']].pct_change()
#pct_change() calculates the percentage change from the immediately previous row.


index_w1[['Coca-Cola_ret_d+1','Pepsi_ret_d+1','Monster_ret_d+1']]=index_w1[['Coca-Cola_ret_d','Pepsi_ret_d','Monster_ret_d']]+1

index_w2=index_w1[['Coca-Cola_ret_d+1','Pepsi_ret_d+1','Monster_ret_d+1','Year','Month']].groupby(['Year','Month'],as_index=False).prod()
# prod() returns the product of the values
#in index_w2, Coca-Cola_ret_d+1 is the product of all Coca-Cola_ret_d+1 in a month

index_w2[['Coca-Cola_ret_m','Pepsi_ret_m','Monster_ret_m']]=index_w2[['Coca-Cola_ret_d+1','Pepsi_ret_d+1','Monster_ret_d+1']]-1

index_w3=index_w2[['Coca-Cola_ret_m','Pepsi_ret_m','Monster_ret_m','Year','Month']]


index_w3['Date']= pd.to_datetime({'year': index_w3['Year'],'month': index_w3['Month'],'day':28})


index_w3.plot(x='Date', y=['Coca-Cola_ret_m','Pepsi_ret_m','Monster_ret_m'], kind='line', linewidth=1, color=['red','blue','green']) 
plt.xlabel('Date', fontsize=10)
plt.ylabel('Monthly return', fontsize=10)
plt.title('Index Monthly Return', fontsize=10)
plt.legend(['Coca-Cola_ret_m','Pepsi_ret_m','Monster_ret_m'], fontsize=10)

#Calculate yearly return
index_w2[['Coca-Cola_ret_m+1','Pepsi_ret_m+1','Monster_ret_m+1']]=index_w2[['Coca-Cola_ret_m','Pepsi_ret_m','Monster_ret_m']]+1

# prod() returns the product of the values
index_w4=index_w2[['Coca-Cola_ret_m+1','Pepsi_ret_m+1','Monster_ret_m+1','Year']].groupby(['Year'],as_index=False).prod()

index_w4[['Coca-Cola_ret_y','Pepsi_ret_y','Monster_ret_y']]=index_w4[['Coca-Cola_ret_m+1','Pepsi_ret_m+1','Monster_ret_m+1']]-1

index_w5=index_w4[['Coca-Cola_ret_y','Pepsi_ret_y','Monster_ret_y','Year']]

index_w5.plot(x='Year', y=['Coca-Cola_ret_y','Pepsi_ret_y','Monster_ret_y'], kind='line', linewidth=1, color=['red','blue','green']) 
plt.xlabel('Year', fontsize=10)
plt.ylabel('Monthly return', fontsize=10)
plt.title('Index Yearly Return', fontsize=10)
plt.legend(['Coca-Cola_ret_y','Pepsi_ret_y','Monster_ret_y'], fontsize=10)


