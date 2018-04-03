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
        self.app.OnCombineSignals = self.OnCombineSignals
        self.app.OnAccumulateSignals = self.OnAccumulateSignals
        self.app.OnShiftSignal = self.OnShiftSignal
        self.app.OnFoldSignal = self.OnFoldSignal

        self.app.OnApplyStandardFourierTransformCommand = lambda: self.ApplyFourier(
            False)
        self.app.OnApplyStandardInverseFourierTransformCommand = lambda: self.ApplyFourier(
            True)

        self.app.OnApplyFastFourierTransformCommand = lambda: self.ApplyFastFourier(
            False)
        self.app.OnApplyInverseFastFourierTransformCommand = lambda: self.ApplyFastFourier(
            True)

        self.app.OnConvluteSignal = self.OnConvluteSignal
        self.app.OnCorrelateSignal = lambda: self.OnCorrelateSignal(is_normalized = False)
        self.app.OnNormalizedCorrelation = lambda: self.OnCorrelateSignal(is_normalized = True)

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
                if signalData.signalType == 1:
                    # Fourier Signal
                    self.fourier_output = signalData.fourier_values
                    return
                signalLabel = self.SignalPath.split('/')[-1].split('.')[0]

                myMarkerIndex = np.random.randint(0, len(self.signalMarkers))
                self.PlotOnAxis(signalData.GetData(), axis_dim=(0, 0), signalName=signalLabel,
                                signalMarker=self.signalMarkers[myMarkerIndex], _global=True)
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

    def PlotOnAxis(self, signalData=[], axis_dim=(1, 0), signalMarker='ob', signalName='label', x_label="", y_label="", axis_title="", _global=False):
        yvals = []
        xvals = []
        for i in signalData:
            xvals.append(i[0])
            yvals.append(i[1])

        if _global:
            for i in self.app.GetPlottingPages():
                # i is a page
                self.app.GetAxis(axis_dim[0], axis_dim[1], page=i[0]).scatter(
                    xvals, yvals, marker=signalMarker[0], color=signalMarker[1], label=signalName)
                self.app.GetAxis(axis_dim[0], axis_dim[1], page=i[0]).legend(
                    loc="upper left", borderaxespad=0, fancybox=True, framealpha=0.5)
                self.app.repaint_axis()
            return

        axis = self.app.GetAxis(axis_dim[0], axis_dim[1])
        axis.scatter(
            xvals, yvals, marker=signalMarker[0], color=signalMarker[1], label=signalName)
        axis.legend(loc="upper left", borderaxespad=0,
                    fancybox=True, framealpha=0.5)
        if axis_title is not None:
              # Invokes Repaint Internally
            self.app.ChangeAxisTitle(axis_dim[0], axis_dim[1], axis_title)
        else:
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
        signals = self.__get_loaded_signals_data()
        final_result = signal_op.accumulate_signlas(signals)

        selected_dim = self.app.GetStdOperationsAxis()
        self.PlotOnAxis(final_result, axis_dim=selected_dim, signalMarker='Dr',
                        signalName="Sum Result", axis_title="AX-{0} - Signals Addition".format(selected_dim))

    def SubtractSignals(self):
        signals = self.__get_loaded_signals_data()
        final_result = signal_op.accumulate_signlas(signals, sign=-1)

        selected_dim = self.app.GetStdOperationsAxis()

        self.PlotOnAxis(final_result, axis_dim=selected_dim,
                        signalMarker='or', signalName="Subtraction Result", axis_title="AX-{0} - Signals Subtraction".format(selected_dim))

    def MultiplySignals(self):
        signals = self.__get_loaded_signals_data()
        cnst = self.app.constantMultiplier.get()

        combined_signal = signal_op.combine(signals)

        final_result = signal_op.multiply_signal(combined_signal, cnst)

        selected_dim = self.app.GetStdOperationsAxis()

        self.PlotOnAxis(final_result, axis_dim=selected_dim,
                        signalMarker='.b', signalName="Multiply Result", axis_title="AX-{0} - Combined Signals Multiplication".format(selected_dim))

    def QuantizeSignal(self):
        signal = self.__get_loaded_signals_data()

        quantizationLevels = self.app.GetQuantizationLevel()

        quantized_signal, signal_encoding, mse = signal_op.quantize_signal(
            signal[0], n=quantizationLevels, use_bit_mode=bool(self.app.GetBoolUseBitMode()))

        print("Error ", mse)
        print("Encoding ", signal_encoding)

        selected_dim = self.app.GetQuantizeOperationsAxis()

        self.PlotOnAxis(quantized_signal, axis_dim=selected_dim,
                        signalName='Quantized Signal', signalMarker='or', axis_title="AX-{0} - First Signal Quantization".format(selected_dim))

    def ApplyFourier(self, bool_is_inverse):
        if bool_is_inverse:
            signal_values = fft.apply_idft(self.fourier_output)
            print(signal_values)
            return
        self.fourier_output = fft.apply_dft(
            self.LoadedSignals[self.SignalPath].GetData())
        fs = self.app.GetFourierSamplingFreq()
        self.PlotAmblitude(sampled_frequency=fs)
        self.PlotPhaseShift(sampled_frequency=fs)
        # self.app.ChangePlotterTitle('defaultPlotter', 'Amblitude')

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

    def PlotAmblitude(self, sampled_frequency=4, title="AX-{0} - Amblitude vs Time"):
        xValue, amblitudes = fft.get_amblitudes(
            self.fourier_output, sampled_frequency)
        signal = []
        for i in range(len(xValue)):
            signal.append((xValue[i], amblitudes[i]))
        working_axis = self.app.GetFourierAmblitudeAxis()
        self.PlotOnAxis(signal, working_axis, signalName='Amblitude',
                        axis_title=title.format(working_axis))

    def PlotPhaseShift(self, sampled_frequency=4, title="AX-{0} - Phase shift vs Time"):
        xValue, phase_shifts = fft.get_phase_shift(
            self.fourier_output, sampled_frequency)
        signal = []
        for i in range(len(xValue)):
            signal.append((xValue[i], phase_shifts[i]))
        working_axis = self.app.GetFourierPhaseShiftAxis()
        self.PlotOnAxis(signal, working_axis, signalName='Phase vs Time',
                        axis_title=title.format(working_axis))

    def ApplyFastFourier(self, bool_is_inverse):
        if bool_is_inverse:
            signal_values = fft.apply_fft(
                self.fourier_output, bool_is_inverse=bool_is_inverse)
            print(signal_values)
            return

        self.fourier_output = fft.apply_fft(
            signal=self.LoadedSignals[self.SignalPath].GetData(), bool_is_inverse=bool_is_inverse)
        fs = self.app.GetFourierSamplingFreq()
        self.PlotAmblitude(sampled_frequency=fs,
                           title="AX-{0} - Amblitude vs Time - FFT")
        self.PlotPhaseShift(sampled_frequency=fs,
                            title="AX-{0} - Phase shift vs Time - FFT")

    def OnShiftSignal(self):
        shift_val = self.app.GetShiftValue()
        signal = self.LoadedSignals[self.SignalPath].GetData()
        is_folded = self.app.GetIfShiftingFoldedSignal()
        shifted = signal_op.shift_signal(
            signal, shift_val, is_folded=is_folded)

        selected_dim = self.app.GetManipulationOperationsAxis()
        self.PlotOnAxis(shifted, axis_dim=selected_dim,
                        signalName='Shifted Signal')

    def OnFoldSignal(self):
        signal = self.LoadedSignals[self.SignalPath].GetData()
        folded = signal_op.fold_signal(signal)

        selected_dim = self.app.GetManipulationOperationsAxis()

        self.PlotOnAxis(folded, axis_dim=selected_dim,
                        signalName='Fodled Signal')

    def OnCombineSignals(self):
        raise "Not Implemented Yet"

    def OnAccumulateSignals(self):
        raise "Not implemented yet"

    def OnConvluteSignal(self):
        loaded_signals = self.__get_loaded_signals()
        first = loaded_signals[0]
        second = loaded_signals[1]
        print('Using first two signals only')
        result_signal = signal_op.convolve_signal(
            first.GetData(), second.GetData())

        w_axis = self.app.GetConvlutionWorkingAxis()

        self.PlotOnAxis(result_signal, axis_dim=w_axis, signalMarker='ob',
                        signalName='Convolution Result', axis_title="AX-{0} - Signals Convolution".format(w_axis))

    def OnCorrelateSignal(self, is_normalized):
        loaded_signals = self.__get_loaded_signals()
        first = loaded_signals[0]
        second = []
        periodic = True
        if len(loaded_signals) == 1: # Auto Correlation
            second = loaded_signals[0]
        else:
            second = loaded_signals[1]
            periodic = first.isPeriodic

        print('Using first two signals only')
        correlation_func = signal_op.corelate_signal if not is_normalized else signal_op.norm_correlate_signal
        result_signal = correlation_func(
            first.GetData(), second.GetData(), is_periodic=periodic)

        w_axis = self.app.GetConvlutionWorkingAxis()

        self.PlotOnAxis(result_signal, axis_dim=w_axis, signalMarker='ob',
                        signalName='Convolution Result', axis_title="AX-{0} - Signals{1}Correlation".format(w_axis, '' if not is_normalized else 'Normalized'))

    def __get_loaded_signals_data(self):
        signals = []
        if self.Mode == 'DS':
            for i in self.LoadedSignals:
                signals.append(self.LoadedSignals[i].GetData())
        return signals

    def __get_loaded_signals(self):
        signals = []
        if self.Mode == 'DS':
            for i in self.LoadedSignals:
                signals.append(self.LoadedSignals[i])
        return signals