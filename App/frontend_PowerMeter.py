
# 'python3 -m pip install tkinter'
# 'python3 -m pip install matplotlib'

import tkinter as tk
from tkinter import ttk
import backend_analysis
import matplotlib.pyplot as plt
import threading
import time

backgroundColour = '#DAEFD2'
previousScreen = tk.Frame

country = ["Ireland", "France", "Great Britain", "Russia", "Australia", "Brazil", "New Zealand", "United States", "Spain", "Portugal", "Italy","Germany"]
countryID = ["IE", "FR", "GB", "RU", "AU", "BR", "NZ", "US", "ES", "PT", "IT", "DE"]
intCountry = 0

# def countdownFunction() :
#     for countdown in range(0, 60, 1) :
#         countdownDisplay = "0:" + str(59-countdown).zfill(2)
#         print(countdownDisplay)
#         tk.Canvas.update_idletasks
#         time.sleep(1)
# countdownThread = threading.Thread(target=countdownFunction)

# def runAppTest(controller) :
#     controller.show_frame(AppTesting)
#     # for sec in range(0, 60, 1):
#     #     timeRemaining = str(sec).zfill(2)
#     #     globalCanvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
#     #     globalCanvas.create_text(200, 200, text=timeRemaining, font=('Arial Bold', 40), fill="black", justify="center")
#     print("here\n")
#     #     globalCanvas.update()
#     countdownThread.start()

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {} 


        for F in (HomePage, ContinuousPowerUsagePage, IndividualMeasurmentPage, AppTesting, IndividualResultsPage ,SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(HomePage)
  

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def updateCountry(self, newCountry):
        global intCountry
        intCountry = newCountry
    
    # def startTest(self,durationInput,canvas,values,currentCountry):
    # ##Calling the analysis function
    #     backendData = backend_analysis.dataAnalysis(durationInput, countryID[currentCountry])
    #     wattInput = backendData[0]
    #     carbonEmissions = (((backendData[1])/60)/12)*1000000
    #     print(wattInput)
    #     print(carbonEmissions)
    #     canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
    #     canvas.create_text(200, 200, text=str(round(wattInput, 2)) + " W", font=('Arial Bold', 40+16), fill="black", justify="center")
    #     canvas.create_text(200, 245, text=str(round(carbonEmissions, 2)) + " mgCO₂", font=('Arial Light', 18), fill="gray", justify="center")
    #     canvas.create_text(200, 160, text="Ø", font=('Arial Light', 18), fill="gray", justify="center")
    #     canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")
    #     canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=8, start=315, extent="%d" % round(270-((wattInput/100)*270)))
    #     values.create_rectangle(5, 5, 150, 250, outline=backgroundColour,fill=backgroundColour)
    #     values.create_text(40,40,text = "GPU : ",font =('Arial Bold', 18),fill="black", justify="center")
    #     values.create_text(40,80,text = "CPU :",font =('Arial Bold', 18),fill="black", justify="center")
    #     values.create_text(40,120,text = "RAM :",font =('Arial Bold', 18),fill="black", justify="center")
    #     if backendData[2] == 0:
    #         values.create_text(100,40,text = "N/A",font =('Arial Light', 12),fill="black", justify="center")
    #     else:
    #         values.create_text(100,40,text = str(round(backendData[2],2)) + " W",font =('Arial Light', 12),fill="black", justify="center")
    #     values.create_text(100,80,text = str(round(backendData[3],2)) + " W",font =('Arial Light', 12),fill="black", justify="center")
    #     values.create_text(100,120,text = str(round(backendData[4],2))+ " W",font =('Arial Light', 12),fill="black", justify="center")

        
    def settingsStart(self,controller):
        global previousScreen
        previousScreen = HomePage
        controller.show_frame(SettingsPage)

    def settingsPage1(self,controller):
        global previousScreen
        previousScreen = ContinuousPowerUsagePage
        controller.show_frame(SettingsPage)

    def settingsPage2(self,controller):
        global previousScreen
        previousScreen = IndividualMeasurmentPage
        controller.show_frame(SettingsPage)

    def graphToDisplay(self,data):
        time = []
        power = []
        plt.figure("Continuous Graph",facecolor='#DAEFD2')
        plt.title(label='Displaying Power Usage')
        plt.xlabel('Time (Seconds)')
        plt.ylabel('Power (Watts)')
        if data:
            for i in range(6,data[5]+6):
                power.append(data[i])
            for i in range(data[5]):
                time.append(i)
            plt.plot(time, power,color='#516E4C')
            plt.show()

    def getContinuousData(self,canvas,values,processorValuesImage):
        global run
        run = True
        self.update()
        global data
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_text(200, 200, text='Calculating ... ', font=('Arial Bold', 40), fill="black", justify="center")
        canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")
        self.update()
        carbon = 0
        peakWatts = 0
        averageWatts = 0
        averageCarbon = 0
        while run:
            self.update()
            data = backend_analysis.dataAnalysis(2, countryID[intCountry])
            averageWatts += data[0]
            self.update()
            watt = data[0]
            self.update()
            carbon = (((data[1])/60)/12)*1000000
            averageCarbon += carbon
            if (peakWatts<data[0]):
                peakWatts = data[0]
            self.update()
            self.update()
            canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
            canvas.create_text(200, 200, text=str(round(watt, 2)) + " W", font=('Arial Bold', 56), fill="black", justify="center")
            self.update()
            canvas.create_text(200, 245, text=str(round(carbon, 2)) + " mgCO₂", font=('Arial Light', 18), fill="gray", justify="center")
            canvas.create_text(200, 160, text="Ø", font=('Arial Light', 18), fill="gray", justify="center")
            self.update()
            canvas.create_arc(5, 5, 395, 395, fill = "black",outline="black", style=tk.ARC, width=6, start=315, extent="270")
            #arc is calculated by the current power against the peak watt
            self.update()
            peakArc = round(270-((watt/peakWatts)*270))
            if (peakArc>270):
                peakArc = 270
            canvas.create_arc(5, 5, 395, 395, fill = "white",outline="white", style=tk.ARC, width=8, start=315, extent=peakArc)
            self.update()
            values.create_image(10,10,anchor=tk.NW,image=processorValuesImage)
            if data[2] == 0:
                values.create_text(110,69,text = "N/A",font =('Arial Light', 12),fill="black", justify="center")
            else:
                values.create_text(110,69,text = str(round(data[2], 2)) + " W",font =('Arial Light', 10),fill="black", justify="center")
            self.update()
            values.create_text(110,47,text = str(round(data[3], 2)) + " W",font =('Arial Light', 10),fill="black", justify="center")
            values.create_text(110,92,text = str(round(data[4], 2)) + " W",font =('Arial Light', 10),fill="black", justify="center")
            self.update()
        averageWatts /= (data[5]/2)
        averageCarbon /= (data[5]/2)
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_text(200, 160, text="Average Power", font=('Arial Bold', 24), fill="black", justify="center")
        canvas.create_text(200, 200, text=str(round(averageWatts, 2)) + " W", font=('Arial Bold', 56), fill="black", justify="center")
        canvas.create_text(200, 240, text="Average Carbon", font=('Arial Light', 18), fill="gray", justify="center")
        canvas.create_text(200, 270, text=str(round(carbon, 2)) + " mgCO₂", font=('Arial Light', 28), fill="gray", justify="center")

    def stop(self):
        global run
        run = False
    
    # def countdownFunction() :
    #     for countdown in range(0, 60, 1) :
    #         countdownDisplay = "0:" + str(59-countdown).zfill(2)
    #         print(countdownDisplay)
    #         # canvas.update_idletasks
    #         time.sleep(1)
    # countdownThread = threading.Thread(target=countdownFunction)

    # def updateCountdown(canvas):
    #     print ("update")

    # def runAppTest(controller,canvas) :
    #     controller.show_frame(AppTesting)
    # # for sec in range(0, 60, 1):
    # #     timeRemaining = str(sec).zfill(2)
    # #     globalCanvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
    # #     globalCanvas.create_text(200, 200, text=timeRemaining, font=('Arial Bold', 40), fill="black", justify="center")
    #     print("here\n")
    # #     globalCanvas.update()
    #     controller.countdownThread.start()

    def baselineCountdown(self, canvas, titleCanvas):

        # global checkBaseline
        # checkBaseline = True

        countDown = 60
        titleCanvas.create_rectangle(0,0,500,700, fill=backgroundColour, outline=backgroundColour)
        titleCanvas.create_text(150, 50, text="Measuring ...",font=('Arial Bold', 32),fill="black", justify="center")
        titleCanvas.create_text(200, 100, text="Please wait while we measure the idle power use\nof your device. Please ensure that you keep all other\napps closed until this test completes.",font=('Arial Light', 15),fill="black", justify="center")
        self.update()
        while countDown >0:
            # self.config(cursor="none")
            canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
            canvas.create_text(200, 200, text="0 : " + str(countDown), font=('Arial Bold', 56),fill="black", justify="center")
            self.update()
            time.sleep(1)
            countDown-= 1
            print(countDown)
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_text(200, 200, text="Open App then press Test App",font=('Arial Bold', 22),fill="black", justify="center")
        #call backend to get baseline here

    # def getBaseline(controller):
    #     return checkBaseline

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        backgroundColour = '#DAEFD2'
        tk.Frame.__init__(self, parent, background=backgroundColour)

        titleLabel = ttk.Label(self, text="Sustainable Software",style= 'Test.TLabel',font=('Arial Bold', 28))

        overallImage = tk.PhotoImage(file='App/overallButton.png')
        overallImage = overallImage.subsample(2)
        overallButton = tk.Button(self,text="Continuous Usage", image = overallImage, height = 100, width = 235, borderwidth = 0, 
                                 command = lambda : controller.show_frame(ContinuousPowerUsagePage))
        overallButton.image = overallImage

        singleImage = tk.PhotoImage(file='App/singleButton.png')
        singleImage = singleImage.subsample(2)
        singleButton = tk.Button(self,text="Individual Usage", image = singleImage, height = 100, width = 235, borderwidth = 0, 
                                 command = lambda : controller.show_frame(IndividualMeasurmentPage))
        singleButton.image = singleImage

        bannerImage = tk.PhotoImage(file='App/banner.png')
        bannerImage = bannerImage.subsample(2)
        bannerLabel = ttk.Label(self, image=bannerImage, border=0)
        bannerLabel.image = bannerImage

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsStart(controller))
        settingsButton.image = settingsImage
        
        titleLabel.grid(row = 1, column = 1, columnspan = 2, rowspan = 1, padx = 50, pady = 100)
        bannerLabel.grid(row = 1, column = 3,padx = 50, pady = 100)
        overallButton.grid(row = 2, column = 2,padx = 50, pady = 0)
        singleButton.grid(row = 2, column = 3, padx = 10, pady = 0)
  

