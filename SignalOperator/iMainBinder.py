import cmath
import sys
import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

from DSP import fft, signal_op
from GUIHelper._GUI import GUI
from SignalGenerator.iDSignalGenerator import DSignalGenerator
from SignalGenerator.iDSignalGeneratorBinder import DSignalGeneratorEvents
from SignalOperations._signal import DS_Signal, Signal
from SignalOperations._signalParser import SignalParser


class MainInterfaceBinder:

    LoadedSignals = {}
    SignalPath = None
    app = None
    OperationsHistory = []
    signalMarkers = []
    selectedChannels = []
    plottedSignals = []
    fourier_output = None

    def __init__(self, app):
        self.app = app
        self.signalMarkers = [(i, j) for i in 'oD<.' for j in 'bgrcmyk']
        np.random.shuffle(self.signalMarkers)

    def BindEvents(self):
        self.app.OnLoadSignalButtonClicked = self.LoadSignal
        self.app.OnSaveSignalButtonClicked = self.SaveSignal
        self.app.OnGeneratorOpenCommand = self.OpenGenerator
        self.app.OnExit = self.OnExit
        self.app.OnAddSignalsButtonClicked = self.AddSignals
        self.app.OnSubtractSignalsButtonClicked = self.SubtractSignals
        self.app.OnMultiplySignalsButtonClicked = self.MultiplySignals
        self.app.OnQuantizeButtonClicked = self.QuantizeSignal
        self.app.OnClearSignals = self.OnClearSignals
        self.app.OnApplyFFTCommand = lambda: self.ApplyFourier(False)
        self.app.OnApplyFFTInverseCommand = lambda: self.ApplyFourier(True)
        self.app.OnCombineSignals = self.OnCombineSignals
        self.app.OnAccumulateSignals = self.OnAccumulateSignals
        self.app.OnShiftSignal = self.OnShiftSignal
        self.app.OnFoldSignal = self.OnFoldSignal
        self.app.RenderGui()

    def OnExit(self):
        self.app.destroy()
        sys.exit()

    def OpenGenerator(self):
        self.signalGen = DSignalGenerator(self.app.master)
        signalGenBinder = DSignalGeneratorEvents(self.signalGen)
        signalGenBinder.BindEvents()

    def OnClearSignals(self):
        self.LoadedSignals = {}
        self.SignalPath = ""
        self.app.DrawPlotters()

    def LoadSignal(self):
        fname = tk.filedialog.askopenfilename(
            filetypes=[("Signal files", "*.sgn;*.ds")])
        if fname:
            if fname in self.LoadedSignals:
                return
            self.SignalPath = fname

            signalFileType = fname.split('.')[1]
            if signalFileType == 'sgn':
                self.Mode = 'SGN'
                signalData = Signal.LoadSignal(signalpath=self.SignalPath)
                self.UpdateSignalUiData(signalData)
                self.LoadedSignals[self.SignalPath] = signalData
                signalLabel = signalData.signalName
                self.AddChannelsToList(signalData)
            else:
                self.Mode = 'DS'
                signalData = DS_Signal.LoadSignal(signalpath=self.SignalPath)
                self.LoadedSignals[self.SignalPath] = signalData
                signalLabel = self.SignalPath.split('/')[-1].split('.')[0]

                myMarkerIndex = np.random.randint(0, len(self.signalMarkers))
                self.PlotOnAxis(signalData.GetData(), axis_dim=(0, 0), signalName=signalLabel,
                                signalMarker=self.signalMarkers[myMarkerIndex], _global = True)
        else:
            print("Error")

    def PlotSignal(self, signalData=[], plotterName="defaultPlotter", signalMarker='ob', signalName='label'):
        yvals = []
        xvals = []
        for i in signalData:
            xvals.append(i[0])
            yvals.append(i[1])

        self.app.GetPlotter(plotterName)[0].scatter(
            xvals, yvals, marker=signalMarker[0], color=signalMarker[1], label=signalName)
        self.app.GetPlotter(plotterName)[0].legend(
            bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
        self.app.GetPlotter(plotterName)[1].draw()

    def PlotOnAxis(self, signalData=[], axis_dim=(1, 0), signalMarker='ob', signalName='label', _global = True):
        yvals = []
        xvals = []
        for i in signalData:
            xvals.append(i[0])
            yvals.append(i[1])

        if _global:
            for i in self.app.GetPlottingPages():
                #i is a page
                self.app.GetAxis(axis_dim[0], axis_dim[1], page = i[0]).scatter(
                    xvals, yvals, marker=signalMarker[0], color=signalMarker[1], label=signalName)
                self.app.GetAxis(axis_dim[0], axis_dim[1], page = i[0]).legend(
                    loc="upper left", borderaxespad=0, fancybox=True, framealpha=0.5)
                self.app.repaint_axis()
            return
            

        self.app.GetAxis(axis_dim[0], axis_dim[1]).scatter(
            xvals, yvals, marker=signalMarker[0], color=signalMarker[1], label=signalName)
        self.app.GetAxis(axis_dim[0], axis_dim[1]).legend(
            loc="upper left", borderaxespad=0, fancybox=True, framealpha=0.5)
        self.app.repaint_axis()

    def SaveSignal(self):
        self.AddSignals()

    def UpdateSignalUiData(self, signalData):
        self.app.GetSignalNameLabel().configure(
            text="Signal Name: " + signalData.signalName)
        self.app.GetSignalChannelsNoLabel().configure(
            text="Channels No: " + str(signalData.channelsCount))
        self.app.GetSignalPathLabel().configure(text="Path: " + signalData.signalPath)

    def UpdateStatusText(self, text, fgColor='black'):
        self.app.GetStatusText().configure(text=text, fg=fgColor)

    def AddChannelsToList(self, signal):
        lbox = self.app.GetChannelsListBox()
        for i in range(signal.channelsCount):
            lbox.insert(tk.END, "C"+str(i+1))

    def AddItemToSignalList(self, signal):
        lbox = self.app.GetChannelsListBox()
        lbox.insert(tk.END, signal)

    def AddSignals(self):
        signals = self.__get_loaded_signals()
        final_result = signal_op.accumulate_signlas(signals)

        selected_dim = self.app.GetStdOperationsAxis()
        self.app.ChangeAxisTitle(selected_dim[0], selected_dim[1], "AX-{0} - Signals Addition".format(selected_dim))
        self.PlotOnAxis(final_result, axis_dim=selected_dim,
                        signalMarker='Dr', signalName="Sum Result")

    def SubtractSignals(self):
        signals = self.__get_loaded_signals()
        final_result = signal_op.accumulate_signlas(signals, sign=-1)

        selected_dim = self.app.GetStdOperationsAxis()
        self.app.ChangeAxisTitle(selected_dim[0], selected_dim[1], "AX-{0} - Signals Subtraction".format(selected_dim))

        self.PlotOnAxis(final_result, axis_dim=selected_dim,
                        signalMarker='or', signalName="Subtraction Result")

    def MultiplySignals(self):
        signals = self.__get_loaded_signals()
        cnst = self.app.constantMultiplier.get()

        combined_signal = signal_op.combine(signals)

        final_result = signal_op.multiply_signal(combined_signal, cnst)

        selected_dim = self.app.GetStdOperationsAxis()
        self.app.ChangeAxisTitle(selected_dim[0], selected_dim[1], "AX-{0} - Combined Signals Multiplication".format(selected_dim))

        self.PlotOnAxis(final_result, axis_dim=selected_dim,
                        signalMarker='.b', signalName="Multiply Result")

    def QuantizeSignal(self):
        signal = self.__get_loaded_signals()

        quantizationLevels = self.app.GetQuantizationLevel()

        quantized_signal, signal_encoding, mse = signal_op.quantize_signal(
            signal[0], n=quantizationLevels, use_bit_mode=bool(self.app.GetBoolUseBitMode()))

        print("Error ", mse)
        print("Encoding ", signal_encoding)

        selected_dim = self.app.GetQuantizeOperationsAxis()
        self.app.ChangeAxisTitle(selected_dim[0], selected_dim[1], "AX-{0} - First Signal Quantization".format(selected_dim))

        self.PlotOnAxis(quantized_signal, axis_dim=selected_dim,
                        signalName='Quantized Signal', signalMarker='or')

    def ApplyFourier(self, bool_is_inverse):
        if len(self.LoadedSignals) > 1:
            return
        signal_values = [x[1]
                         for x in self.LoadedSignals[self.SignalPath].GetData()]
        signal_time = [x[0]
                       for x in self.LoadedSignals[self.SignalPath].GetData()]
        fourier_input = signal_values if not bool_is_inverse else self.fourier_output
        self.fourier_output = self.apply_fourier(
            fourier_input, bool_is_inverse)

        if bool_is_inverse:
            cmpx = [round(x.real) for x in self.fourier_output]
            print('My Inverse Output = ', cmpx)
            return
        converted = [cmath.polar(x) for x in self.fourier_output]

        print('My Fourier Output ', converted)
        with open('_data/outputSignal.ds', 'w') as writer:
            writer.writelines('1\n')
            writer.writelines('0\n')
            writer.writelines(str(len(converted))+'\n')
            for i in range(len(converted)):
                writer.writelines('{0} {1} {2}'.format(
                    i, converted[i][0], converted[i][1])+'\n')
        self.app.DrawPlotters()
        self.PlotAmblitude()
        self.PlotPhaseShift()
        self.app.ChangePlotterTitle('defaultPlotter', 'Amblitude')

    def apply_fourier(self, values, is_inverse):
        fourier_iterations = len(values)
        # x(n) * e^(-jk2PIn/N)
        final_fourier = []
        J = complex(0, 1) if not is_inverse else complex(0, -1)
        for k in range(fourier_iterations):
            x_Value = 0
            for n in range(fourier_iterations):
                x_n = values[n]
                x_Value += x_n * \
                    cmath.exp(J * k * 2 * np.pi * n/fourier_iterations)

            final_fourier.append(
                complex(round(x_Value.real), round(x_Value.imag)))

        if is_inverse:
            final_fourier = [x / fourier_iterations for x in final_fourier]

        return final_fourier

    def PlotAmblitude(self, sampled_frequency=4):
        amblitudes = []
        n = len(self.fourier_output)
        amblitudes = [cmath.sqrt(s.real**2 + s.imag**2)
                      for s in self.fourier_output]
        xValues = []
        # 2*PI / N * (1/Fs) -? X0
        x_0 = 2 * np.pi / (n * (1/sampled_frequency))
        print('my xvalue = ', x_0)
        xValues = [(x*x_0) for x in list(range(2, n+1))]
        xValues.insert(0, x_0)
        print(xValues)
        self.app.DrawResultPlotter(
            xlabel='Frequency', ylabel='Amblitude', _title='Amblitude vs Frequency')
        self.app.GetPlotter('resultPlotter')[0].scatter(
            xValues, amblitudes, marker='o', color='r', label='amb')
        self.app.GetPlotter('resultPlotter')[1].draw()

    def PlotPhaseShift(self, sampled_frequency=4):
        phase_shifts = []
        n = len(self.fourier_output)
        phase_shifts = [np.degrees(cmath.atan(x.imag / x.real).real)
                        for x in self.fourier_output]
        xValues = []
        # 2*PI / N * (1/Fs) -? X0
        x_0 = 2 * np.pi / (n * (1/sampled_frequency))
        xValues = [(x * x_0) for x in list(range(2, n+1))]
        xValues.insert(0, x_0)
        self.app.DrawDefaultPlotter(
            xlabel='Frequency', ylabel='PhaseShift', _title='Phase shift vs Frequency')
        self.app.GetPlotter('defaultPlotter')[0].scatter(
            xValues, phase_shifts, marker='o', color='r', label='x')
        self.app.GetPlotter('defaultPlotter')[1].draw()

    def ApplyFastFourier(self, bool_is_inverse):
        self.fourier_output = fft.apply_fft(
            signal=self.LoadedSignals[self.SignalPath].GetData())
        print(self.fourier_output)

    def OnShiftSignal(self):
        shift_val = self.app.GetShiftValue()
        signal = self.LoadedSignals[self.SignalPath].GetData()
        is_folded = self.app.GetIfShiftingFoldedSignal()
        shifted = signal_op.shift_signal(
            signal, shift_val, is_folded=is_folded)

        selected_dim = self.app.GetManipulationOperationsAxis()
        self.PlotOnAxis(shifted, axis_dim= selected_dim, signalName= 'Shifted Signal')

    def OnFoldSignal(self):
        signal = self.LoadedSignals[self.SignalPath].GetData()
        folded = signal_op.fold_signal(signal)
        
        selected_dim = self.app.GetManipulationOperationsAxis()
        
        self.PlotOnAxis(folded, axis_dim= selected_dim, signalName= 'Fodled Signal')

    def OnCombineSignals(self):
        raise "Not Implemented Yet"

    def OnAccumulateSignals(self):
        raise "Not implemented yet"

    def __get_loaded_signals(self):
        signals = []
        if self.Mode == 'DS':
            for i in self.LoadedSignals:
                signals.append(self.LoadedSignals[i].GetData())
        return signals
