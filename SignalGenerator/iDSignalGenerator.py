import tkinter as tk
from GUIHelper._GUI import GUI


class DSignalGenerator(tk.Tk):

    OnGenerateSignalButtonClick = None
    ####################################
    controls = {}
    signalPlotters = {}
    signalNameEntry = None
    thetaParamEntry = None
    rangeToEntry = None
    aParamEntry = None
    frequencyEntry = None
    signalTypeVar = None
    nSamplesEntry = None

    def __init__(self, master=None):
        GUI.InitRootApp(self, master, title="Generator Window")
        self.attributes('-topmost', True)
        self.__initEntries()

    def BindAndLoad(self):
        self.__drawGui()

    def Show(self):
        self.focus()
        self.mainloop()

    def GetPlotter(self, plotterName):
        return self.signalPlotters[plotterName]

    def GetSignalAmblitude(self):
        return self.aParamEntry.get()

    def GetSignalName(self):
        return self.signalNameEntry.get()

    def GetPhaseShift(self):
        return self.thetaParamEntry.get()

    def GetSignalFrequency(self):
        return self.frequencyEntry.get()

    def GetSignalFs(self):
        return self.fsFrequencyEntry.get()

    def GetSignalType(self):
        return self.signalTypeVar.get()

    def GetSamplesCount(self):
        return self.nSamplesEntry.get()

    def DrawPlotter(self):
        GUI.DrawSignalPlot(self, [], name='generatedSignalPlotter',
                           text='Generated Signal', position=(2, 0), padX=5, padY=5)

    def __drawGui(self):
        GUI.DrawGroupBox(self, name="propGroupBox", text="Signal Properties",
                         position=(0, 0), sticky=(tk.NSEW), padX=5, padY=5)
        propGroupBox = self.controls["propGroupBox"]

        GUI.DrawLabel(self, name="nameLabel", text="Name: ",
                      position=(0, 0), owner=propGroupBox, sticky=(tk.NW))

        GUI.DrawEntry(self, name="nameEntry",
                      position=(0, 1), owner=propGroupBox,
                      variable=self.signalNameEntry, sticky=(tk.NE))

        GUI.DrawLabel(self, name="label1", text="Signal Type:",
                      position=(1, 0), owner=propGroupBox, sticky=(tk.NW))
        signalTypes = ['Cos', 'Sin']

        GUI.DrawOptions(self, self.signalTypeVar, *signalTypes,
                        name="signalTypeOptions", position=(1, 1),
                        owner=propGroupBox, sticky=tk.NE)

        GUI.DrawGroupBox(self, name="signalParams", text="Params.", columnSpan=2, position=(
            2, 0), owner=propGroupBox, padX=5, padY=5)
        paramsGroupBox = self.controls['signalParams']

        GUI.DrawLabel(self, name="nSamplesLabel", text="Number of Samples:",
                      position=(0, 0), owner=paramsGroupBox, sticky=(tk.NW))

        GUI.DrawEntry(self, name="nSamplesEnt", variable=self.nSamplesEntry,
                      position=(0, 1), owner=paramsGroupBox, sticky=(tk.NE))

        GUI.DrawLabel(self, name="aParam", text="A:", position=(
            1, 0), owner=paramsGroupBox, sticky=(tk.NW))

        GUI.DrawEntry(self, name="aParamEntry",
                      position=(1, 1), owner=paramsGroupBox,
                      variable=self.aParamEntry, sticky=(tk.NE))

        GUI.DrawLabel(self, name="thetaLabel", text="Theta:",
                      position=(2, 0), owner=paramsGroupBox, sticky=(tk.NW))

        GUI.DrawEntry(self, name="thetaEntry", variable=self.thetaParamEntry,
                      position=(2, 1), owner=paramsGroupBox, sticky=(tk.NE))

        GUI.DrawLabel(self, name="freqLabel", text="Frquencey Files",
                      position=(3, 0), owner=paramsGroupBox, sticky=(tk.NW))

        GUI.DrawEntry(self, name="freqEntry", variable=self.frequencyEntry,
                      position=(3, 1), owner=paramsGroupBox, sticky=(tk.NE))

        GUI.DrawLabel(self, name="freqLabel2", text="Frequency(Fs):",
                      position=(4, 0), owner=paramsGroupBox, sticky=(tk.NW))

        GUI.DrawEntry(self, name="freqEntry2", variable=self.fsFrequencyEntry,
                      position=(4, 1), owner=paramsGroupBox, sticky=(tk.NE))

        GUI.DrawButton(self, name="btn",
                       position=(1, 0), text="Generate", columnSpan=2, padY=5,
                       onClickCommand=self.OnGenerateSignalButtonClick)

        GUI.DrawSignalPlot(self, [], name='generatedSignalPlotter',
                           text='Generated Signal', position=(2, 0), padX=5, padY=5)

    def __initEntries(self):
        self.signalNameEntry = tk.StringVar(self, "mysignal")
        self.thetaParamEntry = tk.IntVar(self, 45)
        self.aParamEntry = tk.IntVar(self, 20)
        self.frequencyEntry = tk.IntVar(self, 100)
        self.fsFrequencyEntry = tk.IntVar(self, 1800)
        self.signalTypeVar = tk.StringVar(self, 'Sin')
        self.nSamplesEntry = tk.IntVar(self, 20)
