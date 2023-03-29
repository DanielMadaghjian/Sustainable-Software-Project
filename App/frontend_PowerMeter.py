
# 'python3 -m pip install tkinter'
# 'python3 -m pip install matplotlib'
from tkinter import *
import tkinter as tk
from tkinter import ttk
import backend_analysis
import matplotlib.pyplot as plt
import requests
import time

backgroundColour = '#DAEFD2'
previousScreen = tk.Frame

country = ["Ireland", "France", "Great Britain", "Russia", "Australia", "Brazil", "New Zealand", "United States", "Spain", "Portugal", "Italy","Germany"]
countryID = ["IE", "FR", "GB", "RU", "AU", "BR", "NZ", "US", "ES", "PT", "IT", "DE"]
intCountry = 0
checkBaseline = False


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

    def countdownFunction(self, canvas, countDown, isBaseline):
        while countDown >0:
            self.config(cursor="none")
            canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
            canvas.create_text(200, 200, text="0 : " + str(countDown), font=('Arial Bold', 56),fill="black", justify="center")
            backend_analysis.dataGathering()
            self.update()
            time.sleep(1)
            countDown-= 1
            print(countDown)
        if isBaseline == True:
            baseLine = backend_analysis.getBaseLine(countryID[intCountry])
            print(baseLine)
        else:
            appData = backend_analysis.getApp(countryID[intCountry])
            print(appData)
   
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

    def getContinuousData(self,canvas,values,powerBreakdownImage):
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
        isRunning = True
        totalCarbon = 0
        carbonUnits = "mgCO₂eq"
        introDisplay = 0        # Cycles through each datapoint giving info
        cycleChange = 0
        while run:
            
        

            # self.update_idletasks()
            # self.update()
            data = backend_analysis.dataAnalysis(2, countryID[intCountry])
            # self.update()
            watt = data[0]
            # self.update()
            # Note that data[1] is kgCO2eq/Wh
            print(data[1])
            if totalCarbon > 1000 :
                carbonUnits = "gCO₂eq"
                totalCarbon = totalCarbon / 1000
            if carbonUnits == "gCO₂eq" :
                carbon = (data[1]/60/60)*1000
            else :
                carbon = (data[1]/60/60)*1000*1000
            totalCarbon = totalCarbon + carbon
            if (peakWatts<data[0]):
                peakWatts = data[0]
            # self.update()
            # self.update()

            if introDisplay != 7 :
                cycleChange= cycleChange + 1
                if cycleChange > 10 :
                    cycleChange = 0
                    introDisplay = introDisplay + 1

            canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
            if introDisplay == 2 :
                canvas.create_text(200, 155, text = "Power Use - " + str(round(watt, 2)) + " W", font=('Arial', 18), fill='#93A78A', justify='center')
            else :
                canvas.create_text(200, 160, text = str(round(watt, 2)) + " W", font=('Arial', 18), fill='#93A78A', justify='center')

            if introDisplay == 4 :
                canvas.create_text(200, 203, text="Carbon Produced Since Start", font=('Arial Bold', 19), fill='#93A78A', justify="center")
            else :
                canvas.create_text(200, 200, text=str(round(totalCarbon, 2)) + " " + carbonUnits, font=('Arial Bold', 32), fill='#93A78A', justify="center")

            # self.update()
            if introDisplay == 6 :
                canvas.create_text(200, 257, text = "CO₂ Emission Factor -\n" + str(round(data[1]*1000, 2)) + " gCO₂eq/Wh", font=('Arial', 18), fill='#93A78A', justify="center")
            else :
                canvas.create_text(200, 250, text = str(round(data[1]*1000, 2)) + " gCO₂eq/Wh", font=('Arial', 18), fill='#93A78A', justify="center")
            
            # self.update()
            canvas.create_arc(5, 5, 395, 395, fill = '#93A78A',outline='#93A78A', style=tk.ARC, width=6, start=315, extent="270")
            #arc is calculated by the current power against the peak watt
            # self.update()

            ###
            
            #       peakArc has no value!

            ### 

            peakArc = round(270-((0.5)*270))
            if (peakArc>270):
                peakArc = 270
            canvas.create_arc(5, 5, 395, 395, fill = "white",outline="white", style=tk.ARC, width=8, start=315, extent=peakArc)
            carbonImage = tk.PhotoImage(file='App/Carbon.png')
            carbonImage = carbonImage.subsample(4)
            canvas.image = carbonImage
            canvas.create_image(200,370,anchor=tk.S,image=carbonImage)
            canvas.update()
            # self.update()
            values.create_image(200,50,image=powerBreakdownImage)
            if data[2] == 0:
                values.create_text(95,65,text = "N/A",font =('Arial Light', 12),fill="black", justify="left")
            else:
                values.create_text(105,65,text = str(round(data[2], 2)) + " W",font =('Arial Light', 10),fill="black", justify="left")
            # self.update()
            values.create_text(105,33,text = str(round(data[3], 2)) + " W",font =('Arial Light', 10),fill="black", justify="left")
            values.create_text(285,33,text = str(round(data[4], 2)) + " W",font =('Arial Light', 10),fill="black", justify="left")
            values.create_text(295,67,text = str(round((data[2]+data[3]+data[4]), 2)) + " W",font =('Arial Bold', 10),fill="black", justify="left")
            self.update()
        isRunning = False
    def stop(self):
        global run
        run = False


    def stop(self):
        global run
        run = False
    
    def stopRun(controller):
        global run
        run = False
        controller.show_frame(HomePage)
    

    def baselineCountdown(self, canvas, titleCanvas):
        global checkBaseline
        checkBaseline = True
        countDown = 10
        titleCanvas.create_rectangle(0,0,500,700, fill=backgroundColour, outline=backgroundColour)
        titleCanvas.create_text(130, 50, text="Measuring ...",font=('Arial Bold', 32),fill="black", justify="center")
        titleCanvas.create_text(200, 100, text="Please wait while we measure the idle power use\nof your device. Please ensure that you keep all   \nother apps closed until this test completes.     ",font=('Arial Light', 15),fill="black", justify="center")
        self.update()

        self.countdownFunction(canvas, countDown, True)
        self.config(cursor="")
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_text(200, 200, text="Open App then press Test App",font=('Arial Bold', 22),fill="black", justify="center")
        

    def measureApp(controller):
        global checkBaseline
        if checkBaseline:
            controller.show_frame(AppTesting)

        
    def startCountdown(canvas):
        print("timer")

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        backgroundColour = '#DAEFD2'
        tk.Frame.__init__(self, parent, background=backgroundColour)

        titleLabel = ttk.Label(self, text="Sustainable Software",style= 'Test.TLabel',font=('Arial Bold', 28))

        overallImage = tk.PhotoImage(file='App/OverallUsage.png')
        overallImage = overallImage.subsample(4)
        overallButton = tk.Button(self,text="Continuous Usage", image = overallImage, height = 148, width = 382, borderwidth = 0, 
                                 command = lambda : controller.show_frame(ContinuousPowerUsagePage))
        overallButton.image = overallImage

        singleImage = tk.PhotoImage(file='App/SingleApp.png')
        singleImage = singleImage.subsample(4)
        singleButton = tk.Button(self,text="Individual Usage", image = singleImage, height = 148, width = 382, borderwidth = 0, 
                                 command = lambda : controller.show_frame(IndividualMeasurmentPage))
        singleButton.image = singleImage

        bannerImage = tk.PhotoImage(file='App/TrinityCisco.png')
        bannerImage = bannerImage.subsample(4)
        bannerLabel = ttk.Label(self, image=bannerImage, border=0)
        bannerLabel.image = bannerImage

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsStart(controller))
        #command = lambda : controller.navToSettings())
        settingsButton.image = settingsImage
        
        titleLabel.grid(row = 0, column = 0, sticky = tk.SE, padx = (95,15), pady = (150,10))
        bannerLabel.place(x=550,y=140)
        overallButton.grid(row = 1, column = 0, sticky= tk.NE, padx = 10, pady = 0)
        singleButton.grid(row = 1, column = 1, sticky= tk.NW, padx = 10, pady = 0)
        settingsButton.place(x=875, y=500)
  
        # User feedback button - brings user to another screen to give feedback
        feedbackImage = tk.PhotoImage(file='App/Feedback.png')
        feedbackImage = feedbackImage.subsample(3)
        feedbackButton = tk.Button(self, text="Give Feedback", image=feedbackImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.show_frame(FeedbackPage))
        feedbackButton.place(x=750, y=500)
        feedbackButton.image = feedbackImage
  

