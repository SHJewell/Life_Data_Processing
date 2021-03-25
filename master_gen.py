# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 17:15:20 2020

@author: Scott

TO DO


"""

import pandas as pd
import datetime
import pickle
import string

import pprint

# ------------------------------------------------------------------------------

def date_processor(obj):
#returns a datetime.date object
    
    dt_obj_dummy = datetime.date(2000,1,1)
    
    if type(obj) == type(dt_obj_dummy):
        return obj
    
    else:
        
        out = datetime.date(int(obj[0:4]),int(obj[4:6]),int(obj[6:8]))
        return out
    
# ------------------------------------------------------------------------------
            
def daily_totals(calendar):
# gives activity totals by day
    
    cats = set()
    act_totals = {}
    
    # generate categories
    # this is not a terribly efficient, but very general
    for day in calendar:
        
        for cat in calendar[day]:
            
            cats.add(calendar[day][cat])
    
    for day in calendar:
        
        days_acts = dict(zip(cats,len(cats)*[0]))
        
        for cat in calendar[day]:
            
            act = calendar[day][cat]
            
            days_acts[act] = days_acts[act] + 0.5
        
        act_totals[date_processor(day)] = days_acts
    
    return act_totals

# ==============================================================================
# cleans up strings, removing leading and following spaces, carriage returns and
# changing to lower case

def word_processor(in_string):
    
    if in_string == 'Weight (lb)':
        return "weight"
    if in_string == 'Sleep (1-5)':
        return "sleep"
    if in_string == 'Energy (1-5)':
        return "energy"
    if in_string == 'Mental (1-5)':
        return "mental"
    if in_string == 'Heart (1-5)':
        return "heart"
    
    mid = in_string.translate(str.maketrans("","", string.punctuation))
    
    return mid.lower()
    
# ==============================================================================

def col_processing(df):
    
    cols = list(df.columns)
    new_titles = []
    
    for title in cols:
        
        new_titles.append(word_processor(title))
        
    df.columns = new_titles    
        
    return df 

# ==============================================================================
 #MAIN


weight_old = pickle.load(open('older_weights.dat','rb'))
nutrition = pickle.load(open('nutritional_calendar.dat','rb'))
calendar = pickle.load(open("master_calendar.dat", "rb"))
#pickle.dump(linear, open("vector_calendar.dat", "wb"))
weight = pickle.load(open('weight_tracker.dat', "rb"))

daily_activities = daily_totals(calendar)

# ------------------------------------------------------------------------------
# generate frame skeleton

cal = pd.DataFrame.from_dict(weight,orient='index')
nutr_frame = pd.DataFrame.from_dict(nutrition,orient='index')
nutr_frame = pd.DataFrame.from_dict(nutrition,orient='index')
cal_frame = pd.DataFrame.from_dict(daily_activities,orient='index')
old_frame = pd.DataFrame.from_dict(weight_old,orient='index')
old_frame.columns = ['Weight (lb)']

#cal.merge(old_frame)

#frames = [cal, nutr_frame, cal_frame, old_frame]
frames = [cal, nutr_frame, cal_frame]

master = pd.concat(frames,axis=1,sort=True)
master = master.append(old_frame)

master = col_processing(master)

dates = master.index.values

#print(dates)

# print(list(master.columns))

file = "raw_master_db.csv"
master.to_csv(file)

pickle.dump(master,open("raw_master_db.dat",'wb'))


        