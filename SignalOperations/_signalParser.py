class SignalParser:        
        @staticmethod
        def GenerateSignalFile(signalPath = "_data/_signals/", name = "test_signal",
                            channels = [[]],markers = ["ro","<b"]):
                with open(signalPath ,'w') as file:
                        signalName = "name:" + name+ "#\n"
                        file.writelines(signalName)
                        channelsNo = "channel_no:"+str(len(channels)) + "#\n"
                        file.writelines(channelsNo)
                        file.writelines("channels:"+ "\n")
                        for i in range(len(channels)):
                                file.writelines("{")
                                vals = [(x) for x in channels[i]]
                                print(vals)
                                c = 0
                                for j in vals:
                                        c+=1
                                        if type(j) != type((1,2)):
                                               valText = "(_," + str(j) + ")"
                                        else:
                                                if str(j[0]) == '_':
                                                        valText = "(_,"+ str(j[1])+ ")"                                                
                                                else:
                                                        valText = "("+ str(j[0]) + ',' + str(j[1])+ ")"
                                        if c != len(vals):
                                              valText += "-"  
                                        file.writelines(valText)
                                        valText = ""
                                closure = "}"
                                if i != len(channels)-1:
                                        closure+="|"
                                closure += "\n"
                                file.writelines(closure)
                        file.writelines("#"+ "\n")
                        markersSection = "markers:["
                        for i in markers:
                                stringMarker = str(i[0]) + str(i[1])
                                print("String Marker for ", i , " is " , stringMarker)
                                markersSection+= stringMarker
#                                print("Markers ", i , markersSection)
                                if i != markers[-1]:
                                        markersSection+= ","
                        markersSection+="]#"
                        file.writelines(markersSection)
        @staticmethod
        def ReadSignalFile(signalpath = "_data/_signals/test_new_signal.sgn"):
                markers = []
                channels = []
                signalName = ""
                channelsNo = 0
                with open(signalpath,'r') as file:
                        fileData = file.read().replace(" ", "").replace("\n","")
                        print("Before split: " , fileData)
                        fileData = fileData.split('#')
                        print(fileData)
                        signalName = fileData[0].split(':')[1].strip()
                        channelsNo = int(fileData[1].split(':')[1].strip())
                        stringChannels = fileData[2].split(':')[1].strip().split('|')
#                        print(stringChannels)
                        for c in stringChannels:
                                channels.append(list())
                                latestChannel = channels[-1]
                                c = c[1:]
                                c = c[:-1]
#                                print(c)
                                tupleValues = [x for x in c.split('-')]
#                                print('vals  =' , tupleValues)
                                for val in tupleValues:
#                                        print("HERE")
                                        realValue = val[1:]
                                        realValue = realValue[:-1]
                                        realValue = realValue.split(',')
                                        if str(realValue[0]) == '_':
                                                realValue = (int(realValue[1]))
                                        else:
                                                realValue = (int(realValue[0]),int(realValue[1]))
                                        latestChannel.append(realValue)
#                                        print(realValue)
#                        print("Final Channels " , channels)
                        
                       

                        stringMarkers = fileData[3].split(':')[1].strip()
                        stringMarkers = stringMarkers[1:]
                        stringMarkers = stringMarkers[:-1]
                        stringMarkers = stringMarkers.split(',')
                        print("STRING MARKERS: " , stringMarkers)
                        for m in stringMarkers:
                                markers.append(str(m))
#                        print('Final Markers : ', markers)
                        
                return signalName,signalpath, channelsNo,channels,markers
                
        @staticmethod
        def ReadDSFileFormat(signalPath= "_data/_signals/FDS/Signal5.ds"):
                signalType = 0
                isPeriodic= False
                signalData = []
                signalFrequency = []
                with open(signalPath,'r') as file:
                        fileData = file.readlines()
                        signalType = int(fileData[0])
                        isPeriodic = bool(int(fileData[1]))
                        noOfEntries = int(fileData[2])
                        for i in range(noOfEntries):
                                point = fileData[i+3].split(' ')
                                signalData.append( (float(point[0].strip()), float(point[1].strip())) )
#                        print("Signal Data \n " , signalData)
#                        return
                        if signalType == 2:
                                secondEntryNo = int(fileData[noOfEntries])
                                for i in range(secondEntryNo):
                                        point = fileData[i+1+noOfEntries].split(' ')
                                        signalFrequency.append( (float(point[0].strip()), float(point[1].strip())) )
                
                return (signalType, isPeriodic, signalData, signalFrequency)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                