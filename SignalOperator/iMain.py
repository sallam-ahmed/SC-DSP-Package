import tkinter as tk
from GUIHelper._GUI import GUI


class MainInterface(tk.Tk):
    ################################## Events #####################################
    # Navigation
    OnLoadSignalButtonClicked = None
    OnSaveSignalButtonClicked = None
    OnGeneratorOpenCommand = None
    OnChannelSelectedCommand = None
    OnExit = None
    OnPlotChannelButtonClicked = None
# Manipulations
    OnAddSignalsButtonClicked = None
    OnSubtractSignalsButtonClicked = None
    OnMultiplySignalsButtonClicked = None
  
    OnCombineSignals = None
    OnAccumulateSignals = None

# Quantization
    OnMenuOpenQuantizerClicked = None
    OnQuantizeButtonClicked = None
    OnClearSignals = None
    OnQuantizeButtonBitsClicked = None
# FFT
    OnApplyFFTInverseCommand = None
    OnApplyFFTCommand = None
    OnApplyFastFourierCommand = None
    OnApplyIFFTComman = None
# Signal Shifting/Folding
    OnSignalShift = None
    OnSignalFold = None
################################### Vars ######################################
###############################################################################
    controls = {}
    signalPlotters = {}
    previewPanel = None
    selectedFilter = 0
    defaultImage = None
    plottingMode = None
    LoadedSignalName = None
###############################################################################

    def __init__(self, master=None):
        GUI.InitRootApp(self, master, title="SC-DSP'18",
                        resizable=(False, False))
        self.attributes('-fullscreen', True)
        self.__initVars()

    def RenderGui(self):
        self.__drawGui()
################################### Funcs #####################################
###############################################################################

    def GetStatusText(self):
        return self.controls["StatusLabel"]

    def GetPlotter(self, plotterName):
        return self.signalPlotters[plotterName]

    def test(self):
        print(self.plottingMode.get())

    def GetPlottingMode(self):
        return self.plottingMode.get()

    def GetSignalNameLabel(self):
        return self.controls["signalName"]

    def GetSignalPathLabel(self):
        return self.controls["signalPath"]

    def GetSignalChannelsNoLabel(self):
        return self.controls["signalChannelsNo"]

    def GetChannelsListBox(self):
        return self.controls["channelsListBox"]

    def GetQuantizationLevel(self):
        return self.qLevelsVar.get()

    def GetQuantizationBitsLevel(self):
        return 2**self.qLevelsBits.get()

    def ChangePlotterTitle(self, plotterName, plotterTitle):
        self.signalPlotters[plotterName][0].configure(title=plotterTitle)

    def DrawPlotters(self):
        tk.Grid.columnconfigure(self.previewPanel, 1, weight=1)
        GUI.DrawSignalPlot(self, name="defaultPlotter",
                           signalData=[], position=(1, 0),
                           owner=self.previewPanel, sticky=tk.NSEW)

        GUI.DrawSignalPlot(self, name="resultPlotter",
                           signalData=[],
                           position=(1, 1), owner=self.previewPanel,
                           text="Result View", sticky=tk.NSEW)

    def DrawResultPlotter(self, xlabel, ylabel, _title):
        GUI.DrawSignalPlot(self, name="resultPlotter",
                           signalData=[],
                           position=(2, 0), owner=self.previewPanel, xLabel=xlabel, yLabel=ylabel,
                           text=_title, sticky=tk.NSEW)

    def DrawDefaultPlotter(self, xlabel, ylabel, _title):
        GUI.DrawSignalPlot(self, name="defaultPlotter",
                           signalData=[], position=(1, 0), xLabel=xlabel, yLabel=ylabel,
                           owner=self.previewPanel, sticky=tk.NSEW, text=_title)
