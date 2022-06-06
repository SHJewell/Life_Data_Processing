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
    Guard against times greater than 2400H
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
        self.year = None

        if path:
            self.year = utils.get_year(self.path)
            self.data, self.linear = self.import_new_log(path=self.path)
        else:
            self.data = pd.DataFrame
            self.path = None


    def import_new_log(self, **kwargs):
        '''
        :param kwargs:
        :return: dataframe
                 series of index, should be dates
        '''


        self.path = kwargs.get('path', self.path)

        temp = pd.read_excel(self.path, sheet_name=None, index_col=1)

        data = pd.concat(temp.values())     # concatenate months

        data.drop(data.filter(regex="Unnamed"), axis=1, inplace=True) # drop the human readable key column
        data.drop(data.loc[:, data.columns.astype(int) >= 2500], axis=1, inplace=True) # drop any times > 2400
        data.columns = self.list_times()                    # re-index for times, rationalizes
        data = data[data.index.notnull()]                   # drop any null dates
        data.dropna(thresh=13, inplace=True)                              # drop empty rows
        self.data = data.ffill(axis='columns')              # fill in half-hour gaps

        self.data.applymap(utils.word_processor)            # unifies string format in all cells

        self.linear = self.data.stack()                     # make a data vector
        # need to reindex as a datetime object
        self.linear.index = pd.to_datetime(self.linear.index.get_level_values(0).astype('str') + ' ' + self.linear.index.get_level_values(1).astype('str'))

        return self.data, self.linear


    def ret_missing_dates(self):
        '''
        I did this a different way earlier, and I don't know why.
        Also, it didn't work

        :return: set of missing days
        '''

        m = re.search('([1-3][0-9]{3})', self.path)

        #if any(self.data.index.year != float(m[-1])):

        set_dates = set(self.data.index.date)
        year_dates = set(self.gen_days(str(m.group())))

        return year_dates.difference(set_dates)

        #return []

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

    def save_pickles(self, write_path):
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


    def ret_data(self):

        return self.data

    def ret_date(self):

        return self.year
