# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 12:40:52 2020

TODO:
    
Interface with Pandas
Detach from GSheets
Fuzzy typo correction

@author: Scott
"""

import ezsheets
import time

year = 2020
calorie_tracker = {}

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

#=============================================================================


#removes innappropriate data types
def format_filter(column):
    quant_col = filter(None,column)
    quant_col = filter(bool,quant_col)
    quant_col = filter(len,quant_col)
    quant_col = list(filter(lambda item: item, quant_col))

    return quant_col   


#=============================================================================
    

#takes a bunch of data and comma seperates it;
#useful for the typo correction
def comma_seperate(f1, f2, a, b, c, d, e, f):
    f1 = f1.replace(",","")
    f2 = f2.replace(",","")

    a = [f1 , f2, str(a), str(b), str(c), str(d), str(e), str(f)]
    return a 

#=============================================================================

#To be implemented
#do some fuzzy typo squashing
def adv_typo_checker (item, foodKeys, what):
    import jellyfish
    
    for item in foodKeys:
        #print(what,item)
        leven = jellyfish.levenshtein_distance(item, what)
        damerau = jellyfish.damerau_levenshtein_distance(item, what)
        hamming = jellyfish.hamming_distance(item, what)
        jaro = jellyfish.jaro_distance(item, what)
        winkler = jellyfish.jaro_winkler(item, what)
        match = jellyfish.match_rating_comparison(item, what)
        
    return comma_seperate(what, item, leven, damerau, hamming, jaro, winkler, match)

#=============================================================================

#writes files used for typo correction
#can be removed without issue
def write_comp_file(name, comparison):
    import csv
    
    with open(name, mode='w', newline='',errors='replace') as csvfile:
        writer = csv.writer(csvfile)
        for row in comparison:
            writer.writerow(row)
    csvfile.close()
    
#=============================================================================

#checks spelling for newlines, spaces, plurals and capitalization
def basic_typo_checker (day, ref_sheet):
    
    temp = day.lower()
    temp = temp.replace("\n","")
    basic = temp.replace(" ", "")
    
    if basic in ref_sheet:
        return temp
    elif basic[:-1] in ref_sheet:
        return temp[:-1]
    elif basic + "s" in ref_sheet:
        return basic + "s"
    else:
        #print(temp + " not in reference sheet!")
        return False
    
#=============================================================================
    
#sums up the items and quantities for each week
def week_processing(this_weeks_sheet):
    colN = 1
    missing_items = {}
    weekly_items = {}

    while colN < 29:
        
        #filters cold be functionized
        day_col = this_weeks_sheet.getColumn(colN)
        day_col = format_filter(day_col)
        quant_col = this_weeks_sheet.getColumn(colN+1)
        quant_col = format_filter(quant_col)
        
        if day_col == []:
            break
        else:
            this_days_date = day_col[0]
        
        today = {}
        
        for n in range(2,len(day_col)):
        #we'll move backwards, makes it easier to avoid column mis-match errors
        #for n in range(len(day_col),1,-1):
            
            this_item = day_col[n]
            
            if this_item == "":
                continue
            
            if this_item not in oFoodKeys:
                corrected = basic_typo_checker(this_item, formatFoodKeys.keys())
                if corrected == False:
                    if this_item in missing_items:
                        missing_items[this_item].append(this_days_date)
                    else:
                        missing_items[this_item] = [this_days_date]
            
            else:
                if this_item in today:
                    quant = today[this_item]
                    today[this_item] = quant + float(quant_col[n-1])
                else:
                    today[this_item] = float(quant_col[n-1])
                #print(" ")
                #print(temp, day_col[n])      #need fuzzy checking
                #comparison.append(typo_checker())
    
        colN += 2
        
        weekly_items[this_days_date] = today
        #print(this_days_date,today)

    return {"week" : weekly_items, "missing": missing_items}
        
#writes the report file
def report_write(report):
    import csv
    
    header = ["Date", "Calories", "Carbs", "Fats", "Protein", "Fiber", "Sugar"]
    
    #days = report.keys()
    
    
    
    with open("food report", mode='w', newline='',errors='replace') as csvfile:
        writer = csv.writer(csvfile)
        for row in comparison:
            writer.writerow(row)
    csvfile.close()
    
    

#it would be good to have some checks for correct column sizes, but this generates false positives
# =============================================================================
#         if len(day_col) != (len(quant_col) + 1):
#             print(this_days_date + " has mismatched columns!")
#             colN += 2
#             continue
# =============================================================================
    
                        

# nsheets = {"feb" : "1NCDUHSkLfMn3xoI5O5EOBzMqs_VIhIQnHBISL9xxtes",
#           "mar" : "1-VJDccoNEndgBtvq4k5fn3WvIFkbOjtO3hjcXWLGIl8",
#           "apr" : "1NNlbwiHD_5kPzIoF_aDn60k6fH9XmksoOGDkfxbs1G0",
#           "may" : "1QZjH6d9220HA0T2D21fxgjlPOhM1gVSn5wU4mLnVJ3M"}

#we want to use the latest reference sheet
#ss = ezsheets.Spreadsheet(nsheets["may"])

# foodsheets = ss.sheets
# refsheet = ss['Reference sheet']

#oh hey, ref should actually be filled
ref = {}
keylist = {}

n = 0
row = refsheet.getRow(1)

#reference sheet headers
for cell in row:
    if cell == '':
        break
    
    spc = cell.find(" ")
    
    if spc == -1:
        keylist[n] = cell
    else:
        keylist[n] = cell[:spc]
    
    n += 1
    
#reference sheet information

foods = {}
rowN = 1
while True:
    row = refsheet.getRow(rowN)
    if row[0] == '':
        break
    
    entry = {}
    
    for cellN in range(1,len(keylist)):
        entry[keylist[cellN]] = row[cellN]
    
    foods[row[0].lower()] = entry
            
    rowN += 1
#print(foods)
   
oFoodKeys = foods.keys()
formatFoodKeys = {}
    
for n in oFoodKeys:
    temp = n.lower()
    temp = temp.replace(" ","")
    temp = temp.replace("\n","")
    formatFoodKeys[temp] = n

comparison = [["From Date", "From Reference", "Levenshen", "Levenshen-Damerau", "Hamming", "Jaro", "Jaro-Winkler", "Matching"]]
t = time.time()

report = {}
missing_items = {}

#ss = ezsheets.Spreadsheet(nsheets["apr"])

for mon in nsheets.keys():
    
    ss = ezsheets.Spreadsheet(nsheets[mon])

    for week in ss.sheets:
        
        if "week" not in week.title.lower():
            continue
    
        weekly_report = week_processing(week)
        report.update(weekly_report["week"])
        missing_items.update(weekly_report["missing"])
            #print(day_col,quant_col)    

#print(missing_items,report)
print(missing_items)
print(time.time() - t)  

#write_comp_file("test.csv", comparison)
    

#for cursheet in ss.titles:
#    if cursheet == 'Reference sheet':
#        continue
  
#    n = 0
    #while True:
    #    if 
    
    
