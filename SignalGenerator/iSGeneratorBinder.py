import numpy as np
from SignalOperations._signalParser import SignalParser
import tkinter as tk

class SignalGeneratorEvents:
        
        def __init__(self,app):
                self.app = app
                self.signalMarkers = [(i,j) for i in 'oD<.' for j in 'bgrcmyk']
                np.random.shuffle(self.signalMarkers)
                
        def BindEvents(self):
                self.app.OnGenerateSignalButtonClick = self.OnGenerateSignalButtonClick
                self.app.BindAndLoad()
                self.app.Show()
                self.app.focus_set()
                       
        def OnGenerateSignalButtonClick(self):
                # Get arguments first
                channelsCount = self.app.GetChannelsCount()
                signalName = self.app.GetSignalName()
                lower = self.app.GetRangeFrom()
                higher = self.app.GetRangeTo()
                seed = self.app.GetSeed()
                samples = self.app.GetSamplesCount()
                generatedChannels = []
                print(self.signalMarkers)
                generatedMarkers = self.signalMarkers[:channelsCount]
                print(generatedMarkers)
                np.random.seed(seed)
                for i in range(channelsCount):
                        channel = np.random.randint(lower,higher,size = samples)
                        generatedChannels.append(channel)
                
                typevar = tk.StringVar()
                typevar.set("saasasd")
                filetypes =[("Signal files", "*.sgn")]
                fname = tk.filedialog.asksaveasfilename(filetypes = filetypes,typevariable = typevar)
                if fname:
                        selectedTypeExtension = [ y for y in filetypes if (y[0] == typevar.get())][0]
                        pureExtension = selectedTypeExtension[1].split('.')[1]
                        fname += '.'+pureExtension
                        SignalParser.GenerateSignalFile(fname,name = signalName,
                                                        channels= generatedChannels,
                                                        markers = generatedMarkers)
                else:
                        print("Error")