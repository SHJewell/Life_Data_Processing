# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 16:38:37 2020

@author: Scott

TODO:
    Current:
        Creating and adding daily nutrition tallies
    General
    New Year:
        Maybe have the ability to add individual months instead of whole years
        Loop through months
            Loops will almost certainly be necessary, I don't see a way to do this without them
            Turn into ... dict? using date objects
            Convert to cals, etc per day
        Read master food list

"""

import os
import openpyxl
import datetime
import csv
import string
import pickle
import pandas as pd
import re
#import tk
import utils

import pprint


class foodTracker:
    def __init__(self, path=None, food_master=None):
        self.today = datetime.datetime.today()
        self.file_path = path
        self.master_food_path = food_master
        self.eating_log = {}
        self.nutrition_data = pd.DataFrame(columns=['calories (kCal)',
                                                    'carbs (g)',
                                                    'fats (g)',
                                                    'fiber (g)',
                                                    'sugar (g)'])
        self.food_list = pd.DataFrame
        self.reported_dates = pd.Series
        self.missing_dates = set()
        self.year = None
        self.errors = []

        if food_master != None:
            self.food_list = self.import_food_master_from_sheet()

        if path != None:
            #self.year = utils.get_year(self.filepath) how do we get year?
            self.eating_log = self.gen_new_log()


    def import_month(self, filepath):

        month = pd.read_excel(self.file_path + filepath, sheet_name=None)

        for name in month:

            if 'week' in name.lower():

                week = month[name]

                for dayN in range(0, len(week.columns), 2):

                    days_nutrition = {'calories (kCal)':    0,
                                      'carbs (g)':          0,
                                      'fats (g)':           0,
                                      'fiber (g)':          0,
                                      'sugar (g)':          0
                                      }

                    day = week.iloc[1:, dayN:(dayN+2)].dropna()
                    day.iloc[:, 0].apply(utils.word_processor).str.replace(' ', '')

                    for item in (day.dropna()).itertuples():

                        if item._1 in self.food_list.index:     # itertubples produces a pandas frame, where columsn are _n

                            for nutrient in days_nutrition:

                                try:
                                    days_nutrition[nutrient] += float(self.food_list.loc[item._1][nutrient])
                                except TypeError:
                                    self.errors.append(str(week.columns[dayN].date()) + ', ' + item._1 + ', ' + nutrient)

                    days_nutrition['Date'] = week.columns[dayN].date()
                    self.nutrition_data.append(days_nutrition, ignore_index=True)

        return


    def gen_new_log(self):

        # month_opts = []
        #
        # for n in range(1, 12):
        #     month = datetime.datetime.strptime(str(n), '%m')
        #     month_opts.append((month.strftime('%b')).lower())
        #     month_opts.append((month.strftime('%B')).lower())

        for file in os.listdir(self.file_path):

            if 'food' in file.lower():

                file_year = utils.get_year(file)

                if self.year is not None and file_year != self.year:

                    self.errors.append("Years do not match!")
                    self.year = file_year

                self.import_month(file)


    def import_food_master_from_sheet(self):

        self.food_list = pd.read_csv(self.master_food_path)
        self.food_list.index = self.food_list['food'].apply(utils.word_processor).str.replace(' ', '')
        self.food_list.fillna(0, inplace=True)

        return self.food_list


if __name__ == '__main__':

    # path = 'E:\Documents\Datasets\Life Data\\2020 sheets\\'
    # master_path = 'E:\Documents\Datasets\Life Data\\Spreadsheets\\master food list.csv'
    path = 'C:\Datasets\Life Data\\2020\\'
    master_path = 'C:\Datasets\Life Data\Other\master food list.csv'


    foodlog = foodTracker(path=path, food_master=master_path)

    breakpoint()


# #==============================================================================
# #constants
#
# #path = "E:\\Documents\\Coding\\Life Data Processing\\2020 sheets"
# food_list_file = "master food list.xls"
#
# months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
# titles = ['food','cals','carbs','fats','proteins','fiber','sugar','type']
#
# #JD adjuster for starting late in 2020
# JD_adjustement = 44
#
# master_calendar = {}
#
# blankdate = datetime.datetime(2020,1,1,0,0)
#
# #==============================================================================
# #Excel sheet opener
# #==============================================================================
#
# #returns a dictionary, where the worksheets are the keys
# #each sheet is a 2D nested list
#
# def open_xlsx(file):
#
#     wb = openpyxl.load_workbook(file)
#     sheets = wb.sheetnames
#
#     raw_sheets = {}
#
#     for sheet in sheets:
#
#         ws = wb[sheet]
#         cell_range = ws['A:N']
#         raw_data = []
#
#         for row in cell_range:
#             temp_row = []
#
#             for cell in row:
#
#                 temp_row.append(cell.value)
#
#             raw_data.append(temp_row)
#
#         raw_sheets[sheet] = raw_data
#
#     return raw_sheets
#
# #==============================================================================
# #generate a Julian date from a datetime.datetime object
#
# def gen_date(dt_obj):
#
#     leap_years = [2020, 2024, 2028, 2032, 2036, 2040, 2044, 2048, 2052, 2056, 2060, 2064, 2068, 2072, 2076, 2080, 2084, 2088, 2092, 2096]
#
#     normal_year_months = {
#         1 :   0,
#         2 :   31,
#         3 :   59,
#         4 :   90,
#         5 :   120,
#         6 :   151,
#         7 :   181,
#         8 :   212,
#         9 :   243,
#         10:   273,
#         11:   304,
#         12:   334
#         }
#
#     leap_year_months = {
#         1 :   0,
#         2 :   31,
#         3 :   60,
#         4 :   91,
#         5 :   121,
#         6 :   152,
#         7 :   182,
#         8 :   213,
#         9 :   244,
#         10:   274,
#         11:   305,
#         12:   335
#         }
#
#     yr = str(dt_obj.year)
#
#     # if yr in leap_years:
#     #     day = leap_year_months[dt_obj.month] + dt_obj.day
#     # else:
#     #     day = normal_year_months[dt_obj.month] + dt_obj.day
#
#     mon = str(dt_obj.month)
#     day = str(dt_obj.day)
#
#     if len(mon) == 1:
#         mon = "0" + mon
#
#     if len(day) == 1:
#         day = "0" + day
#
#     return yr + mon + day
#
#
# #==============================================================================
# #cleans up strings, removing leading and following spaces, carriage returns and
# #changing to lower case
#
# def word_processor(in_string):
#
#     mid = in_string.replace("\\n","")
#     mid = mid.replace("\n","")
#     mid = mid.replace("&","and")
#     mid = mid.replace(" ","")
#
#     mid = mid.translate(str.maketrans("","", string.punctuation))
#
#     if (mid in ["", None]) or (len(mid) == 0):
#         return
#
#     # while mid[0] == " ":
#
#     #     mid = mid[1:]
#
#     # while mid[-1] == " ":
#
#     #     mid = mid[0:-1]
#
#     if mid[-1] == "s":
#         mid = mid[:-1]
#
#     if mid in ["", None]:
#         return
#     else:
#         return mid.lower()
#
#
#
# #==============================================================================
# def day_processor(what,amount):
#
#     day = {}
#     #print(len(what),len(amount))
#
#     for n in range(2,len(what)):
#
#         #print(what[n],amount[n])
#
#
#         try:
#             item = word_processor(str(what[n]))
#         except:
#             print("STRING ERROR", "\'" + str(what[n]) + "\'")
#             continue
#
#         if item == "" or item == None:
#             continue
#
#         if amount[n] == None:
#             amount[n] = 0
#
#         if item in day:
#             day[item] += amount[n]
#
#         else:
#             day[item] = amount[n]
#
#     return day
#
# #==============================================================================
# #generate master sheet
#
# #generates adictionary for each JD, with the keys consistsing of the food name
# #and containing the amount
#
# def gen_master_calendar(current_master, new_month):
#     dummy_date = datetime.datetime(2020,1,1,0,0)
#
#     month = {}
#
#     for row in new_month:
#         if "Week" in row:
#
#             dayN = 0
#
#             #for dayN in range(len(new_month[row])):
#             while dayN < 14:
#                 day = new_month[row][dayN]
#
#
#                 if day == []:
#                     continue
#
#                 if type(day[0]) == type(dummy_date):
#                     #JD = gen_date(day[0])
#                     JD = day[0].date()
#                     #print(day[0],JD)
#
#                     how_much = new_month[row][dayN+1]
#                 #print(day[0],type(day[0]))
#                     what = new_month[row][dayN]
#
#                     day = day_processor(what,how_much)
#
#                     if len(day) > 1:
#                         month[JD] = day
#                     #print(day)
#
#                 dayN += 2
#
#     return month
#
# #Generate nutritional calendar=================================================
# def gen_nutr_cal(calendar,food):
#
#     missing = []
#     nutrition = {}
#     master = food.keys()
#     ed_master = []
#
#     for dish in master:
#
#         ed_master.append(word_processor(dish))
#
#     titles = ['cals','carbs','fats','proteins','fiber','sugar']
#
#     for day in calendar:
#
#         food_day = {
#               'cals'     :   0,
#               'carbs'    :   0,
#               'fats'     :   0,
#               'proteins' :   0,
#               'fiber'    :   0,
#               'sugar'    :   0
#               }
#
#         for c_item in calendar[day]:
#
#             itemp = word_processor(c_item)
#
#             if itemp == None or itemp == "none" or itemp == "":
#                 continue
#
#             if itemp not in ed_master:
#                 misdate = [c_item , day]
#                 missing.append(misdate)
#                 continue
#
#             for ingred in titles:
#
#                 food_ing = (food[itemp][ingred]).translate(dict.fromkeys(map(ord, string.whitespace)))
#
#                 if (food_ing == "") or (food_ing == None):
#                     food_ing = 0
#
#                 #print("Cal: \"", calendar[day][itemp], "\"",type(calendar[day][itemp]),"Food: \"",food_ing, "\"",type(food_ing))
#                 food_day[ingred] = food_day[ingred] + float(calendar[day][itemp])*float(food_ing)
#
#         nutrition[day] = food_day
#
#     return nutrition, missing
#
# #==============================================================================
#
# def gen_csv(data, name):
#
#     with open(name, 'w', newline='') as f:
#
#         writer = csv.writer(f, delimiter=",")
#
#         for row in data:
#
#             out = [row]
#
#             for item in data[row]:
#
#                 out.append(data[row][item])
#
#             writer.writerow(out)
#
# #==============================================================================
# #main
# #initialize variables
#
# ordered_months = {}
# raw_data = {}
#
# master_calendar = {}
#
# path = tkinter.filedialog.askopendirectory()
# files = os.listdir(path)
#
# #==============================================================================
# #food information
#
# master_file = path + "\\" + "master food list.csv"
#
# food_master = {}
#
# with open(master_file, newline='') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#
#         if row[0] in ['', 'food']:
#             continue
#
#         item = {}
#
#         for n in range(1,len(titles)):
#
#             #item[titles[n]] = word_processor(row[n])
#             item[titles[n]] = row[n]
#
#             food_master[word_processor(row[0])] = item
#             food_master["Name"] = item
#
#
# #pprint.pprint(food_master)
#
# for month in months:
#
#     for file in files:
#
#         if ".xlsx" not in file:
#             continue
#
#         if "#" in file:
#             continue
#
#         if month in file.lower():
#             ordered_months[n] = file
#             #files.remove(file)
#             n += 1
#
# for file in ordered_months:
#
#     filepath = path + "\\" + ordered_months[file]
#
#     if "xls" in filepath:
#         month = gen_master_calendar(master_calendar, open_xlsx(filepath))
#
#         master_calendar = {**master_calendar, **month}
#
#
# temp = gen_nutr_cal(master_calendar,food_master)
#
# nutr_cal = temp[0]
# missing_foods = temp[1]
# gen_csv(missing_foods, "missing food.csv")
# gen_csv(nutr_cal, "nutrition calendar.csv")
#
# #[date,calories,carbs,fats,proteins,fibs,sugar]
# pickle.dump(nutr_cal, open('nutritional_calendar.dat', "wb"))
#
#
# #pprint.pprint(check_missing_food(master_calendar, food_master))
#
# #pprint.pprint(master_calendar)