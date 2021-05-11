
'''
TODO:

Determine best way to hold data while waiting for button clicks

What information should be displayed in order to determine what new data should be read in to the master

'''

import wx
import daily_log_processing

class MasterTab(wx.Panel):
    '''
    Will need to show state of current master pickle file

    Will need to have buttons to integrate new data of each type

    Or maybe this will be a summary tab?
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "hi")


class LifeTab(wx.Panel):
    '''
    Needs import button as well as showing state of current master file, vs new data
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.read_xls_but = wx.Button(self, -1, "Read log")
        self.read_xls_but.Bind(wx.EVT_BUTTON, self.read_log)

    def read_log(self, event):

        path = MainFrame.getpath(self, "E:/")
        print(path)

        #master_log, lin_log = daily_log_processing.import_lifelog()

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

    def getpath(self, default):
        openFileDialog = wx.FileDialog(self,
                                       "Open spreadsheet",
                                       "", "",
                                       "Excel files (*.xls, *.xlsx)|*.xls, *xlsx",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        return openFileDialog.GetPath()

class LifeLogApp(wx.App):
    def OnInit(self):
        frame = MainFrame()
        self.SetTopWindow(frame)
        frame.Show()
        return 1

if __name__ == "__main__":

    app = LifeLogApp()
    app.MainLoop()