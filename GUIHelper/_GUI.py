import tkinter as tk
import tkinter.messagebox as messagebox
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Page(tk.Frame):
    controls = {}
    master_container = None
    def __init__(self,master, _master_container= None):
        tk.Frame.__init__(self, master= master)
        master_container = _master_container
        self.place(in_ = master_container, x=0, y=0, relwidth=1, relheight=1)
        self.draw_gui()

    def show(self):
        self.lift()

    def draw_gui(self):
        pass

class GUI:
    @staticmethod
    def InitRootApp(rootApp, master=None, title="Title", resizable=(True, True)):
        # print(rootApp)
        tk.Tk.__init__(rootApp, master)
        rootApp.grid()
        rootApp.title(title)
        rootApp.focus_set()
        rootApp.grid()
        rootApp.resizable(False, False)
        plt.ioff()

    @staticmethod
    def CreateSubWindow(rootApp, masterWindow, title="Title"):
        rootApp = tk.Toplevel(masterWindow)
        rootApp.title(title)
        return rootApp

    @staticmethod
    def CreateContainer(rootApp, pagesCount,onAddNewPageCommand,activationCallBack,deletePageCallback, page_text_prefix = 'Page',
        name='container_1', position=(0, 0), padX=0, padY=0, sticky=tk.NSEW, columnSpan=1, rowSpan=1, owner = None, navBarAlginment = 'bottom'):
        """
        Create a container with pages of pagesCount

        returns Pages List which has a tuple of page and btn associated, each page is a frame which can be used for drawing components within
        """

        if owner is None:
                owner = rootApp
        
        pages_list = []


        parentFrame = tk.Frame(owner)
        tk.Grid.rowconfigure(owner, position[0], weight = 1)
        tk.Grid.columnconfigure(owner, position[1], weight = 1)
        parentFrame.grid(row=position[0], column=position[1],
                         padx=padX, pady=padY,
                         columnspan=columnSpan, rowspan=rowSpan,
                         sticky=sticky)
        
        buttonframe = tk.Frame(parentFrame)
        container = tk.Frame(parentFrame)
        buttonframe.pack(side= navBarAlginment, fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        for i in range(pagesCount):
                p = Page(master = owner, _master_container= container)
                btn = tk.Button(buttonframe, text="{0} {1}".format(page_text_prefix, i+1), command= lambda n_p=p : GUI.__activate_page(n_p, activationCallBack, pages_list))
                btn.pack(side="left")
                if  i > 0:
                        delbtn = tk.Button(buttonframe, text= 'x', foreground= 'red')
                        delbtn.configure(command = lambda n_p=p, del_p = delbtn, pg_btn = btn, n_i = i : deletePageCallback(n_p, pg_btn, del_p, n_i))
                        delbtn.pack(side='left')
                pages_list.append((p, btn))
        btn = tk.Button(buttonframe, text = '+', command= lambda: GUI.__add_new_page(owner, container, pages_list, buttonframe, onAddNewPageCommand, activationCallBack, deletePageCallback, page_text_prefix))
        btn.pack(side='right')
        rootApp.controls[name] = pages_list
        GUI.__activate_page(pages_list[0][0], None, pages_list)
        return pages_list        
    
    @staticmethod
    def __activate_page(page, callback, pages):
        page.lift()
        for x in pages:
            if x[0] is page:
                x[1].configure(foreground = 'green')
            else:
                x[1].configure(foreground='black')
        if callback is not None:
            callback(page)
    
    @staticmethod  
    def __add_new_page(owner, container, pages_list, buttonframe, callback, activationCallBack, deletePageCallback, page_text_prefix):
            p = Page(master = owner, _master_container= container)
            btn = tk.Button(buttonframe, text="{0} {1}".format(page_text_prefix, len(pages_list)+1), command= lambda n_p=p : GUI.__activate_page(n_p, activationCallBack, pages_list))
            btn.pack(side="left")
            delbtn = tk.Button(buttonframe, text= 'x', foreground= 'red')
            delbtn.configure(command = lambda n_p=p, del_p = delbtn, pg_btn = btn, n_i = len(pages_list) : deletePageCallback(n_p, pg_btn, del_p, n_i))
            delbtn.pack(side='left')
            pages_list.append((p, btn))
            
            callback(p, btn)

    @staticmethod
    def DrawButton(rootApp, name="Button1", text="test", position=(0, 0),
                   onClickCommand=None, padX=0, padY=0,
                   sticky=(tk.W, tk.E), columnSpan=1, rowSpan=1,
                   owner=None):
        if owner == None:
            owner = rootApp

        newControl = tk.Button(owner, text=text, command=onClickCommand)
        newControl.grid(row=position[0], column=position[1],
                        padx=padX, pady=padY,
                        columnspan=columnSpan, rowspan=rowSpan, sticky=sticky)

        rootApp.controls[name] = newControl

    @staticmethod
    def DrawLabel(rootApp, name="Label1", text="test", position=(10, 10),
                  padX=0, padY=0,
                  sticky=(tk.W, tk.E), columnSpan=1, rowSpan=1,
                  owner=None):
        if owner == None:
            owner = rootApp
        newControl = tk.Label(owner, text=text)
        newControl.grid(row=position[0], column=position[1],
                        padx=padX, pady=padY,
                        columnspan=columnSpan, rowspan=rowSpan,
                        sticky=sticky)

        rootApp.controls[name] = newControl

    @staticmethod
    def DrawEntry(rootApp, variable, name="Entry1", position=(10, 10),
                  padX=0, padY=0,
                  sticky=(tk.W, tk.E), columnSpan=1, rowSpan=1,
                  owner=None):
        if owner == None:
            owner = rootApp

        newControl = tk.Entry(owner, textvariable=variable)
        newControl.grid(row=position[0], column=position[1],
                        padx=padX, pady=padY,
                        columnspan=columnSpan, rowspan=rowSpan,
                        sticky=sticky)
        rootApp.controls[name] = newControl

    @staticmethod
    def DrawCheckBox(rootApp, variable, text='text', name="ch1", position=(10, 10),
                     padX=0, padY=0,
                     sticky=(tk.W, tk.E), columnSpan=1, rowSpan=1,
                     owner=None):
        if owner == None:
            owner = rootApp

        newControl = tk.Checkbutton(owner, text=text, variable=variable)
        newControl.grid(row=position[0], column=position[1],
                        padx=padX, pady=padY,
                        columnspan=columnSpan, rowspan=rowSpan,
                        sticky=sticky)
        rootApp.controls[name] = newControl

    @staticmethod
    def DrawGroupBox(rootApp, name="GroupBox1", text="GroupBox1",
                     position=(10, 10),
                     padX=0, padY=0,
                     sticky=(tk.W, tk.E), columnSpan=1, rowSpan=1,
                     owner=None):
        if owner == None:
            owner = rootApp
        newControl = tk.LabelFrame(owner, text=text)
        newControl.grid(row=position[0], column=position[1],
                        padx=padX, pady=padY,
                        columnspan=columnSpan, rowspan=rowSpan,
                        sticky=sticky)
        rootApp.controls[name] = newControl
        return rootApp.controls[name]

    @staticmethod
    def DrawOptions(rootApp,
                    variable,
                    *options,
                    name="Options1",
                    position=(10, 10),
                    padX=0, padY=0,
                    sticky=(tk.W, tk.E), columnSpan=1, rowSpan=1,
                    owner=None):
        if owner == None:
            owner = rootApp

        newControl = tk.OptionMenu(owner, variable, *options)

        newControl.grid(row=position[0], column=position[1],
                        padx=padX, pady=padY,
                        columnspan=columnSpan, rowspan=rowSpan,
                        sticky=sticky)
        rootApp.controls[name] = newControl

    @staticmethod
    def DrawImagePlot(rootApp,
                      imageSource,
                      name="SourcePlot",
                      text="SourceImage",
                      position=(10, 10),
                      padX=0, padY=0,
                      sticky=(tk.W, tk.E), columnSpan=1, rowSpan=1,
                      owner=None):

        if owner == None:
            owner = rootApp

        fig = plt.figure(num=name, figsize=(2.5, 2.5))
        ax = fig.add_subplot(1, 1, 1)

        ax.imshow(imageSource)
        ax.set_title(text)
        canvas = FigureCanvasTkAgg(fig, master=owner)
        canvas.get_tk_widget().grid(row=position[0], column=position[1],
                                    padx=padX, pady=padY,
                                    columnspan=columnSpan, rowspan=rowSpan,
                                    sticky=sticky)

        canvas.show()
        rootApp.controls[name] = canvas.get_tk_widget()

    @staticmethod
    def DrawSignalPlot(rootApp,
                       signalData,
                       name="SourcePlot",
                       text="Signal View'",
                       xLabel="time (s)",
                       yLabel="voltage (mV)",
                       position=(10, 10),
                       padX=0, padY=0,
                       sticky=(tk.S, tk.W), columnSpan=1, rowSpan=1,
                       owner=None):

        if owner == None:
            owner = rootApp
        colors = [i + j for j in 'o<.' for i in 'bgrcmyk']
        print(colors)
        fig, ax = plt.subplots()

        plt.tight_layout(rect=[.01, .2, .72, 1])
        ax.set(xlabel=xLabel, ylabel=yLabel,
               title=text)
        ax.grid('on')

        canvas = FigureCanvasTkAgg(fig, master=owner)
        canvas.get_tk_widget().grid(row=position[0], column=position[1],
                                    padx=padX, pady=padY,
                                    columnspan=columnSpan, rowspan=rowSpan,
                                    sticky=sticky)

        canvas.show()
        rootApp.signalPlotters[name] = (ax, canvas, fig)
        rootApp.controls[name] = canvas.get_tk_widget()

    @staticmethod
    def DrawAxisArray(rootApp, name="SourcePlot",
                      text="Signal View'",
                      xLabel="time (s)",
                      yLabel="voltage (mV)",
                      position=(10, 10),
                      padX=0, padY=0,
                      sticky=(tk.S, tk.W), columnSpan=1, rowSpan=1,nrows = 2, ncols = 2,
                      owner=None):
        if owner == None:
            owner = rootApp
        fig, axis_array = plt.subplots(nrows, ncols)
        plt.tight_layout()

        for i in range(nrows):
            for j in range(ncols):
                axis_array[i, j].grid('on')
                axis_array[i, j].set(
                    title='AX [{0},{1}] - Not Initialized!'.format(i, j))
        axis_array[0, 0].set(title='Workspace Signals')
        canvas = FigureCanvasTkAgg(fig, master=owner)
        canvas.get_tk_widget().grid(row=position[0], column=position[1],
                                    padx=padX, pady=padY,
                                    columnspan=columnSpan, rowspan=rowSpan,
                                    sticky=sticky)

        canvas.show()
        rootApp.signalPlotters[name] = (axis_array, canvas, fig)
        rootApp.controls[name] = canvas.get_tk_widget()

    @staticmethod
    def __getColorsList():
        return [i + j for j in 'o<.' for i in 'bgrcmyk']

    @staticmethod
    def DrawList(rootApp,
                 name="historyListBox",
                 position=(10, 10),
                 padX=0, padY=0,
                 sticky=(tk.W, tk.E), columnSpan=1, rowSpan=1,
                 onItemSelectedCommand=None, listSelectMode=tk.SINGLE,
                 owner=None):
        if owner == None:
            owner = rootApp
        parentFrame = tk.Frame(owner)
        parentFrame.grid(row=position[0], column=position[1],
                         padx=padX, pady=padY,
                         columnspan=columnSpan, rowspan=rowSpan,
                         sticky=sticky)
        scrollBar = tk.Scrollbar(parentFrame)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        newControl = tk.Listbox(parentFrame, selectmode=listSelectMode,
                                yscrollcommand=scrollBar.set)
        if onItemSelectedCommand != None:
            newControl.bind("<<ListboxSelect>>",
                            onItemSelectedCommand)
        newControl.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollBar.config(command=newControl.yview)
        rootApp.controls[name] = newControl

    @staticmethod
    def ShowConfirmMBox(title, message):
        return messagebox.askyesno(title= title, message= message)