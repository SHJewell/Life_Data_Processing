# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 13:44:50 2020

@author: Scrooge


Data structures:
    Calender structure:
        Type: Dataframe
        Rows: Date
        Columns: Hours of Day

        Does it need a key as well?

    Linear structure:
        Type: Dict/Series
        Index: Datetime


TODO:
    Class should have the following methods:
        Read old pickled year
        Append new data
            Will need to determine how to deal with partially filled months
        Export master
            As .csv
        Export linear
            As .csv?
    External function should call Daily class, append for each month
        File opener?
            .csv
            .xlm
            pickle

"""

import openpyxl
import datetime
import csv
import pickle
import pandas as pd
import utils
import re

class dailyLog:
    def __init__(self, path=None):
        self.today = datetime.datetime.today()
        self.path = path
        self.data = pd.DataFrame
        self.linear = pd.Series
        self.reported_dates = pd.Series
        self.missing_dates = set()

        if path != None:
            self.year = utils.get_year(self.path)
            self.data, self.linear = self.import_new_log()

    def import_new_log(self):

        temp = pd.read_excel(self.path, sheet_name=None, index_col=1)

        self.data = pd.concat(temp.values())     # concatenate months

        self.data.drop(self.data.filter(regex="Unnamed"), axis=1, inplace=True) # drop the human readable key column
        self.data.columns = self.list_times()               # re-index for times, rationalizes
        self.data = self.data[self.data.index.notnull()]    # drop any null dates
        self.data.dropna(thresh=13)                         # drop empty rows
        self.missing_dates = self.gen_missing_dates()       # generates a set of unfilled dates
        self.data = self.data.ffill(axis='columns')         # fill in half-hour gaps

        self.data.applymap(utils.word_processor)            # unifies string format in all cells

        self.linear = self.data.stack()                     # make a data vector
        # need to reindex as a datetime object
        self.linear.index = pd.to_datetime(self.linear.index.get_level_values(0).astype('str') + ' ' + self.linear.index.get_level_values(1).astype('str'))

        return self.data, self.linear


    def gen_missing_dates(self):
        '''
        :return: set of missing days
        '''

        m = re.search('([1-3][0-9]{3})', self.path)

        if any(self.data.index.year != float(m.group(0))):

            set_dates = set(self.data.index.date)
            year_dates = set(self.gen_days(self.year))

            return year_dates.difference(set_dates)


    def gen_days(self, year):
        '''
        :param year: Year of set
        :return: pd.DatetimeIndex of all the years dates
        '''

        y_start = '1/1/' + year
        y_end = '12/31/' + year

        return pd.date_range(start=y_start, end=y_end).date

    def list_times(self):
        '''
        Generates a list of datetime.times for every half hour of the day
        '''

        times = ['%s:%s' % (h, m) for h in ([0] + list(range(1, 24))) for m in ('00', '30')]

        dt_times = []

        for a in times:
            dt_times.append(datetime.datetime.strptime(a, '%H:%M').time())

        return dt_times

    def save_pickles(self):
        '''
        Writes pickle repository.
        TODO:
            make write_path a proper variable
        :return:
        '''

        master_name = write_path + 'dailylog' + self.year + '.dat'

        data = {'daily':    self.data,
                'vector':   self.linear,
                'missing':  self.missing_dates}

        with open(master_name, 'w+') as a:

            pickle.dump(data, a)




    def return_data(self):

        return self.data

if __name__ == '__main__':
    path = 'E:\Documents\Datasets\Life Data\\2020 sheets\\Daily log 2020.xlsx'
    write_path = 'E:\Documents\Datasets\Life Data\Data files\\'
    #path = 'E:\Documents\Datasets\Life Data\\2021 sheets\\daily log 2021.xlsx'

    new_log = dailyLog(path)
    data = new_log.return_data()

    print(data)

# import pprint
#
#
#
# #for laptop. Need to make this more general
# #loc = "C:/Users/Scrooge/Documents/Coding/Life Data Processing/2020 sheets"
# #loc = "E:/Documents/Coding/Life Data Processing/2020 sheets"
#
# #filename = "Daily log 2020.xlsx"
#
# #filepath = loc + "/" + filename
#
# date_type = datetime.datetime.now()
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
#         cell_range = ws['A:AX']
#         raw_data = []
#
#         for row in cell_range:
#             temp_row = []
#
#             for cellN in range(0,34):
#
#                 cell = row[cellN]
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
# def gen_JD(dt_obj):
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
#     yr = dt_obj.year
#
#     if yr in leap_years:
#         day = leap_year_months[dt_obj.month] + dt_obj.day
#     else:
#         day = normal_year_months[dt_obj.month] + dt_obj.day
#
#     if day < 10:
#         return str(yr) + "00" + str(day)
#     elif day < 100:
#         return str(yr) + "0" + str(day)
#     else:
#         return str(yr) + str(day)
#
# #==============================================================================
# #generate a datestring from a datetime.datetime object
#
# def date_string_gen(dt_obj):
#
#     out_str = str(dt_obj.year)
#
#     month = str(dt_obj.month)
#     day = str(dt_obj.day)
#
#     if len(month) == 1:
#         month = "0" + month
#
#     if len(day) == 1:
#         day = "0" + day
#
#     return out_str + month + day
#
#
# #==============================================================================
#
# def process_raw(raw):
#
#     months = {'January'     :   1,
#               'February'    :   2,
#               'March'       :   3,
#               'May'         :   4,
#               'April'       :   5,
#               'June'        :   6,
#               'July'        :   7,
#               'August'      :   8,
#               'September'   :   9,
#               'October'     :   10,
#               'November'    :   11,
#               'December'    :   12}
#
#     cur_year = (datetime.datetime.today()).year
#
#     linear = {}
#
# #==============================================================================
# #cleans up strings, removing leading and following spaces, carriage returns and
# #changing to lower case
#
# def word_processor(string):
#
#     if (string in ["", None]) or (len(string) == 0):
#         return
#
#     mid = string.replace("\\n","")
#     mid = mid.replace("\n","")
#     mid = mid.replace("&","and")
#
#     if (mid in ["", None]) or (len(mid) == 0):
#         return
#
#     mid = mid.strip()
#
#     if mid in ["", None]:
#         return
#     else:
#         return mid.lower()
#
# #==============================================================================
# #24 hour clock caluclator
#
# def  mil_time_gen(seg):
#
#     hour = int(seg/2) + 1
#     minute = (int(seg)*30) % 60
#
#     mil_time = str(hour*100 + minute)
#
#     if len(mil_time) < 4:
#         mil_time = "0" + mil_time
#
#     return mil_time
#
# #==============================================================================
# #linear calendar writer
#
# def lin_writer(calendar, name):
#
#     if ".csv" not in name:
#         name = name + ".csv"
#
#
#     with open(name, 'w', newline="") as csvfile:
#
#         writer = csv.writer(csvfile, delimiter=",")
#
#         for row in calendar:
#
#             out = [row, calendar[row]]
#
#             writer.writerow(out)
#
#
# #==============================================================================
# #master calendar writer
#
# def mst_writer(calendar, name):
#
#     if ".csv" not in name:
#         name = name + ".csv"
#
#
#     with open(name, 'w', newline="") as csvfile:
#
#         writer = csv.writer(csvfile, delimiter=",")
#
#         for row in calendar:
#
#             out = [row]
#
#             for elem in calendar[row]:
#                 out.append(calendar[row][elem])
#
#             writer.writerow(out)
#
# #==============================================================================
# #                        End of functions
# #                         Start of MAIN
# #==============================================================================
#
# def import_lifelog(self, filepath):
#
#     #==============================================================================
#     #open our files and extract the raw data
#
#     raw = open_xlsx(filepath)
#
#     #==============================================================================
#     #generate a list of activity catagories
#
#     legend = []
#     totals = {}
#
#     for cell in (raw['January'][0]):
#
#         temp = word_processor(cell)
#
#         if temp in [None, ""]:
#             continue
#
#         legend.append(temp)
#         totals[temp] = 0
#
#     #==============================================================================
#     #generate daily totals and linear
#
#     master = {}
#     linear = {}
#     totals["total"] = 0
#     prev_activ = None
#
#     for month in raw.keys():
#
#         end_flag = False
#
#         for x in range(1,len(raw[month][1])):
#
#             temp = {}
#             empty_cells = 0
#
#             if not (type(raw[month][1][x]) == type(date_type)):
#                 continue
#
#             for y in range(2,len(raw[month])):
#
#                 activ_type = word_processor(raw[month][y][x])
#
#                 if (activ_type == None) or (activ_type == "") or (activ_type == " "):
#                     activ_type = prev_activ
#                     empty_cells += 1
#
#                     if empty_cells > 24:
#                         end_flag = True
#                         break
#
#                 datetime = date_string_gen(raw[month][1][x]) + mil_time_gen(y-2)
#
#                 linear[datetime] = activ_type
#
#                 temp[mil_time_gen(y-2)] = activ_type
#
#                 totals[activ_type] = totals[activ_type] + 0.5
#                 totals["total"] = totals["total"] + 0.5
#
#                 prev_activ = activ_type
#
#             if end_flag:
#                 continue
#
#             master[raw[month][1][x].date()] = temp
#         #print()
#
#     return master, linear
#
# #lin_writer(linear, "hourly_calendar")
# #mst_writer(master, "formatted_calendar")
#
# #pickle.dump(master, open("master_calendar.dat", "wb"))
# #pickle.dump(linear, open("vector_calendar.dat", "wb"))
#
# #pprint.pprint(master)
#
# #pprint.pprint(raw['January'])