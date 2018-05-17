import numpy as np


def P2R(amb, phs):
    return complex(round(amb * np.cos(phs)), round(amb * np.sin(phs)))


def ReadDSFileFormat(signalPath="_data/_signals/FDS/Signal5.ds"):
    signalType = 0
    isPeriodic = False
    signalData = []
    signalFrequency = []
    signal_fourier_input = []
    with open(signalPath, 'r') as file:
        fileData = file.readlines()
        signalType = int(fileData[0])
        isPeriodic = bool(int(fileData[1]))
        noOfEntries = int(fileData[2])
        if signalType == 0:  # Normal Signal
            for i in range(noOfEntries):
                point = fileData[i+3].split(' ')
                signalData.append(
                    (float(point[0].strip()), float(point[1].strip())))
        elif signalType == 1:
            for i in range(noOfEntries):
                # Read Pairs of Polar and convert into complex for further Fourier Input
                sample = fileData[i+3].split(' ')
                amb = float(sample[0])
                phase_shift = float(sample[1])
                complex_form = P2R(amb, phase_shift)
                signal_fourier_input.append(complex_form)
        elif signalType == 2:
            secondEntryNo = int(fileData[noOfEntries])
            for i in range(secondEntryNo):
                point = fileData[i+1+noOfEntries].split(' ')
                signalFrequency.append(
                    (float(point[0].strip()), float(point[1].strip())))

    return (signalType, isPeriodic, signalData, signalFrequency, signal_fourier_input)


def GenerateSignal(samples_count, amblitude, frequency, sampling_frequency,signal_phase_shift,  stype='sin'):
    """Generates a Sin / Cos signal in a range with given attributes"""
    phase_shift = signal_phase_shift
    if stype == 'cos':  # We will use sin as  a base, shifted by 90 if cos is required
        phase_shift += 90
    final_signal = []
    for i in range(samples_count):
        sValue = amblitude * \
            np.sin(2 * np.pi * frequency/sampling_frequency * i + phase_shift)
        final_signal.append((i, sValue))
    return final_signal


class DS_Signal:
    signalType = 0
    isPeriodic = False
    signalData = []
    signalFrequency = []

    def __init__(self, stype, isPeriodic, sData, sFrequency, sFourierInput):
        self.signalData = sData
        self.isPeriodic = isPeriodic
        self.signalFrequency = sFrequency
        self.signalType = stype
        self.fourier_values = sFourierInput

    @staticmethod
    def LoadSignal(signalpath='_data/_signals/test_new_signal.sgn'):
        signalData = ReadDSFileFormat(signalpath)
        return DS_Signal(stype=signalData[0],
                         isPeriodic=signalData[1],
                         sData=signalData[2],
                         sFrequency=signalData[3], sFourierInput=signalData[4])

    def GetData(self):
        return self.signalData

    def GetFrequency(self):
        return self.signalFrequency

    def GetSignalType(self):
        return self.signalType
