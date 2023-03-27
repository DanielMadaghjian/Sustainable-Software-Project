
# 'python3 -m pip install tkinter'
# 'python3 -m pip install matplotlib'

import threading
import time
import tkinter as tk
from tkinter import ttk
import backend_analysis

LARGEFONT =('Arial',45)
backgroundColour = '#DAEFD2'

previousScreen = tk.Frame
baselineRun = False
countdownDisplay = "0:60"

globalCanvas = tk.Canvas

def countdownFunction() :
    for countdown in range(0, 60, 1) :
        countdownDisplay = "0:" + str(59-countdown).zfill(2)
        print(countdownDisplay)
        tk.Canvas.update_idletasks
        time.sleep(1)
countdownThread = threading.Thread(target=countdownFunction)

def runAppTest(controller) :
    controller.show_frame(AppTesting)
    # for sec in range(0, 60, 1):
    #     timeRemaining = str(sec).zfill(2)
    #     globalCanvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
    #     globalCanvas.create_text(200, 200, text=timeRemaining, font=('Arial Bold', 40), fill="black", justify="center")
    print("here\n")
    #     globalCanvas.update()
    countdownThread.start()

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {} 

        for F in (StartPage, AppTestHome, TimedTest, BaselineTest, AppTesting, AppResults, SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
  

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def startTest(self,durationInput,canvas,values):
    ##Calling the analysis function
        backendData = backend_analysis.dataAnalysis(durationInput, 'IE')
        wattInput = backendData[0]
        carbonEmissions = (((backendData[1])/60)/12)*1000000
        print(wattInput)
        print(carbonEmissions)
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_text(200, 200, text=str(round(wattInput, 2)) + " W", font=('Arial Bold', 40+16), fill="black", justify="center")
        canvas.create_text(200, 245, text=str(round(carbonEmissions, 2)) + " mgCO₂eq", font=('Arial Light', 18), fill="gray", justify="center")
        canvas.create_text(200, 160, text="Ø", font=('Arial Light', 18), fill="gray", justify="center")
        canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")
        canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=8, start=315, extent="%d" % round(270-((wattInput/100)*270)))
        values.create_rectangle(5, 5, 150, 250, outline=backgroundColour,fill=backgroundColour)
        values.create_text(40,40,text = "GPU : ",font =('Arial Bold', 18),fill="black", justify="center")
        values.create_text(40,80,text = "CPU :",font =('Arial Bold', 18),fill="black", justify="center")
        values.create_text(40,120,text = "RAM :",font =('Arial Bold', 18),fill="black", justify="center")
        if backendData[2] == 0:
            values.create_text(100,40,text = "N/A",font =('Arial Light', 12),fill="black", justify="center")
        else:
            values.create_text(100,40,text = str(round(backendData[2],2)) + " W",font =('Arial Light', 12),fill="black", justify="center")
        values.create_text(100,80,text = str(round(backendData[3],2)) + " W",font =('Arial Light', 12),fill="black", justify="center")
        values.create_text(100,120,text = str(round(backendData[4],2))+ " W",font =('Arial Light', 12),fill="black", justify="center")
    
    

    def navToSettings(self):
        listbox = tk.Listbox(self, width=40, height=10,selectmode=tk.SINGLE)
        listbox.insert(1, "Ireland")
        listbox.insert(2, "France")
        listbox.insert(3, "Great Britain")
        listbox.insert(4, "Russian")
        listbox.insert(5, "Australia")
        listbox.pack()
        for i in listbox.curselection():
            print(listbox.get(i))
            return listbox.get(i)
        
    def settingsStart(self,controller):
        global previousScreen
        previousScreen = StartPage
        controller.show_frame(SettingsPage)

    def settingsAppTestHome(self,controller):
        global previousScreen
        previousScreen = AppTestHome
        controller.show_frame(SettingsPage)

    def settingsTimedTest(self,controller):
        global previousScreen
        previousScreen = TimedTest
        controller.show_frame(SettingsPage)
    
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        backgroundColour = '#DAEFD2'
        tk.Frame.__init__(self, parent, background=backgroundColour)

        button1 = tk.Button(self, text ="Test an App's Power Usage",command = lambda : controller.show_frame(AppTestHome))
        button2 = tk.Button(self, text ="Test for a Specified Time",command = lambda : controller.show_frame(TimedTest))

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsStart(controller))
        #command = lambda : controller.navToSettings())
        settingsButton.image = settingsImage

        button1.grid(row = 1, column = 1,padx = 10, pady = 10)
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)

