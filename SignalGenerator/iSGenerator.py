import tkinter as tk
from GUIHelper._GUI import GUI

class SignalGenerator(tk.Tk):
        
        OnGenerateSignalButtonClick = None
        ####################################
        controls = {}
        channelsCountEntry = None
        signalNameEntry = None
        rangeFromEntry = None
        rangeToEntry = None
        seedEntry= None
        sampleCount = None
        def __init__(self,master = None):
                GUI.InitRootApp(self,master,title="Generator Window")
                self.attributes('-topmost', True)
                self.__initEntries()
                
        def BindAndLoad(self):
                self.__drawGui()
                
        def Show(self):
                self.focus()
                self.mainloop()
        
        def GetChannelsCount(self):
                return self.channelsCountEntry.get()
        def GetSeed(self):
                return self.seedEntry.get()
        def GetSignalName(self):
                return self.signalNameEntry.get()
        def GetRangeFrom(self):
                return self.rangeFromEntry.get()
        def GetRangeTo(self):
                return self.rangeToEntry.get()
        def GetSamplesCount(self):
                return self.sampleCount.get()
                
        def __drawGui(self):
                GUI.DrawGroupBox(self,name = "propGroupBox",text = "Signal Properties",
                                 position=(0,0),sticky=(tk.NSEW),padX= 5,padY = 5)
                propGroupBox = self.controls["propGroupBox"]
        
                GUI.DrawLabel(self,name = "nameLabel", text="Name: ",
                              position= (0,0),owner = propGroupBox,sticky=(tk.NW))
                
                GUI.DrawEntry(self, name="nameEntry",
                              position=(0,1),owner = propGroupBox,
                              variable=self.signalNameEntry, sticky=(tk.NE))
                
                GUI.DrawLabel(self,name = "label1", text="Channels Count: ",
                              position= (1,0),owner = propGroupBox,sticky=(tk.NW))

                GUI.DrawEntry(self, name="noEntry", position=(1,1),owner = propGroupBox,
                              variable=self.channelsCountEntry,sticky=(tk.NE))


                GUI.DrawLabel(self, name="seedLbl",text = "Random Seed:",position=(2,0),owner=propGroupBox,sticky=(tk.NW))

                GUI.DrawEntry(self, name="seedEntry", 
                              position=(2,1), owner=propGroupBox,
                                variable = self.seedEntry, sticky=(tk.NE))
                


                GUI.DrawLabel(self, name="rangeFromLbl",text = "Ranges from:",position=(3,0),owner=propGroupBox,sticky=(tk.NW))

                GUI.DrawEntry(self, name="rangeFromEntry",variable = self.rangeFromEntry,
                              position=(3,1), owner=propGroupBox,sticky=(tk.NE))
                


                GUI.DrawLabel(self, name="rangeToLbl",text = "Ranges to:",position=(4,0),owner=propGroupBox,sticky=(tk.NW))

                GUI.DrawEntry(self, name="rangeToEntry", variable = self.rangeToEntry,
                              position=(4,1), owner=propGroupBox,sticky=(tk.NE))           
                
                GUI.DrawLabel(self, name="sampleCntLbl",text = "Samples:",position=(5,0),owner=propGroupBox,sticky=(tk.NW))

                GUI.DrawEntry(self, name="samplesEntry", variable = self.sampleCount,
                              position=(5,1), owner=propGroupBox,sticky=(tk.NE))           
                
                GUI.DrawButton(self, name = "btn",
                               position=(1,0), text = "Generate",columnSpan=2,padY = 5,
                               onClickCommand = self.OnGenerateSignalButtonClick)
                
                
        def __initEntries(self):
                print("INIT")
                self.channelsCountEntry = tk.IntVar(self,1)
                self.signalNameEntry = tk.StringVar(self,"mysignal")                
                self.rangeFromEntry = tk.IntVar(self,1)
                self.rangeToEntry = tk.IntVar(self,20)
                self.seedEntry= tk.IntVar(self,11244)               
                self.sampleCount = tk.IntVar(self, 20)
