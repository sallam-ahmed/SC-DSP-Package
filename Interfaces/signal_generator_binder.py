import numpy as np
from DSP.digital_signal import ReadDSFileFormat, GenerateSignal
import tkinter as tk


class SignalGeneratorWindowBinder:

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

        self.finalSignal = GenerateSignal(
            nSamples, signalAmblitude, signalFrequency, signalFs, phaseShift, stype=str(signalType).lower())

        
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
