import numpy as np
from SignalOperations._signalParser import SignalParser
import tkinter as tk

class DSignalGeneratorEvents:

    def __init__(self, app):
        self.app = app

    def BindEvents(self):
        self.app.OnGenerateSignalButtonClick = self.OnGenerateSignalButtonClick
        self.app.BindAndLoad()
        self.app.Show()
        self.app.focus_set()

    def OnGenerateSignalButtonClick(self):
        # Get arguments first
        nSamples = self.app.GetSamplesCount()
        signalAmblitude = self.app.GetSignalAmblitude()
        phaseShift = self.app.GetPhaseShift()
        signalType = self.app.GetSignalType()
        signalFrequency = self.app.GetSignalFrequency()
        signalFs = self.app.GetSignalFs()
        self.finalSignal = []

        if signalType == 'Cos':  # We will use sin as  a base, shifted by 90 if cos is required
            phaseShift += 90

        for i in range(nSamples):
            sValue = signalAmblitude * \
                np.sin(2 * np.pi * signalFrequency/signalFs * i + phaseShift)
            self.finalSignal.append((i, sValue))

        self.PlotSignal(self.finalSignal)

    def PlotSignal(self, signalData):
        self.app.DrawPlotter()
        xVals = [x[0] for x in signalData]
        yVals = [x[1] for x in signalData]
        self.app.GetPlotter('generatedSignalPlotter')[0].scatter(
            xVals, yVals, marker='o', color='r', label='Signal')
        self.app.GetPlotter('generatedSignalPlotter')[0].legend(
            bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)

        self.app.GetPlotter('generatedSignalPlotter')[1].draw()

    def SaveSignal(self):
        pass
        # typevar = tk.StringVar()
        # typevar.set("saasasd")
        # filetypes =[("Signal files", "*.sgn")]
        # fname = tk.filedialog.asksaveasfilename(filetypes = filetypes,typevariable = typevar)
        # if fname:
        #         selectedTypeExtension = [ y for y in filetypes if (y[0] == typevar.get())][0]
        #         pureExtension = selectedTypeExtension[1].split('.')[1]
        #         fname += '.'+pureExtension
        #         extensionName = fname + '.'+pureExtension
        #         SignalParser.(extensionName,name = fname,
        #                                         channels= generatedChannels,
        #                                         markers = generatedMarkers)
        # else:
        #         print("Error")