################################### Private ###################################
###############################################################################

    def __initVars(self):
        self.constantMultiplier = tk.IntVar(self, 2)
        self.plottingMode = tk.StringVar(self.master)
        self.LoadedSignalName = tk.StringVar(self.master)
        self.qLevelsVar = tk.IntVar(self, 4)
        self.qLevelsBits = tk.IntVar(self, 4)
        # Shift a folded signal or normal signal
        self.boolShiftFoldedSignal = tk.BooleanVar(self, False)
        self.boolUseFastMethod = tk.BooleanVar(self, False)  # FFT or DFT

    def __setup_menubar(self):
        # create a toplevel menu
        menubar = tk.Menu(self)
        # File Menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New",
                             command=self.OnGeneratorOpenCommand)
        filemenu.add_command(label="Load",
                             command=self.OnLoadSignalButtonClicked)
        filemenu.add_command(label="Save",
                             command=self.OnSaveSignalButtonClicked)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.OnExit)

        menubar.add_cascade(label="File", menu=filemenu)
        # Edit Menu

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Clear",
                              command=self.OnClearSignals)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        # Operations
        operations_menu = tk.Menu(menubar, tearoff=0)
        operations_menu.add_command(label="Add",
                                    command=self.OnAddSignalsButtonClicked)
        operations_menu.add_command(label="Subtract",
                                    command=self.OnSubtractSignalsButtonClicked)
        operations_menu.add_command(label="Multiply",
                                    command=self.OnMultiplySignalsButtonClicked)
        operations_menu.add_separator()
        operations_menu.add_command(
            label="Combine", command=self.OnCombineSignals)
        operations_menu.add_command(
            label="Accumulate", command=self.OnAccumulateSignals)
        operations_menu.add_separator()

        quantize_submenu = tk.Menu(operations_menu, tearoff=0)

#        quantize_submenu.add_checkbutton(label = "Use Bit Mode")
        quantize_submenu.add_command(
            label="Quantize Signal", command=self.OnQuantizeButtonClicked)
        operations_menu.add_cascade(label="Quantize", menu=quantize_submenu)
####
        fourier_submenu = tk.Menu(operations_menu, tearoff=0)
        fourier_submenu.add_command(
            label="Apply DFT", command=self.OnApplyFFTCommand)
        fourier_submenu.add_command(
            label="Apply Inverse DFT", command=self.OnApplyFFTInverseCommand)
        fourier_submenu.add_command(
            label="Apply FFT", command=self.OnApplyFastFourierCommand)
        fourier_submenu.add_command(
            label="Apply Inverse FFT", command=self.OnApplyIFFTComman)
        operations_menu.add_cascade(
            label="Fourier Transform", menu=fourier_submenu)
        menubar.add_cascade(label="Operations", menu=operations_menu)

        help_meunbar = tk.Menu(menubar, tearoff=0)
        help_meunbar.add_cascade(label="About", command=lambda: print("About"))
        help_meunbar.add_command(label="Contribution",
                                 command=lambda: print("Cont"))
        menubar.add_cascade(label="Help", menu=help_meunbar)
        self.configure(menu=menubar)

    def __drawGui(self):
        self.__setup_menubar()

