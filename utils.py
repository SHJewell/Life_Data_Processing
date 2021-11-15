'''
This is a file containing all the useful functions which can be used by any class

This may be folded into the GUI as that develops
'''

def word_processor(string):

    string = str(string)

    if (string in ["", None]) or (len(string) == 0):
        return

    mid = string.replace("\\n","")
    mid = mid.replace("\n","")
    mid = mid.replace("&","and")

    if (mid in ["", None]) or (len(mid) == 0):
        return

    mid = mid.strip()

    if mid in ["", None]:
        return
    else:
        return mid.lower()

# def read_excel(path, sheet, )
#
# try:
#     raw = pd.read_excel('E:\Documents\Datasets\Life Data\\2020 sheets\Daily log 2020.xlsx', sheet_name=None, index_col=1, skiprows=[1])
# except OSError:
#     raw = None