import tkinter as tk
from GUIHelper._GUI import GUI


class MainInterface(tk.Tk):
    ################################## Events #####################################
    # Navigation
    OnLoadSignalButtonClicked = None
    OnSaveSignalButtonClicked = None
    OnGeneratorOpenCommand = None
    OnExit = None
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

    def GetBoolUseBitMode(self):
        return self.useBitModeVar.get()
   
    def ChangePlotterTitle(self, plotterName, plotterTitle):
        self.signalPlotters[plotterName][0].configure(title=plotterTitle)

    def DrawPlotters(self):
        tk.Grid.rowconfigure(self.previewPanel, 1, weight=1)
        tk.Grid.columnconfigure(self.previewPanel, 1, weight=1)
        GUI.DrawAxisArray(self, name='plotters_axis', position=(
            1, 0), owner=self.previewPanel, columnSpan=2,  sticky=tk.NSEW)

    def ChangeAxisTitle(self, i, j, _title):
        axis_array = self.signalPlotters['plotters_axis'][0]
        axis_array[i, j].set(title=_title)
        self.repaint_axis()

    def repaint_axis(self):
        self.signalPlotters['plotters_axis'][1].draw()

    def GetAxis(self, i, j):
        return self.signalPlotters['plotters_axis'][0][i,j]

    def DrawResultPlotter(self, xlabel, ylabel, _title):
        GUI.DrawSignalPlot(self, name="resultPlotter",
                           signalData=[],
                           position=(2, 0), owner=self.previewPanel, xLabel=xlabel, yLabel=ylabel,
                           text=_title, sticky=tk.NSEW)

    def DrawDefaultPlotter(self, xlabel, ylabel, _title):
        GUI.DrawSignalPlot(self, name="defaultPlotter",
                           signalData=[], position=(1, 0), xLabel=xlabel, yLabel=ylabel,
                           owner=self.previewPanel, sticky=tk.NSEW, text=_title)


    def GetStdOperationsAxis(self):
        ax_str = self.std_working_axis.get()
        x = int(ax_str[1])
        y = int(ax_str[3])
        return (x,y)
    
    def GetQuantizeOperationsAxis(self):
        ax_str = self.q_working_axis.get()
        x = int(ax_str[1])
        y = int(ax_str[3])
        
        return (x,y)    
    def GetFourierOperationsAxis(self):
        ax_str = self.f_working_axis.get()
        x = int(ax_str[1])
        y = int(ax_str[3])
        return (x,y)
    
    def GetManipulationOperationsAxis(self):
        ax_str = self.manp_working_axis.get()
        x = int(ax_str[1])
        y = int(ax_str[3])
        return (x,y)
################################### Private ###################################
###############################################################################

    def __initVars(self):
        self.constantMultiplier = tk.IntVar(self, 2)
        self.plottingMode = tk.StringVar(self.master)
        self.LoadedSignalName = tk.StringVar(self.master)
        self.qLevelsVar = tk.IntVar(self, 4)
        # Shift a folded signal or normal signal
        self.boolShiftFoldedSignal = tk.BooleanVar(self, False)

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

        quantize_submenu.add_command(
            label="Quantize Signal", command=self.OnQuantizeButtonClicked)
        operations_menu.add_cascade(label="Quantize", menu=quantize_submenu)
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
                         position=(0, 0), padX=5, sticky=tk.NSEW)

        loadingGroup = self.controls["loadingGroup"]
        
        GUI.DrawButton(self, name="newBtn", text="New Signal",
                       position=(0, 0),
                       owner=loadingGroup, padX=10, padY=5,
                       sticky=(tk.NW),
                       onClickCommand=self.OnLoadSignalButtonClicked)

        GUI.DrawButton(self, name="loadButton", text="Load Signal",
                       position=(0, 1),
                       owner=loadingGroup, padX=10, padY=5,
                       sticky=(tk.NE),
                       onClickCommand=self.OnLoadSignalButtonClicked)

        GUI.DrawButton(self, name="saveBtn", text="Save",
                       position=(1, 0),
                       owner=loadingGroup, padX=10, padY=5,
                       sticky=(tk.NW),
                       onClickCommand=self.OnSaveSignalButtonClicked)

        GUI.DrawButton(self, name="clrBtn", text="Clear",
                       position=(1, 1),
                       owner=loadingGroup, padX=10, padY=5,
                       sticky=(tk.NE),
                       onClickCommand=self.OnClearSignals)