# Loading Group
        GUI.DrawGroupBox(self, name="loadingGroup", text="Load Signal",
                         position=(0, 0), padX=5, sticky=(tk.N+tk.S+tk.E+tk.W))

        loadingGroup = self.controls["loadingGroup"]
        GUI.DrawLabel(self, name="desc",
                      text="Select a signal file.",
                      position=(0, 0), padY=5, owner=loadingGroup, sticky=tk.NW)
        GUI.DrawButton(self, name="loadButton", text="Load Signal",
                       position=(0, 1),
                       owner=loadingGroup, padX=10, padY=5,
                       sticky=(tk.NE),
                       onClickCommand=self.OnLoadSignalButtonClicked)

        GUI.DrawButton(self, name="loadButton", text="Clear",
                       position=(0, 2),
                       owner=loadingGroup, padX=10, padY=5,
                       sticky=(tk.NE),
                       onClickCommand=self.OnClearSignals)

        GUI.DrawButton(self, name="addButton", text="Add Signals",
                       position=(1, 0), owner=loadingGroup, padX=5, padY=5,
                       onClickCommand=self.OnAddSignalsButtonClicked, sticky=tk.NW)
        GUI.DrawButton(self, name="subBtn", text="Subtract Signals",
                       position=(1, 1), owner=loadingGroup, padX=5, padY=5,
                       onClickCommand=self.OnSubtractSignalsButtonClicked, sticky=tk.NE)
        GUI.DrawButton(self, name="mulBtn", text="Multiply",
                       position=(2, 0), owner=loadingGroup, padX=5, padY=5,
                       onClickCommand=self.OnMultiplySignalsButtonClicked, sticky=tk.NW)
        GUI.DrawEntry(self, name="mul", variable=self.constantMultiplier,
                      position=(2, 1), owner=loadingGroup,
                      sticky=tk.NE, padX=5, padY=5)
        GUI.DrawGroupBox(self, name="qBox", text="Quantize",
                         position=(3, 0), columnSpan=3, owner=loadingGroup, padX=5, sticky=(tk.N+tk.S+tk.E+tk.W))

        qbox = self.controls["qBox"]

        GUI.DrawLabel(self, name="lb1", padX=5, padY=5, text="No. of levels:", position=(0, 0),
                      sticky=tk.NE, owner=qbox)
        GUI.DrawEntry(self, name="levelsEntry", padX=5, padY=5, variable=self.qLevelsVar,
                      owner=qbox, position=(0, 1), sticky=tk.NW)
        GUI.DrawLabel(self, name="lb2", padX=5, padY=5, text="No. of bits:", position=(1, 0),
                      sticky=tk.NE, owner=qbox)
        GUI.DrawEntry(self, name="bitsEntry", padX=5, padY=5, variable=self.qLevelsBits,
                      owner=qbox, position=(1, 1), sticky=tk.NW)

        GUI.DrawButton(self, name="qButton", text="Quantize Signal",
                       position=(2, 0), columnSpan=2, padX=5, padY=5,
                       owner=qbox, sticky=tk.NSEW, onClickCommand=self.OnQuantizeButtonClicked)

        GUI.DrawButton(self, name="qButton", text="Quantize Signal(Bits)",
                       position=(3, 0), columnSpan=2, padX=5, padY=5,
                       owner=qbox, sticky=tk.NSEW, onClickCommand=self.OnQuantizeButtonBitsClicked)

        GUI.DrawGroupBox(self, name="qvBox", padX=5, padY=5, text="Quantization Values",
                         position=(4, 0), columnSpan=2, owner=qbox, sticky=tk.NSEW)
        qvbox = self.controls["qvBox"]

        GUI.DrawLabel(self, name="lblError", text="Error Rate", position=(0, 0),
                      sticky=tk.NE, owner=qvbox)

        GUI.DrawLabel(self, name="lblErrorValue", text="00", position=(0, 1),
                      sticky=tk.NW, owner=qvbox)

        GUI.DrawGroupBox(self, name='fourierBox', text='Fourier Transform', position=(
            1, 0), columnSpan=2, sticky=tk.NSEW)
        ffBox = self.controls['fourierBox']
        GUI.DrawButton(self, name='applyFFT', text='Apply FFT', position=(
            0, 0), owner=ffBox, onClickCommand=self.OnApplyFFTCommand, sticky=tk.NSEW)
        GUI.DrawButton(self, name='applyIFFT', text='Apply IFFT', position=(
            1, 0), owner=ffBox, onClickCommand=self.OnApplyFFTInverseCommand, sticky=tk.NSEW)

# Preview Panel
        GUI.DrawGroupBox(self, name="previewGroup", text="Preview Panel",
                         position=(0, 1), rowSpan=5, padX=5,
                         sticky=(tk.N+tk.S+tk.E+tk.W))

        previewPanel = self.controls["previewGroup"]
        tk.Grid.columnconfigure(self, 1, weight=1)

        self.previewPanel = previewPanel
        GUI.DrawLabel(self, name="Preview",
                      text="Each Signal has a unique color!",
                      position=(0, 0), owner=previewPanel,
                      columnSpan=1, sticky=tk.NSEW)

# Signal Plot
        self.DrawPlotters()
