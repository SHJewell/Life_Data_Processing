'''
This is a file containing all the useful functions which can be used by any class

This may be folded into the GUI as that develops
'''

import csv
import pandas as pd
import string

def word_processor(word):

    word = str(word)

    if (word in ["", None]) or (len(word) == 0):
        return

    mid = word.replace("\\n", "")
    mid = mid.replace("\n", "")
    mid = mid.replace("&", "and")
    mid = mid.replace(" ", "")
    mid = mid.translate(str.maketrans('', '', string.punctuation))

    if (mid in ["", None]) or (len(mid) == 0):
        return

    mid = mid.strip()

    try:
        if mid[-1] == "s":
            mid = mid[:-1]
    except IndexError:
        return mid

    if mid in ["", None]:
        return
    else:
        return mid.lower()


def get_year(path):
    import re
    '''
    Should this be a datetime object?
    
    pulls year out of file path
    :return: int of year
    '''

    m = re.search('([1-3][0-9]{3})', path)

    year = int(m.group(0))

    return year

def gen_csv_reader(path):

    master_list = list()

    with open(path, newline='') as r:
        reader = csv.reader(r, delimiter=',')
        for row in reader:
            master_list.append(row)

    return master_list


def import_food_master(path):

    df = pd.read_csv(path)
    df.index = df['food']

    if len(df.columns) > 8:
        df.drop(df.columns[8:], axis='columns')

    return df

# def read_excel(path, sheet, )
#
# try:
#     raw = pd.read_excel('E:\Documents\Datasets\Life Data\\2020 sheets\Daily log 2020.xlsx', sheet_name=None, index_col=1, skiprows=[1])
# except OSError:
#     raw = None