# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 16:38:57 2020

@author: Scott

TODO

"""

#import openpyxl
import pandas as pd
import datetime
import csv
import os
import pickle

import pprint

#loc = "E:/Documents/Coding/Life Data Processing/2020 sheets"

loc = os.getcwd()

filename = "/2020 sheets/Weight Tracker 2020.xlsx"

filepath = loc + filename

dt_object = pd.Timestamp('2020-01-01')


#==============================================================================
#open xlsx, generic

# def open_xlsx(file):
    
#     wb = openpyxl.load_workbook(file)
#     sheets = wb.sheetnames
    
#     raw_sheets = {}
    
#     for sheet in sheets:
        
#         ws = wb[sheet]
#         cell_range = ws['A:N']
#         raw_data = []
        
#         for row in cell_range:   
#             temp_row = []
            
#             for cellN in range(len(row)):
                
#                 cell = row[cellN]
                
#                 temp_row.append(cell.value)
                
#             raw_data.append(temp_row)
        
#         raw_sheets[sheet] = raw_data
        
#     return raw_sheets

#==============================================================================
#open xlsx w/ pandas
    
def data_from_xls(file_path):
    
    raw = {}
    
    sheets = pd.ExcelFile(file_path).sheet_names
    
    for page in sheets:
        
        temp = pd.read_excel(file_path,sheet_name=page)
        
        #removes colmuns with empty names
        raw[page] = temp.loc[:, ~temp.columns.str.contains("^Unnamed")]

    return raw

#==============================================================================
#generate a datestring from a datetime.datetime object
    
def date_string_gen(dt_obj):

    out_str = (dt_obj.year)
    
    month = (dt_obj.month)
    day = (dt_obj.day)
    
    new_date = datetime.date(out_str,month,day)
        
    return new_date

#==============================================================================
#    MAIN
#==============================================================================
    
data = data_from_xls(filepath)
header = data['January'].columns
last_day = "20200000"
master = {}
days_acts = {}

for month_name in data:
    
    month = data[month_name]
    dayN = 0
    
    while dayN < month.shape[0]:
        
        empty = True
        
        if type(month.iloc[dayN,0]) != type(dt_object):

            for ex in range(10,12):
                
                # if month.iloc[dayN, ex] == "no" or pd.isnull(month.iloc[dayN, ex]):
                #     break
                
                if not pd.isna(month.iloc[dayN,ex]):
                    empty = False
                
                days_acts[header[ex]] = [month.iloc[dayN-1, ex], month.iloc[dayN, ex]]
            
        else:
            days_acts = {}
            
            for itemN in range(1,len(header)-1):
            
                days_acts[header[itemN]] = month.iloc[dayN,itemN]
            
            if not pd.isna(month.iloc[dayN,itemN]):
                empty = False
        
            last_day = date_string_gen(month.iloc[dayN,0])

        if not empty:
            master[last_day] = days_acts
            
        dayN += 1
    
#pprint.pprint(master)
#pprint.pprint(master[datetime.date(2020, 3, 23)])

pickle.dump(master, open('weight_tracker.dat', "wb"))