class AppTestHome(tk.Frame):
     
    def __init__(self, parent, controller):
        # backgroundColour = '#DAEFD2' 
        tk.Frame.__init__(self, parent)

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsAppTestHome(controller))
        #command = lambda : controller.navToSettings())
        settingsButton.image = settingsImage

        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        titleLabel = ttk.Label(self, text="App Power Usage",style= 'Test.TLabel',font=('Arial Bold', 32))
        infoLabel = ttk.Label(self, text="Measure the idle energy use of your device with the\nmeasure baseline function while no applications are\nopen and then test the app for statistics.", font=('Arial Light', 15), style= 'Test.TLabel')

        baselineImage = tk.PhotoImage(file='App/Baseline.png')
        baselineImage = baselineImage.subsample(2)
        baselineButton = tk.Button(self,text="Start", image = baselineImage, height = 150, width = 150, borderwidth = 0, 
                                 command = lambda : controller.show_frame(BaselineTest))
        baselineButton.image = baselineImage

        appTestImage = tk.PhotoImage(file='App/AppTest.png')
        appTestImage = appTestImage.subsample(2)
        appTestButton = tk.Button(self,text="Start", image = appTestImage, height = 150, width = 150, borderwidth = 0, 
                                 command = lambda : runAppTest(controller))
        appTestButton.image = appTestImage

        backImage = tk.PhotoImage(file='App/back.png')
        backImage = backImage.subsample(2)
        backButton = tk.Button(self, image=backImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.show_frame(StartPage))
        backButton.image = backImage

        tk.Tk.configure(self, bg='#DAEFD2')

        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=6, start=315, extent="270")
        canvas.create_text(200, 182, text="CARBON", font=('Arial', 22), fill='#A3B59C', justify="center")
        carbonImage = tk.PhotoImage(file='App/Carbon.png')
        carbonImage = carbonImage.subsample(6)
        canvas.image = carbonImage
        canvas.create_image(200,240,anchor=tk.S,image=carbonImage)
        canvas.update()

        infoLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = (40,0), pady = 0)
        titleLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
        baselineButton.grid(row = 2, column = 0, sticky = tk.E, padx = (40,20), pady = 2)
        appTestButton.grid(row = 2, column = 1, sticky = tk.W, padx = (20,0), pady = 2)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        backButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
  
class TimedTest(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Test.TLabel', background= backgroundColour)

        titleLabel = ttk.Label(self, text="Power Consumption",style= 'Test.TLabel',font=('Arial Bold', 32))
        durationLabel = ttk.Label(self, text="5 SECOND", font=('Arial Light', 18), style= 'Test.TLabel')

        startImage = tk.PhotoImage(file='App/Test.png')
        startImage = startImage.subsample(2)
        startButton = tk.Button(self,text="Start", image = startImage, height = 150, width = 150, borderwidth = 0, 
                                 command = lambda : controller.startTest(5,canvas,values))
        startButton.image = startImage

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsTimedTest(controller))
        #command = lambda : controller.navToSettings())
        settingsButton.image = settingsImage

        returnButton = tk.Button(self, text ="Return",command = lambda : controller.show_frame(StartPage))

        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")
        canvas.create_text(200, 200, text='Press "Start"', font=('Arial Bold', 40), fill="black", justify="center")
        canvas.create_text(200, 245, text="TO START A 5-SECOND TEST", font=('Arial Light', 18), fill="gray", justify="center")

        values = tk.Canvas(self, background=backgroundColour,height=150, width=150, highlightthickness=0)
        values.create_rectangle(5, 5, 150, 250, outline=backgroundColour,fill=backgroundColour)
        values.create_text(40,40,text = "GPU : ",font =('Arial Bold', 18),fill="black", justify="center")
        values.create_text(40,80,text = "CPU :",font =('Arial Bold', 18),fill="black", justify="center")
        values.create_text(40,120,text = "RAM :",font =('Arial Bold', 18),fill="black", justify="center")
        values.create_text(100,40,text = "TBC",font =('Arial Light', 12),fill="black", justify="center")
        values.create_text(100,80,text = "TBC",font =('Arial Light', 12),fill="black", justify="center")
        values.create_text(100,120,text = "TBC",font =('Arial Light', 12),fill="black", justify="center")

        titleLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 40, pady = 0)
        durationLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
        startButton.grid(row = 2, column = 0, sticky = tk.E, padx = 40, pady = 2)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        returnButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
        values.grid(row = 2, column = 1, sticky = tk.W, padx = 0, pady = 2)

        