###
        GUI.DrawGroupBox(self, name='OperationsBox', text='Operations', position=(
            1, 0), sticky=tk.NSEW, padX=5)
        operationsBox = self.controls['OperationsBox']
       
       #STD Operations
        GUI.DrawGroupBox(self, name='std', text='Standard Operations', position=(
            0, 0), owner=operationsBox, sticky=tk.NSEW)
        
        stdBox = self.controls['std']

        axisArray = ['(0,1)', '(1,0)', '(1,1)']
        self.std_working_axis = tk.StringVar(self, '(0,1)')
        
        GUI.DrawLabel(self, name='axlbl', text='Axis:',
                      position=(0, 0), owner=stdBox, sticky=tk.NW)
        GUI.DrawOptions(self, self.std_working_axis, *axisArray, name='std_ax_op',
                        position=(0, 1), owner=stdBox, sticky=tk.NE)

        GUI.DrawButton(self, name="addButton", text="Add Signals",
                       position=(1, 0), owner=stdBox, padX=5, padY=5,
                       onClickCommand=self.OnAddSignalsButtonClicked, sticky=tk.NW)
        GUI.DrawButton(self, name="subBtn", text="Subtract Signals",
                       position=(1, 1), owner=stdBox, padX=5, padY=5,
                       onClickCommand=self.OnSubtractSignalsButtonClicked, sticky=tk.NE)
        GUI.DrawButton(self, name="mulBtn", text="Multiply",
                       position=(2, 0), owner=stdBox, padX=5, padY=5,
                       onClickCommand=self.OnMultiplySignalsButtonClicked, sticky=tk.NW)
        GUI.DrawEntry(self, name="mul", variable=self.constantMultiplier,
                      position=(2, 1), owner=stdBox,
                      sticky=tk.NE, padX=5, padY=5)
       #Quantize Operations
        GUI.DrawGroupBox(self, name="qBox", text="Quantize",
                         position=(1, 0), owner=operationsBox, padX=5, sticky=(tk.N+tk.S+tk.E+tk.W))

        qbox = self.controls["qBox"]

        self.q_working_axis = tk.StringVar(self, '(0,1)')
        GUI.DrawLabel(self, name='axlbl', text='Axis:',
                      position=(0, 0), owner=qbox, sticky=tk.NW)
        GUI.DrawOptions(self, self.q_working_axis, *axisArray, name='q_ax_op',
                        position=(0, 1), owner=qbox, sticky=tk.NE)

        GUI.DrawLabel(self, name="lb1", padX=5, padY=5, text="No. of levels:", position=(1, 0),
                      sticky=tk.NE, owner=qbox)
        GUI.DrawEntry(self, name="levelsEntry", padX=5, padY=5, variable=self.qLevelsVar,
                      owner=qbox, position=(1, 1), sticky=tk.NW)
        self.useBitModeVar = tk.IntVar(self, 0)
        GUI.DrawCheckBox(self, self.useBitModeVar, name='bitmodecheck', text='Use Bit Mode(levels are #bits)',
                         padX=5, padY=5, owner=qbox, columnSpan=2, position=(2, 0), sticky=tk.NW)

        GUI.DrawButton(self, name="qButton", text="Quantize Signal",
                       position=(3, 0), columnSpan=2, padX=5, padY=5,
                       owner=qbox, sticky=tk.NSEW, onClickCommand=self.OnQuantizeButtonClicked)

        GUI.DrawGroupBox(self, name="qvBox", padX=5, padY=5, text="Quantization Values",
                         position=(4, 0), columnSpan=2, owner=qbox, sticky=tk.NSEW)
        qvbox = self.controls["qvBox"]

        GUI.DrawLabel(self, name="lblError", text="Error Rate", position=(0, 0),
                      sticky=tk.NE, owner=qvbox)

        GUI.DrawLabel(self, name="lblErrorValue", text="00", position=(0, 1),
                      sticky=tk.NW, owner=qvbox)
       
       #Fourier Transform

        GUI.DrawGroupBox(self, name="fourierBox", text="Fourier Transform",
                         position=(2, 0), owner=operationsBox, padX=5, sticky=tk.NSEW)

        ffBox = self.controls['fourierBox']

        self.f_working_axis = tk.StringVar(self, '(0,1)')
        tk.Grid.columnconfigure(ffBox, 0, weight = 1)
        GUI.DrawLabel(self, name='axlbl', text='Axis:',
                      position=(0, 0), owner=ffBox, sticky=tk.NW)

        GUI.DrawOptions(self, self.f_working_axis, *axisArray, name='f_ax_op',
                        position=(0, 1), owner=ffBox, sticky=tk.NW)
   
   
        GUI.DrawGroupBox(self, name= 'stdft',columnSpan=2, padX = 5, padY = 5, text = 'Standard Fourier Transform', owner = ffBox, position=(1,0), sticky= tk.NSEW)

        std_ft = self.controls['stdft'] 
        tk.Grid.columnconfigure(std_ft, 0, weight = 1)

        GUI.DrawButton(self, name='applyFFT', padX = 5, padY = 5, text='Apply Transform', position=(
            0, 0), owner=std_ft, onClickCommand=self.OnApplyFFTCommand, sticky=tk.NSEW)
        
        GUI.DrawButton(self, name='applyIFFT', padX = 5, padY = 5, text='Apply Inverse Transform', position=(
            1, 0), owner=std_ft, onClickCommand=self.OnApplyFFTInverseCommand, sticky=tk.NSEW)
        
        GUI.DrawGroupBox(self, name= 'fft', columnSpan=2,padX = 5, padY = 5,   text = 'Fast Fourier Transform', owner = ffBox, position=(2,0), sticky= tk.NSEW)
        fft_box = self.controls['fft'] 
        tk.Grid.columnconfigure(fft_box, 0, weight = 1)
        GUI.DrawButton(self, name='applyFFT', padX = 5, padY = 5, text='Apply Fast Transform', position=(
            0, 0), owner=fft_box, onClickCommand=self.OnApplyFFTCommand, sticky=tk.NSEW)
        
        GUI.DrawButton(self, name='applyIFFT', padX = 5, padY = 5, text='Apply Fast Inverse Transform', position=(
            1, 0), owner=fft_box, onClickCommand=self.OnApplyFFTInverseCommand, sticky=tk.NSEW)

        GUI.DrawGroupBox(self, name = 'manpBox', text= 'Signal Manipulation', position=(3, 0), owner= operationsBox, sticky= tk.NSEW)
    # Signal Manipulations
        manpBox = self.controls['manpBox']
        
        self.manp_working_axis = tk.StringVar(self, '(0,1)')
        tk.Grid.columnconfigure(manpBox, 0, weight = 1)
        GUI.DrawLabel(self, name='axlbl', text='Axis:',
                      position=(0, 0), owner=manpBox, sticky=tk.NW)

        GUI.DrawOptions(self, self.manp_working_axis, *axisArray, name='manp_ax_op',
                        position=(0, 1), owner=manpBox, sticky=tk.NW)

        GUI.DrawGroupBox(self, name= 'signal_shiftBox',columnSpan=2, padX = 5, padY = 5, text = 'Shifting', owner = manpBox, position=(1,0), sticky= tk.NSEW)

        signal_shift_box = self.controls['signal_shiftBox'] 
        tk.Grid.columnconfigure(signal_shift_box, 0, weight = 1)
        
        GUI.DrawLabel(self, name = 'lb', text = 'Shift Amount', position=(0,0), owner=signal_shift_box, sticky=tk.NW)
        
        self.shiftAmountVar = tk.IntVar(self, 0)
        GUI.DrawEntry(self, self.shiftAmountVar, name = 'shftAmountentr', position=(0,1), owner=signal_shift_box, sticky= tk.NE)
        
        GUI.DrawCheckBox(self, self.boolShiftFoldedSignal, text = 'Folded Signal Shift', position=(1,0),columnSpan=2, owner=signal_shift_box, sticky=tk.NW)
        
        GUI.DrawButton(self, name='shiftSignalBtn', padX = 5, padY = 5, text='Shift Signal', position=(
            2, 0),columnSpan=2, owner=signal_shift_box, onClickCommand=self.OnApplyFFTCommand, sticky=tk.NSEW)
        
        GUI.DrawButton(self, name='fld_btn', text = 'Fold Signal', padX= 5, padY=5, owner=manpBox, sticky= tk.NSEW, position=(2,0), columnSpan= 2)
        
# Preview Panel
        tk.Grid.columnconfigure(self, 1, weight=1)
        tk.Grid.rowconfigure(self, 1, weight=1)
        GUI.DrawGroupBox(self, name="previewGroup", text="Preview Panel",
                         position=(0, 1), rowSpan=5, padX=5,
                         sticky=(tk.N+tk.S+tk.E+tk.W))

        previewPanel = self.controls["previewGroup"]

        self.previewPanel = previewPanel
        GUI.DrawLabel(self, name="Preview",
                      text="Each Signal has a unique color!",
                      position=(0, 0), owner=previewPanel,
                      columnSpan=1, sticky=tk.NSEW)

# Signal Plot
        self.DrawPlotters()