# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 15:21:57 2020

@author: Scott

TODO

check if there's a way to filter NaNs and other undesireables
come up with system to split datasets based on dt
general delta gen (DateOffset)
interpolater
UI

"""

import pickle
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#==============================================================================
#datify
#takes a datetime or date indexed dataframe and returns and calculates the t-delta
#IN: dataframe, date indexed
#OUT: dataframe, date indexed containing t-delta

def datify(df):
    
    dates = data.index.values
    dt = [float("NaN")]
    
    for n in range(1,len(dates)):
        
        dt.append((dates[n] - dates[n-1]).days)
        
    ts = pd.DataFrame({"delt" : dt},index=dates)
        
    return ts

#==============================================================================
#2d_dat_checker
#cleans data for plotting
#   removes NaNs/NaTs
#   ensures lists are the same length    
#IN: dataframe, two strings with the names of desired datasets, maximum tim difference between points
#OUT: dataframe with columns representing the datasets and the time delta
    
def d2_dat_checker(dat, col1, col2):
    
    N = len(dat)
    dates = list(data.index)
    set1, set2, date, delt = [], [], [], []
    
    for n in range(N):
        
        datpt1, datpt2, deltpt = data[col1][n], data[col2][n], data['delt'][n]
        check = [datpt1, datpt2]
        
        if True in pd.isnull(check):
            continue
        
        set1.append(datpt1), set2.append(datpt2), delt.append(deltpt), date.append(dates[n])
        
    #return pd.DataFrame([delt,set1,set2],index=date,columns=['delt',col1,col2])
    return pd.DataFrame({'delt': delt, col1: set1, col2: set2},index=date)

#==============================================================================
#delta_gen
#calculates change in a single dataset  
#IN: dataframe, column to be delta'd
#OUT: dataframe original column and index and delta column
        
def delta_gen(df, col):
    
    N = len(df)
    dset = df[col]
    indx = list(df.index)
    delt = [0]
    name = "del-" + col
    
    for n in range(1,N):
        
        delt[indx[n]] = (dset[n] - dset[n-1])
        
    return pd.DataFrame()
        
#==============================================================================
#interpolate
#interpolates a single data column
#IN: dataframe, column to be delta'd, type of interpolation, maximum span
#OUT: dataframe of dates and interpolated data

#==============================================================================
#main
#==============================================================================

data = pickle.load(open("raw_master_db.dat",'rb'))
data.sort_index(axis=0,inplace=True)

data = pd.concat([data, datify(data)],axis=1,sort=True)

dfat = d2_dat_checker(data,'delt','fats')

#def sub_set_gen(set1,set2,delt):
    
#def interpolate(y,x):    
    
#def diff(y,x)

# plt.scatter(data.index.tolist(),data["weight"])
# data.plot(y="weight")
# data.plot(y="cals")

#dates = datify(data)



# column_names = data.columns.tolist()
# dates = data.index.values

# delt_masked = np.ma.masked_where(data['delt'] > 100, data['delt'])
# plt.plot(dates,delt_masked)
