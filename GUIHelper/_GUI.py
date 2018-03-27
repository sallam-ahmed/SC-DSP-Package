import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class GUI:
        @staticmethod
        def InitRootApp(rootApp, master = None, title = "Title", resizable = (True,True)):
                #print(rootApp)
                tk.Tk.__init__(rootApp,master)
                rootApp.grid()
                rootApp.title(title)
                rootApp.focus_set()
                rootApp.grid()
                rootApp.resizable(False,False)
                plt.ioff()
        @staticmethod
        def CreateSubWindow(rootApp,masterWindow,title = "Title"):                
                rootApp = tk.Toplevel(masterWindow)
                rootApp.title(title)
                return rootApp

        @staticmethod
        def DrawButton(rootApp,name = "Button1", text = "test",position = (0,0),
                         onClickCommand = None,padX = 0, padY = 0,
                         sticky = (tk.W,tk.E), columnSpan = 1, rowSpan = 1,
                         owner = None):
                if owner == None:
                        owner = rootApp

                newControl = tk.Button(owner,text = text, command = onClickCommand)
                newControl.grid(row = position[0],column = position[1],
                                padx = padX,pady = padY,
                                columnspan = columnSpan, rowspan = rowSpan
                                ,sticky= sticky)
                
                rootApp.controls[name] = newControl
        @staticmethod
        def DrawLabel(rootApp,name = "Label1", text = "test",position = (10,10),
                         padX = 0, padY = 0,
                         sticky = (tk.W,tk.E), columnSpan = 1, rowSpan = 1,
                         owner = None):
                if owner == None:
                        owner = rootApp
                newControl = tk.Label(owner,text = text)
                newControl.grid(row = position[0],column = position[1],
                                padx = padX,pady = padY,
                                columnspan = columnSpan, rowspan = rowSpan,
                                sticky= sticky)
                
                rootApp.controls[name] = newControl
        @staticmethod
        def DrawEntry(rootApp,variable,name = "Entry1",position = (10,10),
                         padX = 0, padY = 0,
                         sticky = (tk.W,tk.E), columnSpan = 1, rowSpan = 1,
                         owner = None):
                if owner == None:
                        owner = rootApp
                        
                newControl = tk.Entry(owner,textvariable = variable)
                newControl.grid(row = position[0],column = position[1],
                                padx = padX,pady = padY,
                                columnspan = columnSpan, rowspan = rowSpan,
                                sticky= sticky)
                rootApp.controls[name] = newControl

        @staticmethod
        def DrawCheckBox(rootApp,variable,text = 'text', name = "ch1",position = (10,10),
                         padX = 0, padY = 0,
                         sticky = (tk.W,tk.E), columnSpan = 1, rowSpan = 1,
                         owner = None):
                if owner == None:
                        owner = rootApp
                        
                newControl = tk.Checkbutton(owner,text = text, variable = variable)
                newControl.grid(row = position[0],column = position[1],
                                padx = padX,pady = padY,
                                columnspan = columnSpan, rowspan = rowSpan,
                                sticky= sticky)
                rootApp.controls[name] = newControl

        @staticmethod
        def DrawGroupBox(rootApp,name = "GroupBox1", text = "GroupBox1",
                           position = (10,10),
                           padX = 0, padY = 0,
                           sticky = (tk.W,tk.E), columnSpan = 1, rowSpan = 1,
                           owner = None):
                if owner == None:
                        owner = rootApp
                newControl = tk.LabelFrame(owner,text = text)
                newControl.grid(row = position[0],column = position[1],
                                padx = padX,pady = padY,
                                columnspan = columnSpan, rowspan = rowSpan,
                                sticky= sticky)
                rootApp.controls[name] = newControl
        @staticmethod        
        def DrawOptions(rootApp,
                           variable,
                           *options,
                           name = "Options1",
                           position = (10,10),
                           padX = 0, padY = 0,
                           sticky = (tk.W,tk.E), columnSpan = 1, rowSpan = 1,
                           owner = None):
                if owner == None:
                        owner = rootApp
                
                
                newControl = tk.OptionMenu(owner,variable,*options)
                
                newControl.grid(row = position[0],column = position[1],
                                padx = padX,pady = padY,
                                columnspan = columnSpan, rowspan = rowSpan,
                                sticky= sticky)
                rootApp.controls[name] = newControl
        @staticmethod        
        def DrawImagePlot(rootApp,
                       imageSource,
                       name = "SourcePlot",
                       text = "SourceImage", 
                       position = (10,10),
                       padX = 0, padY = 0,
                       sticky = (tk.W,tk.E), columnSpan = 1, rowSpan = 1,
                       owner = None):
                
                if owner == None:
                        owner = rootApp
                
                fig = plt.figure(num = name, figsize=(2.5,2.5))
                ax = fig.add_subplot(1,1,1)
               
                ax.imshow(imageSource)                
                ax.set_title(text)
                canvas = FigureCanvasTkAgg(fig, master=owner)
                canvas.get_tk_widget().grid(row = position[0],column = position[1],
                                padx = padX,pady = padY,
                                columnspan = columnSpan, rowspan = rowSpan,
                                sticky= sticky)
                
                canvas.show()
                rootApp.controls[name] = canvas.get_tk_widget()
        @staticmethod            
        def DrawSignalPlot(rootApp,
                       signalData,
                       name = "SourcePlot",
                       text = "Signal View'",
                       xLabel = "time (s)",
                        yLabel = "voltage (mV)",
                       position = (10,10),
                       padX = 0, padY = 0,
                       sticky = (tk.S,tk.W), columnSpan = 1, rowSpan = 1,
                       owner = None):
                
                if owner == None:
                        owner = rootApp
                colors = [i + j for j in 'o<.' for i in 'bgrcmyk']
                print(colors)
                fig, ax = plt.subplots()
                
                plt.tight_layout(rect=[.01,.2,.72,1])
                ax.set(xlabel=xLabel, ylabel=yLabel,
                       title=text)
                ax.grid('on')      
                
                canvas = FigureCanvasTkAgg(fig, master=owner)
                canvas.get_tk_widget().grid(row = position[0],column = position[1],
                                padx = padX,pady = padY,
                                columnspan = columnSpan, rowspan = rowSpan,
                                sticky= sticky)
                
                
                canvas.show()
                rootApp.signalPlotters[name] = (ax,canvas,fig)
                rootApp.controls[name] = canvas.get_tk_widget()
        
        @staticmethod
        def DrawAxisArray(rootApp, name = "SourcePlot",
                       text = "Signal View'",
                       xLabel = "time (s)",
                        yLabel = "voltage (mV)",
                       position = (10,10),
                       padX = 0, padY = 0,
                       sticky = (tk.S,tk.W), columnSpan = 1, rowSpan = 1,
                       owner = None):
                if owner == None:
                        owner = rootApp
                fig, axis_array = plt.subplots(2,2)
                plt.tight_layout()
                
                for i in range(2):
                        for j in range(2):
                                axis_array[i,j].grid('on')
                                axis_array[i,j].set(title = 'AX [{0},{1}] - Not Initialized!'.format(i,j))
                axis_array[0,0].set(title= 'Workspace Signals')
                canvas = FigureCanvasTkAgg(fig, master=owner)
                canvas.get_tk_widget().grid(row = position[0],column = position[1],
                                padx = padX,pady = padY,
                                columnspan = columnSpan, rowspan = rowSpan,
                                sticky= sticky)
                
                
                canvas.show()
                rootApp.signalPlotters[name] = (axis_array,canvas,fig)
                rootApp.controls[name] = canvas.get_tk_widget()


        @staticmethod
        def __getColorsList():
                return [i + j for j in 'o<.' for i in 'bgrcmyk']
        @staticmethod
        def DrawList(rootApp,
                           name = "historyListBox",
                           position = (10,10),
                           padX = 0, padY = 0,
                           sticky = (tk.W,tk.E), columnSpan = 1, rowSpan = 1,
                           onItemSelectedCommand = None,listSelectMode = tk.SINGLE,
                           owner = None):
                if owner == None:
                        owner = rootApp
                parentFrame = tk.Frame(owner)
                parentFrame.grid(row = position[0],column = position[1],
                                padx = padX,pady = padY,
                                columnspan = columnSpan, rowspan = rowSpan,
                                sticky= sticky)
                scrollBar = tk.Scrollbar(parentFrame)
                scrollBar.pack(side=tk.RIGHT,fill = tk.Y)
                newControl = tk.Listbox(parentFrame,selectmode = listSelectMode,
                                        yscrollcommand = scrollBar.set)
                if onItemSelectedCommand != None:
                        newControl.bind("<<ListboxSelect>>",
                                        onItemSelectedCommand)
                newControl.pack(side=tk.LEFT,fill = tk.BOTH)
                scrollBar.config(command= newControl.yview)
                rootApp.controls[name] = newControl