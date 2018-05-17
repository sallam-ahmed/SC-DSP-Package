import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import tkinter as tk
from GUIHelper._GUI import GUI

import DSP.filters as fls
from DSP.digital_signal import DS_Signal
import numpy as np

from DSP.signal_op import convolve_signal, shift_signal
import scipy.signal as my_dsp_package

class DSignalFilter(tk.Tk):
    OnLoadSignal = None
    OnApplyFilter = None
    controls = {}
    signalPlotters = {}
    
    def __init__(self, master=None):
        GUI.InitRootApp(self, master, title="Filtering Window")
        self.attributes('-topmost', True)
        self.__initEntries__()

    def BindAndLoad(self):
        self.__drawGui__()
    
    def Show(self):
        self.focus()
        self.mainloop()
    def GetSelectedFilter(self):
        return self.selected_filter_entry.get()
    
    def GetAxis(self, i):
        return self.signalPlotters['axis_plotters'][0][i]
    
    def ChangeAxisTitle(self, i, _title):
        axis_array = self.signalPlotters['axis_plotters'][0]
        axis_array[i].set(title=_title)
        self.repaint_axis()

    def repaint_axis(self):
        self.signalPlotters['axis_plotters'][1].draw()


    def __drawGui__(self):
        GUI.DrawButton(self, name= 'loadBtn', text = 'Load Signal', position=(0,0),columnSpan=2, sticky= tk.NSEW, onClickCommand= self.OnLoadSignal)
        GUI.DrawButton(self, name= 'aptn', text = 'Apply Filter', position=(1,0),columnSpan=2, sticky= tk.NSEW, onClickCommand= self.OnApplyFilter)
        
        GUI.DrawGroupBox(self, name= 'fprop', position= (2,0), sticky= tk.NSEW, columnSpan=2, text= 'Filtering')
        fprop = self.controls['fprop']

        GUI.DrawLabel(self, name='lbl1', text= 'Sampling Frequency(hz)', position=(1,0), owner= fprop, sticky= tk.NW)
        GUI.DrawEntry(self, variable= self.fs_entry, name = 'sampling_freq', position=(1,1), padX= 5, sticky= tk.NE, owner= fprop)        
        
        # GUI.DrawLabel(self, name='lbl2', text= 'Transition Width(hz)', position=(2,0), owner= fprop)
        # GUI.DrawEntry(self, variable= self.tw_entry, name = 'tw', position=(2,1), padX= 5, sticky= tk.NE, owner= fprop)        
        
        GUI.DrawLabel(self, name='lbl3', text= 'Stop Attenuation(db)', position=(2,0), owner= fprop)
        GUI.DrawEntry(self, variable= self.sta_entry, name = 'st', position=(2,1), padX= 5, sticky= tk.NE, owner= fprop)        
        
        GUI.DrawLabel(self, name='lbl3', text= 'Transition Band(hz)', position=(3,0), owner= fprop)
        GUI.DrawEntry(self, variable= self.tband_entry, name = 'tband', position=(3,1), padX= 5, sticky= tk.NE, owner= fprop)        

        hlfilter = GUI.DrawGroupBox(self, name ='hlfilter', text= 'High/Low Filter', position=(0, 2), owner= fprop)
        
        GUI.DrawLabel(self, name='lbl4', text= 'Cutoff frequency (hz)', position=(0,0), owner= hlfilter)
        GUI.DrawEntry(self, variable= self.cutoff_entry, name = 'tband', position=(0,1), padX= 5, sticky= tk.NE, owner= hlfilter)        
        
        bandfilter = GUI.DrawGroupBox(self, name ='blfilter', text= 'Band pass/reject Filter', position=(2, 2), owner= fprop)
        
        GUI.DrawLabel(self, name='lbl4', text= 'Band1 frequency (hz)', position=(0,0), owner= bandfilter)
        GUI.DrawEntry(self, variable= self.band1_entry, name = 'tband', position=(0,1), padX= 5, sticky= tk.NE, owner= bandfilter)        
        
        GUI.DrawLabel(self, name='lbl4', text= 'Band2 frequency (hz)', position=(1,0), owner= bandfilter)
        GUI.DrawEntry(self, variable= self.band2_entry, name = 'tband', position=(1,1), padX= 5, sticky= tk.NE, owner= bandfilter)        
        
        filters = ['High', 'Low', 'Bandpass', 'Bandreject']

        GUI.DrawOptions(self, self.selected_filter_entry, *filters, name= 'op1', position=(4,2), owner= fprop)


        #GUI.DrawAxisArray(self, name= 'axis_plotters', text='Signal View', position=(5,0), columnSpan= 2)
        self.fig, self.axarr = plt.subplots(2, sharex=True)
        self.axarr[0].plot([], [])
        self.axarr[0].grid(True)
        self.axarr[0].set_title('Workspace')
        self.axarr[1].scatter([], [])
        self.axarr[1].grid(True)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.controls['axis_plotters'] = canvas.get_tk_widget()
        self.controls['axis_plotters'].grid(row=5, column=0, sticky= tk.NSEW, columnspan = 2)
        self.axis_array = self.controls['axis_plotters']
        self.signalPlotters['axis_plotters'] = (self.axarr, canvas, self.fig)
        canvas.show()
        
    def __initEntries__(self):
        self.fs_entry = tk.DoubleVar(self, 0.0)
        self.tw_entry = tk.DoubleVar(self, 1.0)
        self.sta_entry = tk.DoubleVar(self, 1.0)
        self.tband_entry = tk.DoubleVar(self, 1.0)
        self.cutoff_entry = tk.DoubleVar(self, 1.0)
        self.band1_entry  =tk.DoubleVar(self, 1.0)
        self.band2_entry  =tk.DoubleVar(self, 1.0)

        self.selected_filter_entry = tk.StringVar(self, 'High')



