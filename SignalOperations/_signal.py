from SignalOperations._signalParser import SignalParser
class Signal:
        signalChannels = []
        channelsCount = None
        signalMarkers = []
        signalPath = None
        signalName = None
        
#        def __init__(self,signalData = None):
#                self.signalData = signalData
        def __init__(self,signalName,signalpath, channelsNo,channels,markers):
                self.signalChannels = channels
                self.signalName = signalName
                self.signalMarkers = markers
                self.channelsCount = channelsNo
                self.signalPath = signalpath
                

        @staticmethod
        def LoadSignal(signalpath = '_data/_signals/test_new_signal.sgn'):
                signalData = SignalParser.ReadSignalFile(signalpath)
#                print(signalData)
                return Signal(signalName= signalData[0],
                               signalpath= signalData[1],
                               channelsNo= signalData[2],
                               channels= signalData[3],
                               markers= signalData[4])                       
        
        def GetChannelsList(self):
                return [x for x in range(1,len(self.channelsCount))]

        def GetData(self,channelNumber = 1):
                assert channelNumber <= self.channelsCount-1
                return self.signalChannels[channelNumber]
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
        def LoadSignal(signalpath = '_data/_signals/test_new_signal.sgn'):
                signalData = SignalParser.ReadDSFileFormat(signalpath)
                return DS_Signal(stype = signalData[0],
                                 isPeriodic= signalData[1],
                                sData = signalData[2],
                                sFrequency = signalData[3], sFourierInput = signalData[4])
        def GetData(self):
                return self.signalData
        def GetFrequency(self):
                return self.signalFrequency
        def GetSignalType(self):
                return self.signalType
                