class BaselineTest(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)
        tk.Tk.configure(self, bg='#DAEFD2')

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsAppTestHome(controller))
        #command = lambda : controller.navToSettings())
        settingsButton.image = settingsImage

        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        titleLabel = ttk.Label(self, text="Measuring...",style= 'Test.TLabel',font=('Arial Bold', 32), padding=(0,22,0,0))
        infoLabel = ttk.Label(self, text="Please wait while we measure the idle power use of\nyour device. Please ensure that you keep all other\napps closed until this test completes.", font=('Arial Light', 15), style= 'Test.TLabel')

        countdownLabel = ttk.Label(self, text=countdownDisplay,style= 'Test.TLabel',font=('Arial Bold', 64), padding=(0,22,0,0))

        tk.Tk.configure(self, bg='#DAEFD2')

        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=6, start=315, extent="270")
        
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")

        carbonImage = tk.PhotoImage(file='App/Carbon.png')
        carbonImage = carbonImage.subsample(6)
        canvas.image = carbonImage
        canvas.create_image(200,350,anchor=tk.S,image=carbonImage)
        

        infoLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = (40,0), pady = 0)
        titleLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
        countdownLabel.grid(row = 2, column = 0, sticky = tk.NW, padx = (40,20), pady = 2)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
        

class AppTesting(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)
        tk.Tk.configure(self, bg='#DAEFD2')

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsAppTestHome(controller))
        #command = lambda : controller.navToSettings())
        settingsButton.image = settingsImage

        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        titleLabel = ttk.Label(self, text="Measuring...",style= 'Test.TLabel',font=('Arial Bold', 32), padding=(0,22,0,0))
        infoLabel = ttk.Label(self, text="Please wait while we measure the idle power use of\nyour device. Please ensure that you keep all other\napps closed until this test completes.", font=('Arial Light', 15), style= 'Test.TLabel')

        stopImage = tk.PhotoImage(file='App/Stop.png')
        stopImage = stopImage.subsample(2)
        stopButton = tk.Button(self,text="Start", image = stopImage, height = 150, width = 150, borderwidth = 0, 
                                 command = lambda : controller.show_frame(BaselineTest))
        stopButton.image = stopImage

       

        tk.Tk.configure(self, bg='#DAEFD2')

        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=6, start=315, extent="270")
        
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")

        carbonImage = tk.PhotoImage(file='App/Carbon.png')
        carbonImage = carbonImage.subsample(6)
        canvas.image = carbonImage
        canvas.create_image(200,350,anchor=tk.S,image=carbonImage)
        canvas.create_text(200, 200, text=countdownDisplay, font=('Arial Bold', 40), fill='#DAEFD2', justify="center")
        

        infoLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = (40,0), pady = 0)
        titleLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
        stopButton.grid(row = 2, column = 0, sticky = tk.E, padx = (40,20), pady = 2)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
        globalCanvas = canvas
        

class AppResults(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)
        tk.Tk.configure(self, bg='#DAEFD2')
        

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)
        tk.Tk.configure(self, bg='#DAEFD2')
        returnButton = tk.Button(self, text ="Return",command = lambda : controller.show_frame(previousScreen))

        irlButton = tk.Button(self, text ="Ireland",command = lambda : controller.show_frame(previousScreen))
        fraButton = tk.Button(self, text ="France",command = lambda : controller.show_frame(previousScreen))
        ukButton = tk.Button(self, text ="United Kingdom",command = lambda : controller.show_frame(previousScreen))
        rusButton = tk.Button(self, text ="Russia",command = lambda : controller.show_frame(previousScreen))
        ausButton = tk.Button(self, text ="Australia",command = lambda : controller.show_frame(previousScreen))

        irlButton.grid(row = 1, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        fraButton.grid(row = 1, column = 1,sticky=tk.NW, padx = 5, pady = 5)
        ukButton.grid(row = 1, column = 2,sticky=tk.NW, padx = 5, pady = 5)
        rusButton.grid(row = 1, column = 3,sticky=tk.NW, padx = 5, pady = 5)
        ausButton.grid(row = 1, column = 4,sticky=tk.NW, padx = 5, pady = 5)
        returnButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)


app = tkinterApp()
app.mainloop()