class DSignalFilterBinder:
    LoadedSignals = {}

    def __init__(self, app):
        self.signalMarkers = [(i, j) for i in 'oD<.' for j in 'bgrcmyk']
        np.random.shuffle(self.signalMarkers)
        self.app = app

    def BindEvents(self):
        self.app.OnLoadSignal = self.LoadSignal
        self.app.OnApplyFilter = self.ApplyFilter
        self.app.BindAndLoad()
        self.app.Show()
        self.app.focus_set()

    def PlotOnAxis(self, signalData=[], axis_dim=0, signalMarker='ob', signalName='label', x_label="", y_label=""):
        yvals = []
        xvals = []
        for i in signalData:
            xvals.append(i[0])
            yvals.append(i[1])

        axis = self.app.GetAxis(axis_dim)
        axis.scatter(
            xvals, yvals, marker=signalMarker[0], color=signalMarker[1], label=signalName)
        axis.legend(loc="upper left", borderaxespad=0,
                    fancybox=True, framealpha=0.5)
        self.app.repaint_axis()

    def LoadSignal(self):
        fname = tk.filedialog.askopenfilename(
            filetypes=[("Signal files", "*.sgn;*.ds")])
        if fname:
            self.SignalPath = fname
            self.Mode = 'DS'
            signalData = DS_Signal.LoadSignal(signalpath=self.SignalPath)
            self.LoadedSignal = signalData
            if signalData.signalType == 1:
                # Fourier Signal
                self.fourier_output = signalData.fourier_values
                return
            signalLabel = self.SignalPath.split('/')[-1].split('.')[0]

            myMarkerIndex = np.random.randint(0, len(self.signalMarkers))
            self.PlotOnAxis(signalData.GetData(), axis_dim=0, signalName=signalLabel,
                            signalMarker=self.signalMarkers[myMarkerIndex])
        pass
    def ApplyFilter(self):
        selected_filter = self.app.GetSelectedFilter()
        sampling_frequency= float(self.app.fs_entry.get())
        stop_attenuation= float(self.app.sta_entry.get())
        transition_band= float(self.app.tband_entry.get())
        cutoff_frequency= float(self.app.cutoff_entry.get())

        band1 = float(self.app.band1_entry.get())
        band2 = float(self.app.band2_entry.get())

        fir = None
        fil = None
        if selected_filter == 'Low':
            fir = fls.FIR_FILTERS.Low
            fil = fls.apply_filter(self.LoadedSignal.GetData(), sampling_frequency= sampling_frequency, stop_attenuation= float(self.app.sta_entry.get()),
            transition_band= float(self.app.tband_entry.get()), cutoff_frequency= float(self.app.cutoff_entry.get()),filter_type= fir )
        elif selected_filter =='High':
            fir = fls.FIR_FILTERS.High
            fil = fls.apply_filter(self.LoadedSignal.GetData(), sampling_frequency= float(self.app.fs_entry.get()), stop_attenuation= float(self.app.sta_entry.get()),
            transition_band= float(self.app.tband_entry.get()), cutoff_frequency= float(self.app.cutoff_entry.get()),filter_type= fir )
        elif selected_filter == 'Bandpass':
            fir = fls.FIR_FILTERS.BandPass
            fil = fls.apply_band_filter(self.LoadedSignal.GetData(), sampling_frequency= float(self.app.fs_entry.get()), stop_attenuation= float(self.app.sta_entry.get()),
            transition_band= float(self.app.tband_entry.get()), band1= band1, band2 = band2,filter_type= fir )
        elif selected_filter == 'Bandreject':
            fir = fls.FIR_FILTERS.BandReject
            fil = fls.apply_band_filter(self.LoadedSignal.GetData(), sampling_frequency= float(self.app.fs_entry.get()), stop_attenuation= float(self.app.sta_entry.get()),
            transition_band= float(self.app.tband_entry.get()), band1= band1, band2 = band2,filter_type= fir )

        yvals = [x[1] for x in self.LoadedSignal.GetData()]
        filter_yvals = [x[1] for x in fil]
        res = my_dsp_package.convolve(yvals, filter_yvals, mode= 'full')
        xvals = [x[0] for x in self.LoadedSignal.GetData()]
        resx = []
        for i in range(len(xvals)):
            resx.append((xvals[i], res[i]))

        self.PlotOnAxis(resx, axis_dim= 1)