class ContinuousPowerUsagePage(tk.Frame):
     
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,background=backgroundColour)

        stopImage = tk.PhotoImage(file='App/Stop.png')
        stopImage = stopImage.subsample(2)
        startImage = tk.PhotoImage(file='App/Start.png')
        startImage = startImage.subsample(2)

        def toggleButtonTest(toggleButton, controller, canvas, values, powerBreakdownImage):
            if toggleButton["text"] == "Running":
                toggleButton.configure(text="Not Running")
                toggleButton["image"] = startImage
                
                controller.stop()
            else:
                toggleButton.configure(text="Running")
                toggleButton["image"] = stopImage
                
                controller.getContinuousData(canvas,values,powerBreakdownImage)

        durationLabel = tk.Label(self, text="Measuring Live Data" , font=('Arial Light', 18), bg=backgroundColour, fg="black")
        titleLabel = tk.Label(self, text="Overall Power Usage", font=('Arial Bold', 32), bg=backgroundColour, fg="black")

        backImage = tk.PhotoImage(file='App/Return.png')
        backImage = backImage.subsample(2)
        backButton = tk.Button(self, image=backImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.show_frame(HomePage))
        backButton.image = backImage

        startImage = tk.PhotoImage(file='App/Start.png')
        startImage = startImage.subsample(2)
        toggleButton = tk.Button(self, text="Start", image=startImage, height = 150, width = 150, borderwidth=0,command = lambda : toggleButtonTest(toggleButton, controller, canvas, values, powerBreakdownImage))
        
        



        graphImage = tk.PhotoImage(file='App/Graph.png')
        graphImage = graphImage.subsample(2)
        graphButton = tk.Button(self, text="View Graph", image=graphImage, height = 150, width = 150, borderwidth=0,command = lambda : controller.graphToDisplay(data))
        graphButton.image = graphImage

        powerBreakdownImage = tk.PhotoImage(file='App/PowerBreakdown.png')
        powerBreakdownImage = powerBreakdownImage.subsample(2)
        values = tk.Canvas(self, background=backgroundColour,height=100, width=250, highlightthickness=0)
        # values.create_image(200,50,image=powerBreakdownImage)
        # values.create_text(295,67,text = "Start Test",font =('Arial Bold', 10),fill="black", justify="left")

        # settingsImage = tk.PhotoImage(file='App/images/Settings.png')
        # settingsImage = settingsImage.subsample(3)
        # settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.settingsPage1(controller))

        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=6, start=315, extent="270")
        canvas.create_text(200, 182, text="CARBON", font=('Arial', 22), fill='#A3B59C', justify="center")
        carbonImage = tk.PhotoImage(file='App/Carbon.png')
        carbonImage = carbonImage.subsample(4)
        canvas.image = carbonImage
        canvas.create_image(200,240,anchor=tk.S,image=carbonImage)
        canvas.update()

        # settingsButton.image = settingsImage
        
        durationLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
        titleLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 40, pady = 0)
        # settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        backButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        toggleButton.grid(row = 1, column = 0,sticky = tk.SE, padx = 30, pady = (30,50))
        graphButton.grid(row = 1, column = 1,sticky = tk.SW, pady = (30,50))
        values.place(x=75,y=370, width=400, height=100)
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
  
  
class IndividualMeasurmentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Test.TLabel', background= backgroundColour)

        # startCountdown()

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
        appTestButton = tk.Button(self,text="Start", image = appTestImage, height = 150, width = 150, borderwidth = 0, command= lambda : controller.measureApp())
        appTestButton.image = appTestImage

        returnImage = tk.PhotoImage(file='App/Return.png')
        returnImage = returnImage.subsample(2)
        returnButton = tk.Button(self, text ="Return",image=returnImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.show_frame(HomePage))
        returnButton.image = returnImage

        titleCanvas = tk.Canvas(self, background=backgroundColour, height=200, width=400, highlightthickness=0)
        titleLabel = tk.Label(self, background=backgroundColour, text="App Power Usage",font=('Arial Bold', 32))
        infoLabel = tk.Label(self,background=backgroundColour, text="Measure the idle energy use of your device with the\nmeasure baseline function while no applications are\nopen and then test the app for statistics.", font=('Arial Light', 15))


        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=6, start=315, extent="270")
        carbonImage = tk.PhotoImage(file='App/Carbon.png')
        carbonImage = carbonImage.subsample(6)
        canvas.image = carbonImage
        canvas.create_image(200,350,anchor=tk.S,image=carbonImage)
        #canvas.create_text(200, 200, text=countdownDisplay, font=('Arial Bold', 40), fill='#DAEFD2', justify="center")
        canvas.update()

          
        infoLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = (40,0), pady = 0)
        titleLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
        baselineButton.grid(row = 2, column = 0, sticky = tk.E, padx = (40,20), pady = 2)
        appTestButton.grid(row = 2, column = 1, sticky = tk.W, padx = (20,0), pady = 2)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        returnButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)

class IndividualResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsAppTestHome(controller))
        settingsButton.image = settingsImage

        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        titleLabel = ttk.Label(self, text="Results",style= 'Test.TLabel',font=('Arial Bold', 32), padding=(0,22,0,0))

        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=6, start=315, extent="270")
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")

        carbonImage = tk.PhotoImage(file='App/Carbon.png')
        carbonImage = carbonImage.subsample(6)
        canvas.image = carbonImage
        canvas.create_image(200,350,anchor=tk.S,image=carbonImage)
        
        titleLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)


class AppTesting(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, background=backgroundColour)
        #countdownDisplay = "0:00"
        countDown = 10

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsAppTestHome(controller))
        settingsButton.image = settingsImage

        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        titleLabel = ttk.Label(self, text="Measuring...",style= 'Test.TLabel',font=('Arial Bold', 32), padding=(0,22,0,0))
        infoLabel = ttk.Label(self, text="Please wait while we measure the idle power use of\nyour device. Please ensure that you keep all other\napps closed until this test completes.", font=('Arial Light', 15), style= 'Test.TLabel')

        ##stopImage = tk.PhotoImage(file='App/Stop.png')
        ##stopImage = stopImage.subsample(2)
        ##stopButton = tk.Button(self,text="Start", image = stopImage, height = 150, width = 150, borderwidth = 0, 
        ##                         command = lambda : controller.show_frame(IndividualResultsPage))
        ##stopButton.image = stopImage

        startImage = tk.PhotoImage(file='App/CUStart.png')
        startImage = startImage.subsample(2)
        startButton = tk.Button(self,text="Start", image = startImage, height = 150, width = 150, borderwidth = 0, 
                                 command = lambda : controller.countdownFunction(canvas, countDown, False))
        startButton.image = startImage

        returnImage = tk.PhotoImage(file='App/Return.png')
        returnImage = returnImage.subsample(2)
        returnButton = tk.Button(self, text ="Return",image=returnImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.show_frame(IndividualMeasurmentPage))
        returnButton.image = returnImage

        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=6, start=315, extent="270")
        
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")

        carbonImage = tk.PhotoImage(file='App/Carbon.png')
        carbonImage = carbonImage.subsample(6)
        canvas.image = carbonImage
        canvas.create_image(200,350,anchor=tk.S,image=carbonImage)
        #canvas.create_text(200, 200, text=countdownDisplay, font=('Arial Bold', 40), fill='#DAEFD2', justify="center")

        #infoLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = (40,0), pady = 0)
        #titleLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
        
        startButton.grid(row = 2, column = 0, sticky = tk.E, padx = (40,20), pady = 2)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
        returnButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
    

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)

        def changeRegion(i,buttonText):
            countryLabel["text"] = buttonText
            countryLabel.update
            controller.updateCountry(i)

        returnImage = tk.PhotoImage(file='App/Return.png')
        returnImage = returnImage.subsample(2)
        returnButton = tk.Button(self, text ="Return",image=returnImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.show_frame(previousScreen))      
        returnButton.image = returnImage  
        
        currentLabel = tk.Label(self, text="Current Country : ", font=('Arial Bold', 24),background=backgroundColour, foreground="black")
        countryLabel = tk.Label(self, text="Ireland", font=('Arial Light', 24),background=backgroundColour, foreground="grey")

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

        currentLabel.grid(row = 0, column = 1)
        countryLabel.grid(row = 0, column = 1, columnspan=3)
        irlButton.grid(row = 1, column = 0,sticky=tk.NE, padx = 50, pady = 20, )
        fraButton.grid(row = 1, column = 1, sticky=tk.N,padx = 50, pady = 20)
        ukButton.grid(row = 1, column = 2,sticky=tk.N, padx = 50, pady = 20)
        rusButton.grid(row = 1, column = 3,sticky=tk.NW, padx = 30, pady = 20)
        ausButton.grid(row = 2, column = 0,sticky=tk.NS, padx = 50, pady = 20)
        braButton.grid(row = 2, column = 1,sticky=tk.NS, padx = 50, pady = 20)
        nzButton.grid(row = 2, column = 2,sticky=tk.NS, padx = 50, pady = 20)
        spaButton.grid(row = 2, column = 3,sticky=tk.NW, padx = 30, pady = 20)
        porButton.grid(row = 3, column = 0, padx = 50, pady = 20)
        itaButton.grid(row = 3, column = 1, padx = 50, pady = 20)
        gerButton.grid(row = 3, column = 2,padx = 30, pady = 20)

        returnButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)

class FeedbackPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,background=backgroundColour)
        returnButton = tk.Button(self, text ="Return",command = lambda : controller.show_frame(HomePage))
        returnButton.pack(side='top', anchor='nw')
        
        # Function to send form data
        def send_form_data():
            # Get input values
            name = name_entry.get()
            email = email_entry.get()
            message = message_entry.get("1.0", "end-1c")

            # Create dictionary with form data
            form_data = {
                "name": name,
                "email": email,
                "message": message
            }

            # Send POST request to Getform API
            response = requests.post("https://getform.io/f/da461dc3-8929-49bc-977b-03a9f84201a9", data=form_data)

            # Show success message
            success_label.config(text="Message sent successfully!")
        # Create input fields
        title_label = tk.Label(self, text="Give feedback on potential inaccuracies you found in the app!")
        name_label = tk.Label(self, text="Name:")
        name_entry = tk.Entry(self)

        email_label = tk.Label(self, text="Email:")
        email_entry = tk.Entry(self)

        message_label = tk.Label(self, text="Message:")
        message_entry = tk.Text(self)

        # Create submit button
        submit_button = tk.Button(self, text="Send Message", command=send_form_data)

        # Create success label
        success_label = tk.Label(self, fg="green")

        title_label.pack()
        name_label.pack()
        name_entry.pack()

        email_label.pack()
        email_entry.pack()

        message_label.pack()
        message_entry.pack()

        submit_button.pack(pady=10)
        success_label.pack()      

        

app = tkinterApp()
app.resizable(False,False)
app.title("Sustainable Software")
app.mainloop()