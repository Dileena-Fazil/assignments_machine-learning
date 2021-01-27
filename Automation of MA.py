# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:40:01 2021

@author: Dileena
"""

import pandas as pd
from pandas_datareader import data, wb
import matplotlib as mpl
#from mpl_finance import candlestick_ohlc
import matplotlib.dates as dates
import datetime
import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import itertools 


mav_period=[]           #list to store user input moving average time period
ylist=[]                #list the store user input x (splitted)
xlist=[]                #list the store user input x (splitted)
columname=[]         #list to store the column name generated for MAV time period
rows=[]
sub=[]
sub_dataframes = []


df = pd.read_csv('C:/Users/fazil/Desktop/Stock_market/data/EUR_USD_1H.csv')
df['Date']=pd.to_datetime(df['Date'])   
df['Datetime']=df['Date']                         #creating  a new column for date time
df.set_index("Date", inplace = True)              # setting date column as index
print(df)
columns=df.columns.tolist()                       #coverting column name to list
print(columns[:-1])
MAV_column=input("select required column:-")       #select required column to calculate MAV .

print(MAV_column)               

def SMA(df):
   
    n=input("How many number of  M.AV windows needed to be computed:-") #inputiing number of Periods required (like 1,2,3....)
    n=int(n)

    for num in range(n):
        x, y = input("Enter values: eg: 2 D, 4 H, 1 W:-").split() # inputting the frequency of Moving average (like 3 H ,4 D, 5 D, 1 W)
        xlist.append(x)
        x=int(x)
        if y=="H":                             #if y == H ie if user needed to calculate hourly moving average                                        
            hourly=df.resample('H').agg({MAV_column:'last','Datetime':'last'})
            mav_period.append(x)              # appending   the x value inputted to list of mav_period      
            ylist.append(y)
            sub.append(hourly)
          
        
        if y=="D":
            daily_data=df.resample('D').agg({MAV_column:'last','Datetime':'last'})  #if y == D ie if user needed to calculate daily moving average 
            daily_data = daily_data.dropna()
            df['Datetime']=pd.to_datetime(df['Datetime'])
            daily_data.set_index("Datetime", inplace = True)
            df['is_true']=df.index.map(daily_data[MAV_column])==df[MAV_column]      #comparing both dataframe values of thr column with the index (live vlookup)
            df['daily_data']=df.index.map(daily_data[MAV_column])
            df['daily_data'].replace(to_replace=np.nan, method='bfill' ,inplace = True) #filling other cells with bff
            daily=df[df['is_true'] == True]                                               #creating another dataframe with True values of the column

            mav_period.append(x)  # appending  the x value inputted to list of mav_period
            ylist.append(y)
            sub.append(daily)
            
            
        if y=="W":
            weekly_data=df.resample('W').agg({MAV_column:'last','Datetime':'last'})  #if y == W ie if user needed to calculate daily moving average 
            weekly_data = weekly_data.dropna()
            df['Datetime']=pd.to_datetime(df['Datetime'])
            weekly_data.set_index("Datetime", inplace = True)
            df['is_true']=df.index.map(weekly_data[MAV_column])==df[MAV_column]      
            df['weekly_data']=df.index.map(weekly_data[MAV_column])
            df['weekly_data'].replace(to_replace=np.nan, method='bfill' ,inplace = True) 
            weekly=df[df['is_true'] == True]                                               
         
            mav_period.append(x)  # appending  the x value inputted to list of mav_period
            ylist.append(y)
            sub.append(weekly)
          
   
    columname = [str(MAV_column)+"-"+str(xlist[i])+ ylist[i] for i in range(len(xlist))] #creating the column name by concatinating the xlist and y list for the new columns
    rows=[]
    for (row,i) in  zip(enumerate(sub),mav_period):
        index=row[0]
        sub_dataframes.append(row[1])
        i=int(i)
                                                                         #calculating moving average for user inputted frequency
        rows.append(sub_dataframes[index][MAV_column].rolling(window =i ).mean())
        
    for i in range(len(columname)):
        #sub[columname[i]]=rows[i]
        df[columname[i]]=df.index.map(rows[i])
        df[columname[i]].fillna(method ='ffill', inplace = True)
    
    
    selected=['seagreen','red','blue','orange','yellow','violet'] #For Graph Plotting
    plt.figure(figsize = (20,10))
    for lines,colors in zip(columname,selected):
        
        df[lines].plot(color = colors, label= lines) 
    df[MAV_column].plot(color = 'mediumorchid', label= MAV_column) 
    plt.ylabel('Price in US ', fontsize = 15 )
    plt.xlabel('Date', fontsize = 15 )
    plt.title('ZAR', fontsize = 20)
    plt.legend()
    plt.grid()
    plt.show()
    df=df.drop(['Datetime', 'is_true'], axis = 1,inplace = True) 
       
    
    return(df)
SMA(df)

df.to_csv('C:/Users/fazil/Desktop/Stock_market/data/Automate_MAV_Results1.csv', mode = 'a')