class ContinuousPowerUsagePage(tk.Frame):
     
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,background=backgroundColour)

        durationLabel = tk.Label(self, text="Measuring Live Data" , font=('Arial Light', 18), bg=backgroundColour, fg="black")
        titleLabel = tk.Label(self, text="Overall Power Usage", font=('Arial Bold', 32), bg=backgroundColour, fg="black")

        returnButton = tk.Button(self, text ="Return",command = lambda : controller.show_frame(HomePage))

        startImage = tk.PhotoImage(file='App/CUStart.png')
        startImage = startImage.subsample(2)
        startButton = tk.Button(self, text="Start", image=startImage, height=125, width=125, borderwidth=0,command = lambda : controller.getContinuousData(canvas,values,processorValuesImage))
        startButton.image = startImage

        stopImage = tk.PhotoImage(file='App/CUStop.png')
        stopImage = stopImage.subsample(2)
        stopButton = tk.Button(self, text="Stop", image=stopImage, height=125, width=125, borderwidth=0,command = lambda : controller.stop())
        stopButton.image = stopImage

        graphImage = tk.PhotoImage(file='App/CUGraph.png')
        graphImage = graphImage.subsample(2)
        graphButton = tk.Button(self, text="View Graph", image=graphImage, height=125, width=125, borderwidth=0,command = lambda : controller.graphToDisplay(data))
        graphButton.image = graphImage

        processorValuesImage = tk.PhotoImage(file='App/CUValues.png')
        processorValuesImage = processorValuesImage.subsample(2)
        values = tk.Canvas(self, background=backgroundColour,height=150, width=150, highlightthickness=0)
        values.create_image(10,10,anchor=tk.NW,image=processorValuesImage)
        GPU_values = values.create_text(110,47,text = "TBC",font =('Arial Light', 12),fill="black", justify="center")
        CPU_values = values.create_text(110,69,text = "TBC",font =('Arial Light', 12),fill="black", justify="center")
        GPU_values = values.create_text(110,92,text = "TBC",font =('Arial Light', 12),fill="black", justify="center")

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.settingsPage1(controller))

        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        intCircle = canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        backArc = canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")
        startText = canvas.create_text(200, 200, text='Press "Start"', font=('Arial Bold', 40), fill="black", justify="center")
        subtitleText = canvas.create_text(200, 245, text="TO BEGIN MEASURING", font=('Arial Light', 18), fill="gray", justify="center")

        returnImage = tk.PhotoImage(file='App/Return.png')
        returnImage = returnImage.subsample(2)
        returnButton = tk.Button(self, text ="Return",image=returnImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.show_frame(HomePage))
        returnButton.image = returnImage    

        settingsButton.image = settingsImage
        processorValuesImage.image = processorValuesImage
     
        durationLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
        titleLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 40, pady = 0)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        returnButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        startButton.grid(row = 1, column = 0,sticky = tk.SE, padx = 30)
        stopButton.grid(row = 1, column = 1,sticky = tk.SW)
        graphButton.grid(row = 2, column = 0,sticky = tk.NE, padx = 30, rowspan = 4)
        values.grid(row = 2, column = 1, sticky = tk.NW, padx = 0, pady = 2, rowspan= 4)
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
  
class IndividualMeasurmentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Test.TLabel', background= backgroundColour)

        # titleLabel = ttk.Label(self, text="App Power Usage",style= 'Test.TLabel',font=('Arial Bold', 32))
        # infoLabel = ttk.Label(self, text="Measure the idle energy use of your device with the\nmeasure baseline function while no applications are\nopen and then test the app for statistics.", font=('Arial Light', 15), style= 'Test.TLabel')

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsPage2(controller))
        settingsButton.image = settingsImage

        baselineImage = tk.PhotoImage(file='App/Baseline.png')
        baselineImage = baselineImage.subsample(2)
        baselineButton = tk.Button(self,text="Start", image = baselineImage, height = 150, width = 150, borderwidth = 0, 
                                 command = lambda : controller.baselineCountdown(canvas, titleCanvas))
        baselineButton.image = baselineImage

        appTestImage = tk.PhotoImage(file='App/AppTest.png')
        appTestImage = appTestImage.subsample(2)
        appTestButton = tk.Button(self,text="Start", image = appTestImage, height = 150, width = 150, borderwidth = 0, command= lambda : controller.show_frame(AppTesting))
        appTestButton.image = appTestImage

        returnImage = tk.PhotoImage(file='App/Return.png')
        returnImage = returnImage.subsample(2)
        returnButton = tk.Button(self, text ="Return",image=returnImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.show_frame(HomePage))
        returnButton.image = returnImage

        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")
        canvas.create_text(200, 180, text='Intructions', font=('Arial Bold', 40), fill="black", justify="center")
        canvas.create_text(200, 220, text="1. Close All Unnecessary Applications", font=('Arial Light', 18), fill="gray", justify="center")
        canvas.create_text(200, 245, text="1. Press 'Get Baseline'", font=('Arial Light', 18), fill="gray", justify="center")
        canvas.create_text(200, 270, text="2. Open App to Measure", font=('Arial Light', 18), fill="gray", justify="center")
        canvas.create_text(200, 295, text="3. Press 'Test App'", font=('Arial Light', 18), fill="gray", justify="center")

        titleCanvas = tk.Canvas(self, background=backgroundColour, height=200, width=400, highlightthickness=0)
        titleLabel = titleCanvas.create_text(170, 50, text="App Power Usage", font=('Arial Bold', 32), fill="black", justify="center")
        infoLabel = titleCanvas.create_text(200,100, text="Measure the idle energy use of your device with\nthe'Get Baseline' function, while no applications\nare open, then 'Test App' function for statistics.", font=('Arial Light', 15), fill="black", justify="center")        
        

        # values = tk.Canvas(self, background=backgroundColour,height=150, width=150, highlightthickness=0)
        # values.create_rectangle(5, 5, 150, 250, outline=backgroundColour,fill=backgroundColour)
        # values.create_text(40,40,text = "GPU : ",font =('Arial Bold', 18),fill="black", justify="center")
        # values.create_text(40,80,text = "CPU :",font =('Arial Bold', 18),fill="black", justify="center")
        # values.create_text(40,120,text = "RAM :",font =('Arial Bold', 18),fill="black", justify="center")
        # values.create_text(100,40,text = "TBC",font =('Arial Light', 12),fill="black", justify="center")
        # values.create_text(100,80,text = "TBC",font =('Arial Light', 12),fill="black", justify="center")
        # values.create_text(100,120,text = "TBC",font =('Arial Light', 12),fill="black", justify="center")

        # infoLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = (40,0), pady = 0)
        # titleLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
        baselineButton.grid(row = 2, column = 0, sticky = tk.E, padx = (40,20), pady = 2)
        appTestButton.grid(row = 2, column = 1, sticky = tk.W, padx = (20,0), pady = 2)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        returnButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
        titleCanvas.grid(row= 1, column= 0,columnspan = 2, rowspan = 1, padx=20)
          

class IndividualResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)
        # tk.Tk.configure(self, bg='#DAEFD2')

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsAppTestHome(controller))
        settingsButton.image = settingsImage

        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        titleLabel = ttk.Label(self, text="Results",style= 'Test.TLabel',font=('Arial Bold', 32), padding=(0,22,0,0))
#         infoLabel = ttk.Label(self, text="Please wait while we measure the idle power use of\nyour device. Please ensure that you keep all other\napps closed until this test completes.", font=('Arial Light', 15), style= 'Test.TLabel')

#         countdownLabel = ttk.Label(self, text=countdownDisplay,style= 'Test.TLabel',font=('Arial Bold', 64), padding=(0,22,0,0))

        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=6, start=315, extent="270")
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")

        carbonImage = tk.PhotoImage(file='App/Carbon.png')
        carbonImage = carbonImage.subsample(6)
        canvas.image = carbonImage
        canvas.create_image(200,350,anchor=tk.S,image=carbonImage)
        

#         infoLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = (40,0), pady = 0)
        titleLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
#         countdownLabel.grid(row = 2, column = 0, sticky = tk.NW, padx = (40,20), pady = 2)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)


class AppTesting(tk.Frame):
    def __init__(self, parent, controller):

        # global checkBaseline
        # checkBaseline = False
        # tkinterApp.getBaseline(controller)
        # print(checkBaseline)
        # if checkBaseline:
        #     print("show")


        tk.Frame.__init__(self, parent, background=backgroundColour)
        # tk.Tk.configure(self, bg='#DAEFD2')
        countdownDisplay = "0:00"

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsAppTestHome(controller))
        settingsButton.image = settingsImage

        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        titleLabel = ttk.Label(self, text="Measuring...",style= 'Test.TLabel',font=('Arial Bold', 32), padding=(0,22,0,0))
        infoLabel = ttk.Label(self, text="Please wait while we measure the idle power use of\nyour device. Please ensure that you keep all other\napps closed until this test completes.", font=('Arial Light', 15), style= 'Test.TLabel')

        stopImage = tk.PhotoImage(file='App/Stop.png')
        stopImage = stopImage.subsample(2)
        stopButton = tk.Button(self,text="Start", image = stopImage, height = 150, width = 150, borderwidth = 0, 
                                 command = lambda : controller.show_frame(IndividualResultsPage))
        stopButton.image = stopImage

        returnImage = tk.PhotoImage(file='App/Return.png')
        returnImage = returnImage.subsample(2)
        returnButton = tk.Button(self, text ="Return",image=returnImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.show_frame(IndividualMeasurmentPage))
        returnButton.image = returnImage

        # tk.Tk.configure(self, bg='#DAEFD2')

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
        returnButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        # globalCanvas = canvas

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)

        def changeRegion(i,buttonText):
            countryLabel["text"] = buttonText
            countryLabel.update
            controller.updateCountry(i)

        returnButton = tk.PhotoImage(file='App/Return.png')
        returnButton = returnButton.subsample(2)
        returnButton.image = returnButton
        returnButton = tk.Button(self, text ="Return",image=returnButton, height = 50, width = 100, borderwidth = 0, command = lambda : controller.show_frame(previousScreen))        
        
        currentLabel = ttk.Label(self, text="Current Country: ", font=('Arial Light', 18), style= 'Test.TLabel')
        countryLabel = ttk.Label(self, text="Ireland", font=('Arial Light', 18), style= 'Test.TLabel')

        irlImage = tk.PhotoImage(file='App/flagIreland.png')
        irlImage = irlImage.subsample(1)
        irlButton = tk.Button(self, text ="Ireland",image = irlImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                               command = lambda : changeRegion(0, irlButton["text"]))
        irlButton.image = irlImage

        fraImage = tk.PhotoImage(file='App/flagFrance.png')
        fraImage = fraImage.subsample(1)
        fraButton = tk.Button(self, text ="France",image = fraImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(1,fraButton["text"]))
        fraButton.image = fraImage

        ukImage = tk.PhotoImage(file='App/flagUK.png')
        ukImage = ukImage.subsample(1)
        ukButton = tk.Button(self, text ="United Kingdom",image = ukImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(2,ukButton["text"]))
        ukButton.image = ukImage

        rusImage = tk.PhotoImage(file='App/flagRussia.png')
        rusImage = rusImage.subsample(1)
        rusButton = tk.Button(self, text ="Russia",image = rusImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(3,rusButton["text"]))
        rusButton.image = rusImage

        ausImage = tk.PhotoImage(file='App/flagAustralia.png')
        ausImage = ausImage.subsample(1)
        ausButton = tk.Button(self, text ="Australia",image = ausImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(4,ausButton["text"]))
        ausButton.image = ausImage

        braImage = tk.PhotoImage(file='App/flagBrazil.png')
        braImage = braImage.subsample(1)
        braButton = tk.Button(self, text ="Brazil",image = braImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(5,braButton["text"]))
        braButton.image = braImage

        nzImage = tk.PhotoImage(file='App/flagNewZealand.png')
        nzImage = nzImage.subsample(1)
        nzButton = tk.Button(self, text ="New Zealand",image = nzImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(6,nzButton["text"]))
        nzButton.image = nzImage

        spaImage = tk.PhotoImage(file='App/flagSpain.png')
        spaImage = spaImage.subsample(1)
        spaButton = tk.Button(self, text ="Spain",image = spaImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(7,spaButton["text"]))
        spaButton.image = spaImage

        porImage = tk.PhotoImage(file='App/flagPortugal.png')
        porImage = porImage.subsample(1)
        porButton = tk.Button(self, text ="Portugal",image = porImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(8,porButton["text"]))
        porButton.image = porImage

        itaImage = tk.PhotoImage(file='App/flagItaly.png')
        itaImage = itaImage.subsample(1)
        itaButton = tk.Button(self, text ="Italy",image = itaImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(9,itaButton["text"]))
        itaButton.image = itaImage

        gerImage = tk.PhotoImage(file='App/flagGermany.png')
        gerImage = gerImage.subsample(1)
        gerButton = tk.Button(self, text ="Germany",image = gerImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(10,gerButton["text"]))
        gerButton.image = gerImage

        currentLabel.grid(row = 0, column = 2, sticky=tk.NW, padx = 5, pady = 5)
        countryLabel.grid(row = 0, column = 3, sticky=tk.NW, padx = 5, pady = 5)
        irlButton.grid(row = 1, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        fraButton.grid(row = 1, column = 1,sticky=tk.NW, padx = 5, pady = 5)
        ukButton.grid(row = 1, column = 2,sticky=tk.NW, padx = 5, pady = 5)
        rusButton.grid(row = 1, column = 3,sticky=tk.NW, padx = 5, pady = 5)
        ausButton.grid(row = 2, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        braButton.grid(row = 2, column = 1,sticky=tk.NW, padx = 5, pady = 5)
        nzButton.grid(row = 2, column = 2,sticky=tk.NW, padx = 5, pady = 5)
        spaButton.grid(row = 2, column = 3,sticky=tk.NW, padx = 5, pady = 5)
        porButton.grid(row = 3, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        itaButton.grid(row = 3, column = 1,sticky=tk.NW, padx = 5, pady = 5)
        gerButton.grid(row = 3, column = 2,sticky=tk.NW, padx = 5, pady = 5)

        returnButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        

app = tkinterApp()
app.resizable(False,False)
app.title("Sustainable Software")
app.mainloop()



