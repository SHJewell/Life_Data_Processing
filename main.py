
'''
General Structure
    Daily log, food and weight tracker modules should only deal with one year at a time.
        For large analysis, a dedicated module should be used

TODO:
    Determine best way to hold data while waiting for button clicks
    What information should be displayed in order to determine what new data should be read in to the master
    Should probably keep master .dats seperated like the spreadsheets as determing first/last dates from the master
    is a complete mess

'''

import wx
import pandas as pd
import daily_log_processing

class MasterTab(wx.Panel):
    '''
    Will need to show state of current master pickle file

    Will need to have buttons to integrate new data of each type

    Or maybe this will be a summary tab?
    '''

    weight = ['drinks', 'heart', '']

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "hi")


class LifeTab(wx.Panel):
    '''
    Needs import button as well as showing state of current master file, vs new data
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.read_xls_but = wx.Button(self, -1, "Import Log")
        self.read_xls_but.Bind(wx.EVT_BUTTON, self.read_log)

        self.start = wx.StaticText()
        self.stop = wx.StaticText()

    def initFrame(self):

        self.master = pd.read_pickle('E:\Documents\Datasets\Life_Data\Data files\master_calendar.dat')
        self.start.SetLabel(str(self.master.max()))

    def read_log(self, event):

        self.d_path = MainFrame.getpath(self)
        #print(self.d_path)

        self.master_log, self.lin_log = daily_log_processing.import_lifelog(self, self.d_path)

        #print(self.d_path, len(self.master_log))

        return self.master_log, self.lin_log

class FoodTab(wx.Panel):
    '''
    Biggest tab, will show list of missing foods

    GUI food entry?
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "hi")

class WeightTab(wx.Panel):
    '''
    Basic tab, import and compare missing dates
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "hi")

        self.weights = pd.read_pickle('E:\Documents\Datasets\Life_Data\Data files\master_calendar.dat')

class ProcessTab(wx.Panel):
    '''
    Will probably be most complicated,

    Will need to see about displaying dynamic plots
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "hi")


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Life Log Processor")
        wx.SystemOptions.SetOption(u"osx.openfiledialog.always-show-types", "1")

        pnl = wx.Panel(self)
        nb = wx.Notebook(pnl)

        tab1 = MasterTab(nb)
        tab2 = LifeTab(nb)
        tab3 = FoodTab(nb)
        tab4 = WeightTab(nb)
        tab5 = ProcessTab(nb)

        nb.AddPage(tab1, "Master Tab")
        nb.AddPage(tab2, "LifeLog")
        nb.AddPage(tab3, "Food Calendar")
        nb.AddPage(tab4, "Weight Tracker")
        nb.AddPage(tab5, "Data Processing")

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        pnl.SetSizer(sizer)

    def getpath(self):

        # naming the parameters breaks this because, fuck you right?
        fileDialog = wx.FileDialog(self,
                                   "Open spreadsheet",
                                   "",
                                   "E:\\Documents\\Datasets\\Life_Data",
                                   "Excel files (*.xlsx)|*.xlsx|" \
                                   "All files (*.*)|*.*",
                                   wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return

        # pathname = fileDialog.GetPath()

        # return pathname
        return fileDialog.GetPath()

class LifeLogApp(wx.App):
    def OnInit(self):
        frame = MainFrame()
        self.SetTopWindow(frame)
        frame.Show()
        return 1



if __name__ == "__main__":

    app = LifeLogApp()
    app.MainLoop()