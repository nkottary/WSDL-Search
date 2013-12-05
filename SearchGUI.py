'''
	GUI for the SearchEngine. We are using wxPython here.
'''
import wx
from SearchEngine import *
from htmlPresenter import *
from utils import *
import time

class SearchGUI(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(SearchGUI, self).__init__(*args, **kw) 
        
        self.InitUI()

        #flags indicating checkbox states.
        self.enrichFlag = False
        self.SVDFlag = False
        self.metric = COSINE

        #self.searchEng = SearchEngine()
        
        try:
            self.searchEng = SearchEngine()
        except Exception as e:
            self.errorMessage("Error: Feature vectors have not been created!")
            

    def InitUI(self):   

        '''
            Defining all the widgets.
        '''
        self.panel = wx.Panel(self)

        #Label indicating query.
        self.label = wx.StaticText(self.panel, label="What do you want to search for: ", size = (200, -1))

        #Text box for the query.
        self.queryBox = wx.TextCtrl(self.panel, size=(190, -1))

        self.checkPanel = wx.Panel(self.panel)

        #check box for query enrich
        self.enrichCheck = wx.CheckBox(self.checkPanel, label='Enrich Query', pos=(20, 20))
        self.enrichCheck.SetValue(False)
        self.enrichCheck.Bind(wx.EVT_CHECKBOX, self.changeEnrichFlag)

        #check box for SVD
        self.svdCheck = wx.CheckBox(self.checkPanel, label='SVD', pos=(20, 40))
        self.svdCheck.SetValue(False)
        self.svdCheck.Bind(wx.EVT_CHECKBOX, self.changeSVDFlag)

        #Radio buttons for similarity metrics
        self.rbPanel = wx.Panel(self.panel)
        self.rb1 = wx.RadioButton(self.rbPanel, label='Cosine', pos=(10, 10), style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(self.rbPanel, label='Norm', pos=(10, 30))
        self.rb3 = wx.RadioButton(self.rbPanel, label='Chebyshev', pos=(10, 50))
        self.rb4 = wx.RadioButton(self.rbPanel, label='Correlation', pos=(10, 70))

        self.rb1.Bind(wx.EVT_RADIOBUTTON, self.SetVal)
        self.rb2.Bind(wx.EVT_RADIOBUTTON, self.SetVal)
        self.rb3.Bind(wx.EVT_RADIOBUTTON, self.SetVal)
        self.rb4.Bind(wx.EVT_RADIOBUTTON, self.SetVal)

        #Search button
        self.searchButton = wx.Button(self.panel, label='Search', pos=(20, 30))
        self.searchButton.Bind(wx.EVT_BUTTON, self.executeSearch)

 		#managing layout
        self.sizer = wx.GridBagSizer(3, 2)
        self.sizer.Add(self.label, (0, 0))
        self.sizer.Add(self.queryBox, (0, 1))
        self.sizer.Add(self.checkPanel, (1, 0))
        self.sizer.Add(self.rbPanel, (1, 1))
        self.sizer.Add(self.searchButton, (2, 1))
    
        # Use the sizers
        self.panel.SetSizerAndFit(self.sizer) 
        self.SetSize((420,220))
        self.SetTitle('Search Web Service')
        self.Centre()
        self.Show(True)          
        
    def executeSearch(self, e):
        
        '''
            Execute the query depending on the enrich and SVD flags.
        '''
        
       	qString = self.queryBox.GetValue()

       	if not qString:
       		self.errorMessage("Your query is empty!")
       	else:
            if self.enrichFlag:
                qString = enrich(qString)

            try:    
                start = time.time()
                if self.SVDFlag:
                    sortedFileDist = self.searchEng.svdSearch(qString, self.metric)
                else:
                    sortedFileDist = self.searchEng.normalSearch(qString, self.metric)
                end = time.time()

                htmlPresenter(sortedFileDist, HTML_DIR, qString, end-start)
                self.successMessage()  
            except Exception as e:
                self.errorMessage(str(e))

    def changeSVDFlag(self, e):
        
        sender = e.GetEventObject()
        self.SVDFlag = sender.GetValue()  
        if self.SVDFlag:
            self.rbPanel.Disable()
        else:
            self.rbPanel.Enable()

    def changeEnrichFlag(self, e):
        
        sender = e.GetEventObject()
        self.enrichFlag = sender.GetValue()

    def SetVal(self, e):
        
        state1 = self.rb1.GetValue()
        state2 = self.rb2.GetValue()
        state3 = self.rb3.GetValue()
        state4 = self.rb4.GetValue()

        if state1:
            self.metric = COSINE
        elif state2:
            self.metric = NORM
        elif state3:
            self.metric = CHEBYSHEV
        else:
            self.metric = CORRELATION

    def errorMessage(self, msg):

        dial = wx.MessageDialog(None, msg, 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()      

    def successMessage(self):

        dial = wx.MessageDialog(None, 'Results are generated', 'Info', wx.OK)
        dial.ShowModal()       
        
if __name__ == '__main__':
    
    ex = wx.App()
    SearchGUI(None)
    ex.MainLoop()    


