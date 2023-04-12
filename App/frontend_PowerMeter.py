from tkinter import *
import tkinter as tk
from tkinter import ttk
import backend_analysis
import matplotlib.pyplot as plt
import requests
import time

backgroundColour = '#DAEFD2'
country = ["Ireland", "France", "Great Britain", "Russia", "Australia", "Brazil", "New Zealand", "United States", "Spain", "Portugal", "Italy","Germany"]
countryID = ["IE", "FR", "GB", "RU", "AU", "BR", "NZ", "US", "ES", "PT", "IT", "DE"]
previousScreen = tk.Frame
intCountry = 0
checkBaseline = False


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
        self.geometry("1000x560")
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        for F in (StartPage, Page1, Page2, SettingsPage, FeedbackPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def showResults(self, canvas, baseLine) :
        print("Showing Results")
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        headerImage = tk.PhotoImage(file='App/images/Header.png')
        canvas.image = headerImage
        global baseValues
        global appValues
        baseValuesGpu = round(baseValues[2], 2)
        appValuesGpu = round(appValues[2], 2)
        if baseValues[2] == 0 :
            baseValuesGpu = "N/A"
            appValuesGpu  = "N/A"
            gpuInc = "N/A"
        else:
            baseValuesGpu = str(baseValuesGpu) + " W"
            if appValuesGpu >= 0 :
                appValuesGpu = "+" + str(appValuesGpu) + " W"
            else :
                appValuesGpu = str(appValuesGpu) + " W"
            gpuInc = round((appValues[2]/baseValues[2])*100,1) 
        canvas.create_image(200,165,anchor=tk.S,image=headerImage)
        canvas.create_text(75, 170, text="CPU:", font=('Arial Bold', 12), fill="black", justify=LEFT)
        canvas.create_text(75, 205, text="GPU:", font=('Arial Bold', 12), fill="black", justify=LEFT)
        canvas.create_text(75, 240, text="RAM:", font=('Arial Bold', 12), fill="black", justify=LEFT)
        canvas.create_text(75, 275, text="Total:", font=('Arial Bold', 12), fill="black", justify=LEFT)
        canvas.create_text(155, 170, text=str(round(baseValues[3], 2))+" W", font=('Arial', 12), fill="black")
        canvas.create_text(155, 205, text=baseValuesGpu, font=('Arial', 12), fill="black")
        canvas.create_text(155, 240, text=str(round(baseValues[4], 2))+" W", font=('Arial', 12), fill="black")
        canvas.create_text(155, 275, text=str(round(baseValues[2]+baseValues[3]+baseValues[4], 2)) + " W", font=('Arial Bold', 12), fill="black")
        appValuesCpu = round(appValues[3], 2)
        if appValuesCpu >= 0 :
            appValuesCpu = "+" + str(appValuesCpu) + " W"
        else :
            appValuesCpu = str(appValuesCpu) + " W"
        appValuesRam = round(appValues[4], 2)
        if appValuesRam >= 0 :
            appValuesRam = "+" + str(appValuesRam) + " W"
        else :
            appValuesRam = str(appValuesRam) + " W"
        canvas.create_text(234, 170, text=appValuesCpu, font=('Arial', 12), fill="black")
        canvas.create_text(234, 205, text=appValuesGpu, font=('Arial', 12), fill="black")
        canvas.create_text(234, 240, text=appValuesRam, font=('Arial', 12), fill="black")
        canvas.create_text(234, 275, text=str(round(baseValues[2]+baseValues[3]+baseValues[4]+appValues[2]+appValues[3]+appValues[4],2)) + " W", font=('Arial Bold', 12), fill="black")
        cpuInc = round((appValues[3]/baseValues[3])*100,1)
        ramInc = round((appValues[4]/baseValues[4])*100,1)
        if appValues[3] <= 0 :
            cpuInc = "Negligible"
        else :
            cpuInc = "+" + str(cpuInc) + "%"
        if gpuInc == "N/A" :
            gpuInc = "N/A"
        elif appValues[2] <= 0 :
            gpuInc = "Negligible"
        else :
            gpuInc = "+" + str(gpuInc) + "%"
        if appValues[4] <= 0 :
            ramInc = "Negligible"
        else :
            ramInc = "+" + str(ramInc) + "%"
        canvas.create_text(320, 170, text=cpuInc, font=('Arial', 12), fill="#93A78A")
        canvas.create_text(320, 205, text=gpuInc, font=('Arial', 12), fill="#93A78A")
        canvas.create_text(320, 240, text=ramInc, font=('Arial', 12), fill="#93A78A")
        currCarb = backend_analysis.getCarbon(countryID[intCountry])
        if currCarb == "API CONNECTION ERROR" :
            currCarb = 0
        else :
            currCarb = currCarb*1000000
        canvas.create_text(200, 320, text="Using "+ str(round(((baseValues[2]+baseValues[3]+baseValues[4]+appValues[2]+appValues[3]+appValues[4])*currCarb)/1000,2)) + " gCO₂eq/hr\n" + str(round(currCarb,2)) + " mgCO₂eq/Wh", font=('Arial Bold', 12), fill="#93A78A", justify="center")
        carbonImage = tk.PhotoImage(file='App/images/Carbon.png')
        carbonImage = carbonImage.subsample(4)
        canvas.create_image(200,370,anchor=tk.S,image=carbonImage)

    def updateCountry(self, newCountry):
        global intCountry
        intCountry = newCountry

    def countdownFunction(self, canvas, countDown, isBaseline):
        carbonImage = tk.PhotoImage(file='App/images/Carbon.png')
        carbonImage = carbonImage.subsample(4)
        canvas.image = carbonImage
        while countDown >0:
            self.config(cursor="none")
            canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
            canvas.create_text(200, 200, text="0:" + str(countDown).zfill(2), font=('Arial Bold', 56),fill='#93A78A', justify="center")
            canvas.create_image(200,370,anchor=tk.S,image=carbonImage)
            canvas.create_arc(5, 5, 395, 395, fill = '#93A78A',outline='#93A78A', style=tk.ARC, width=6, start=315, extent="270")
            if isBaseline :
                timeArc = round(270-((1-0.1*countDown)*270))
            else :
                timeArc = round(270-((0.1*countDown)*270))
            if (timeArc>270):
                timeArc = 270
            canvas.create_arc(5, 5, 395, 395, fill = "white",outline="white", style=tk.ARC, width=8, start=315, extent=timeArc)
            canvas.update()
            backend_analysis.dataGathering()
            self.update()
            time.sleep(1)
            countDown-= 1
            print(countDown)
        if isBaseline == True:
            baseLine = backend_analysis.getBaseLine(countryID[intCountry])
            return baseLine
        else:
            appData, baseLineData, oData = backend_analysis.getApp(countryID[intCountry])
            return appData

    def settingsStart(self,controller):
        global previousScreen
        previousScreen = StartPage
        controller.show_frame(SettingsPage)

    def settingsContinuousPowerPage(self,controller):
        global previousScreen
        previousScreen = ContinuousPowerPage
        controller.show_frame(SettingsPage)

    def settingsIndividualPowerPage(self,controller):
        global previousScreen
        previousScreen = IndividualPowerPage
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
        totalCarbon = 0
        carbonUnits = "mgCO₂eq"
        while run:
            data = backend_analysis.dataAnalysis(2, countryID[intCountry])
            if isinstance(data[1], float):
                if totalCarbon > 1000 :
                    carbonUnits = "gCO₂eq"
                    totalCarbon = totalCarbon / 1000
                if carbonUnits == "gCO₂eq" :
                    carbon = (data[1]/60/60)*1000
                else :
                    carbon = (data[1]/60/60)*1000*1000
                totalCarbon = totalCarbon + carbon
                carbonText = str(round(data[1]*1000000, 2))
            else:
                totalCarbon = 0
                carbonText = "Can't Connect To API"
            canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
            canvas.create_text(200, 160, text = str(round(data[0], 2)) + " W", font=('Arial', 18), fill='#93A78A', justify='center')
            canvas.create_text(200, 200, text=str(round(totalCarbon, 2)) + " " + carbonUnits, font=('Arial Bold', 32), fill='#93A78A', justify="center")
            canvas.create_text(200, 250, text = carbonText + " mgCO₂eq/Wh", font=('Arial', 18), fill='#93A78A', justify="center")
            canvas.create_arc(5, 5, 395, 395, fill = 'white',outline='white', style=tk.ARC, width=6, start=315, extent="270")
            carbonImage = tk.PhotoImage(file='App/images/Carbon.png')
            carbonImage = carbonImage.subsample(4)
            canvas.image = carbonImage
            canvas.create_image(200,370,anchor=tk.S,image=carbonImage)
            canvas.update()
            values.create_image(200,50,image=powerBreakdownImage)
            if data[2] == 0:
                values.create_text(95,65,text = "N/A",font =('Arial Light', 12),fill="black", justify="left")
            else:
                values.create_text(105,65,text = str(round(data[2], 2)) + " W",font =('Arial Light', 10),fill="black", justify="left")
            values.create_text(105,33,text = str(round(data[3], 2)) + " W",font =('Arial Light', 10),fill="black", justify="left")
            values.create_text(285,33,text = str(round(data[4], 2)) + " W",font =('Arial Light', 10),fill="black", justify="left")
            values.create_text(295,67,text = str(round((data[2]+data[3]+data[4]), 2)) + " W",font =('Arial Bold', 10),fill="black", justify="left")
            self.update()
    def stop(self):
        global run
        run = False
    def stop(self):
        global run
        run = False
    
    def stopRun(controller):
        global run
        run = False
        controller.show_frame(StartPage)
    

    def baselineCountdown(self, canvas, titleCanvas, isApp, controller):
        countDown = 10
        global checkBaseline
        global baseValues
        global appValues
        if isApp:
            
            checkBaseline = True
            titleCanvas.create_rectangle(0,0,500,700, fill=backgroundColour, outline=backgroundColour)
            titleCanvas.create_text(130, 50, text="Measuring ...",font=('Arial Bold', 32),fill="black", justify="center")
            titleCanvas.create_text(200, 100, text="Please wait while we measure the idle power use\nof your device. Please ensure that you keep all   \nother apps closed until this test completes.     ",font=('Arial Light', 15),fill="black", justify="center")
            self.update()
            baseLine = self.countdownFunction(canvas, countDown, True)
            baseValues = baseLine
            self.config(cursor="")
            canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
            canvas.create_arc(5, 5, 395, 395, outline="#93A78A", style=tk.ARC, width=6, start=315, extent="270")
            canvas.create_text(200, 200, text="Baseline\nReady",font=('Arial Bold', 22),fill="#93A78A", justify="center")
            carbonImage = tk.PhotoImage(file='App/images/Carbon.png')
            carbonImage = carbonImage.subsample(4)
            canvas.image = carbonImage
            canvas.create_image(200,370,anchor=tk.S,image=carbonImage)
            canvas.update()
        elif checkBaseline:
            self.update()
            baseLine = self.countdownFunction(canvas, countDown, False)
            appValues = baseLine
            self.config(cursor="")
            canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
            canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=6, start=315, extent="270")
            carbonImage = tk.PhotoImage(file='App/images/Carbon.png')
            carbonImage = carbonImage.subsample(4)
            canvas.image = carbonImage
            canvas.create_image(200,370,anchor=tk.S,image=carbonImage)
            controller.showResults(canvas, baseLine)

    def measureApp(controller):
        global checkBaseline
        if checkBaseline:
            controller.show_frame(AppTesting)

    def startCountdown(canvas):
        print("timer")

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        backgroundColour = '#DAEFD2'
        tk.Frame.__init__(self, parent, background=backgroundColour) # This is the UI design of the page that shows on launch
        titleLabel = ttk.Label(self, text="Sustainable Software",style= 'Test.TLabel',font=('Arial Bold', 28))
        overallImage = tk.PhotoImage(file='App/images/OverallUsage.png')
        overallImage = overallImage.subsample(4)
        overallButton = tk.Button(self,text="Continuous Usage", image = overallImage, height = 148, width = 382, borderwidth = 0, command = lambda : controller.show_frame(Page1))
        overallButton.image = overallImage
        singleImage = tk.PhotoImage(file='App/images/SingleApp.png')
        singleImage = singleImage.subsample(4)
        singleButton = tk.Button(self,text="Individual Usage", image = singleImage, height = 148, width = 382, borderwidth = 0, command = lambda : controller.show_frame(Page2))
        singleButton.image = singleImage
        bannerImage = tk.PhotoImage(file='App/images/TrinityCisco.png')
        bannerImage = bannerImage.subsample(4)
        bannerLabel = ttk.Label(self, image=bannerImage, border=0)
        bannerLabel.image = bannerImage
        settingsImage = tk.PhotoImage(file='App/images/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.settingsStart(controller))
        settingsButton.image = settingsImage
        titleLabel.grid(row = 0, column = 0, sticky = tk.SE, padx = (95,15), pady = (150,10))
        bannerLabel.place(x=550,y=140)
        overallButton.grid(row = 1, column = 0, sticky= tk.NE, padx = 10, pady = 0)
        singleButton.grid(row = 1, column = 1, sticky= tk.NW, padx = 10, pady = 0)
        settingsButton.place(x=875, y=500)
        feedbackImage = tk.PhotoImage(file='App/images/Feedback.png') # User Feedback
        feedbackImage = feedbackImage.subsample(3)
        feedbackButton = tk.Button(self, text="Give Feedback", image=feedbackImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.show_frame(FeedbackPage))
        feedbackButton.place(x=750, y=500)
        feedbackButton.image = feedbackImage

class ContinuousPowerPage(tk.Frame):
     
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,background=backgroundColour)
<<<<<<< HEAD
        stopImage = tk.PhotoImage(file='App/images/Stop.png')
        stopImage = stopImage.subsample(2)
        startImage = tk.PhotoImage(file='App/images/Start.png')
        startImage = startImage.subsample(2)
=======

        # Function to test whether to continuously update the power consumption
>>>>>>> 128a74550403d0c8d7adddbdf0441700a8ce729b
        def toggleButtonTest(toggleButton, controller, canvas, values, powerBreakdownImage):
            if toggleButton["text"] == "Running":
                toggleButton.configure(text="Not Running")
                toggleButton["image"] = startImage
                controller.stop()
            else:
                toggleButton.configure(text="Running")
                toggleButton["image"] = stopImage
                controller.getContinuousData(canvas,values,powerBreakdownImage)

        # Function to return to homepage and stop continuously updating the power consumption
        def backToStartPage(controller):
            toggleButton.configure(text="Not Running")
            toggleButton["image"] = startImage
            controller.stop()
            controller.show_frame(StartPage)

        # Create title labels
        durationLabel = tk.Label(self, text="Measuring Live Data" , font=('Arial Light', 18), bg=backgroundColour, fg="black")
        titleLabel = tk.Label(self, text="Overall Power Usage", font=('Arial Bold', 32), bg=backgroundColour, fg="black")

        # Create return button
        backImage = tk.PhotoImage(file='App/images/Return.png')
        backImage = backImage.subsample(2)
        backButton = tk.Button(self, image=backImage, height = 50, width = 100, borderwidth = 0, command = lambda : backToStartPage(controller))
        backButton.image = backImage

        # Create start button
        startImage = tk.PhotoImage(file='App/images/Start.png')
        startImage = startImage.subsample(2)
        toggleButton = tk.Button(self, text="Start", image=startImage, height = 150, width = 150, borderwidth=0,command = lambda : toggleButtonTest(toggleButton, controller, canvas, values, powerBreakdownImage))
        toggleButton.image = startImage

        # Create graph button
        graphImage = tk.PhotoImage(file='App/images/Graph.png')
        graphImage = graphImage.subsample(2)
        graphButton = tk.Button(self, text="View Graph", image=graphImage, height = 150, width = 150, borderwidth=0,command = lambda : controller.graphToDisplay(data))
        graphButton.image = graphImage

        # Create stop image
        stopImage = tk.PhotoImage(file='App/images/Stop.png')
        stopImage = stopImage.subsample(2)

        # Create GPU, CPU and Ram display image 
        powerBreakdownImage = tk.PhotoImage(file='App/images/PowerBreakdown.png')
        powerBreakdownImage = powerBreakdownImage.subsample(2)

        # Create canvas which updates to display the wattage and carbon
        values = tk.Canvas(self, background=backgroundColour,height=100, width=250, highlightthickness=0)
        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=6, start=315, extent="270")
        canvas.create_text(200, 182, text="CARBON", font=('Arial', 22), fill='#A3B59C', justify="center")
        carbonImage = tk.PhotoImage(file='App/images/Carbon.png')
        carbonImage = carbonImage.subsample(4)
        canvas.create_image(200,240,anchor=tk.S,image=carbonImage)
        canvas.update()
        durationLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
        titleLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 40, pady = 0)
        backButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        toggleButton.grid(row = 1, column = 0,sticky = tk.SE, padx = 30, pady = (30,50))
        graphButton.grid(row = 1, column = 1,sticky = tk.SW, pady = (30,50))

        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
        values.place(x=75,y=370, width=400, height=100)
  
class IndividualPowerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)

        # This is used to create the green background theme
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Test.TLabel', background= backgroundColour)

        # Create settings button
        settingsImage = tk.PhotoImage(file='App/images/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.settingsIndividualPowerPage(controller))
        settingsButton.image = settingsImage

        # Create baseline button
        baselineImage = tk.PhotoImage(file='App/images/Baseline.png')
        baselineImage = baselineImage.subsample(2)
        baselineButton = tk.Button(self,text="Start", image = baselineImage, height = 150, width = 150, borderwidth = 0, command = lambda : controller.baselineCountdown(canvas, titleCanvas, True, controller))
        baselineButton.image = baselineImage

        # Create app test button
        appTestImage = tk.PhotoImage(file='App/images/AppTest.png')
        appTestImage = appTestImage.subsample(2)
        appTestButton = tk.Button(self,text="Start", image = appTestImage, height = 150, width = 150, borderwidth = 0, command= lambda : controller.baselineCountdown(canvas, titleCanvas, False, controller))
        appTestButton.image = appTestImage

        # Create return button
        returnImage = tk.PhotoImage(file='App/images/Return.png')
        returnImage = returnImage.subsample(2)
        returnButton = tk.Button(self, text ="Return",image=returnImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.show_frame(StartPage))
        returnButton.image = returnImage

        # Create title canvas
        titleCanvas = tk.Canvas(self, background=backgroundColour, height=200, width=400, highlightthickness=0)
        titleLabel = tk.Label(self, background=backgroundColour, text="App Power Usage",font=('Arial Bold', 32))
        infoLabel = tk.Label(self,background=backgroundColour, text="Measure the idle energy use of your device with the\nmeasure baseline function while no applications are\nopen and then test the app for statistics.", font=('Arial Light', 14), justify=LEFT)

         # Create canvas to display countdown and results
        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_text(200, 200, text="0:10", font=('Arial Bold', 56),fill='#93A78A', justify="center")
        canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=6, start=315, extent="270")
        carbonImage = tk.PhotoImage(file='App/images/Carbon.png')
        carbonImage = carbonImage.subsample(4)
        canvas.image = carbonImage
        canvas.create_image(200,370,anchor=tk.S,image=carbonImage)
        canvas.update()

        infoLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 40, pady = 0)
        titleLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = (20,0))

        baselineButton.grid(row = 2, column = 0, sticky = tk.E, padx = (40,20), pady = 2)
        appTestButton.grid(row = 2, column = 1, sticky = tk.W, padx = (20,0), pady = 2)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        returnButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)

        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)

class AppTesting(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, background=backgroundColour)
        countDown = 10

        # Create settings button
        settingsImage = tk.PhotoImage(file='App/images/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.settingsAppTestHome(controller))
        settingsButton.image = settingsImage    

        # Create start button
        startImage = tk.PhotoImage(file='App/images/AppTest.png')
        startImage = startImage.subsample(2)
        startButton = tk.Button(self,text="Start", image = startImage, height = 150, width = 150, borderwidth = 0, command = lambda : controller.countdownFunction(canvas, countDown, False))
        startButton.image = startImage

        # Create return button
        returnImage = tk.PhotoImage(file='App/images/Return.png')
        returnImage = returnImage.subsample(2)
        returnButton = tk.Button(self, text ="Return",image=returnImage, height = 50, width = 100, borderwidth = 0, command = lambda : controller.show_frame(IndividualPowerPage))
        returnButton.image = returnImage

        # Create canvas
        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=6, start=315, extent="270")
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        carbonImage = tk.PhotoImage(file='App/images/Carbon.png')
        carbonImage = carbonImage.subsample(6)
        canvas.image = carbonImage
        canvas.create_image(200,350,anchor=tk.S,image=carbonImage)
        
        startButton.grid(row = 2, column = 0, sticky = tk.E, padx = (40,20), pady = 2)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
        returnButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)

        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
    

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)

        # Funtion to update the country label
        def changeRegion(i,buttonText):
            countryLabel["text"] = buttonText
            countryLabel.update
            controller.updateCountry(i)

        # Create return button
        backImage = tk.PhotoImage(file='App/images/Return.png')
        backImage = backImage.subsample(2)
        backButton = tk.Button(self, image=backImage, height = 50, width = 100, borderwidth = 0,command = lambda : controller.show_frame(StartPage))
        backButton.image = backImage

        # Create label to display selected country 
        currentLabel = ttk.Label(self, text="Current Country: ", font=('Arial Light', 24), style= 'Test.TLabel')
        countryLabel = ttk.Label(self, text="Ireland", font=('Arial Light', 24), style= 'Test.TLabel')
        selectLabel = ttk.Label(self, text="Select a country: ",font=('Arial Light', 18), style= 'Test.TLabel')

        # Creating country buttons
        irlImage = tk.PhotoImage(file='App/images/flagIreland.png')
        irlImage = irlImage.subsample(1)
        irlButton = tk.Button(self, text ="Ireland",image = irlImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                               command = lambda : changeRegion(0, irlButton["text"]))
        irlButton.image = irlImage

        fraImage = tk.PhotoImage(file='App/images/flagFrance.png')
        fraImage = fraImage.subsample(1)
        fraButton = tk.Button(self, text ="France",image = fraImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(1,fraButton["text"]))
        fraButton.image = fraImage

        ukImage = tk.PhotoImage(file='App/images/flagUK.png')
        ukImage = ukImage.subsample(1)
        ukButton = tk.Button(self, text ="United Kingdom",image = ukImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(2,ukButton["text"]))
        ukButton.image = ukImage

        rusImage = tk.PhotoImage(file='App/images/flagRussia.png')
        rusImage = rusImage.subsample(1)
        rusButton = tk.Button(self, text ="Russia",image = rusImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(3,rusButton["text"]))
        rusButton.image = rusImage

        ausImage = tk.PhotoImage(file='App/images/flagAustralia.png')
        ausImage = ausImage.subsample(1)
        ausButton = tk.Button(self, text ="Australia",image = ausImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(4,ausButton["text"]))
        ausButton.image = ausImage

        braImage = tk.PhotoImage(file='App/images/flagBrazil.png')
        braImage = braImage.subsample(1)
        braButton = tk.Button(self, text ="Brazil",image = braImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(5,braButton["text"]))
        braButton.image = braImage

        nzImage = tk.PhotoImage(file='App/images/flagNewZealand.png')
        nzImage = nzImage.subsample(1)
        nzButton = tk.Button(self, text ="New Zealand",image = nzImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(6,nzButton["text"]))
        nzButton.image = nzImage

        spaImage = tk.PhotoImage(file='App/images/flagSpain.png')
        spaImage = spaImage.subsample(1)
        spaButton = tk.Button(self, text ="Spain",image = spaImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(7,spaButton["text"]))
        spaButton.image = spaImage

        porImage = tk.PhotoImage(file='App/images/flagPortugal.png')
        porImage = porImage.subsample(1)
        porButton = tk.Button(self, text ="Portugal",image = porImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(8,porButton["text"]))
        porButton.image = porImage

        itaImage = tk.PhotoImage(file='App/images/flagItaly.png')
        itaImage = itaImage.subsample(1)
        itaButton = tk.Button(self, text ="Italy",image = itaImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(9,itaButton["text"]))
        itaButton.image = itaImage

        gerImage = tk.PhotoImage(file='App/images/flagGermany.png')
        gerImage = gerImage.subsample(1)
        gerButton = tk.Button(self, text ="Germany",image = gerImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(10,gerButton["text"]))
        gerButton.image = gerImage

        polImage = tk.PhotoImage(file='App/images/flagPoland.png')
        polImage = polImage.subsample(1)
        polButton = tk.Button(self, text ="Poland",image = polImage, height=90, width=130, borderwidth = 0, bg = backgroundColour,
                              command = lambda : changeRegion(11,polButton["text"]))
        polButton.image = polImage

        currentLabel.place(x = 300, y = 20)
        countryLabel.place(x = 550, y = 20)
        selectLabel.grid(row = 1, column = 0, stick = tk.NW, padx = 5, pady = 30)
        backButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)

        irlButton.grid(row = 2, column = 1,sticky=tk.NW, padx = 5, pady = 5)
        fraButton.grid(row = 2, column = 2,sticky=tk.NW, padx = 5, pady = 5)
        ukButton.grid(row = 2, column = 3,sticky=tk.NW, padx = 5, pady = 5)
        rusButton.grid(row = 2, column = 4,sticky=tk.NW, padx = 5, pady = 5)
        ausButton.grid(row = 3, column = 1,sticky=tk.NW, padx = 5, pady = 5)
        braButton.grid(row = 3, column = 2,sticky=tk.NW, padx = 5, pady = 5)
        nzButton.grid(row = 3, column = 3,sticky=tk.NW, padx = 5, pady = 5)
        spaButton.grid(row = 3, column = 4,sticky=tk.NW, padx = 5, pady = 5)
        porButton.grid(row = 4, column = 1,sticky=tk.NW, padx = 5, pady = 5)
        itaButton.grid(row = 4, column = 2,sticky=tk.NW, padx = 5, pady = 5)
        gerButton.grid(row = 4, column = 3,sticky=tk.NW, padx = 5, pady = 5)
        polButton.grid(row = 4, column = 4,sticky=tk.NW, padx = 5, pady = 5)

class FeedbackPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,background=backgroundColour)
        
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

        # Create success label
        success_label = tk.Label(self, fg="green")

        returnButton = tk.Button(self, text ="Return",command = lambda : controller.show_frame(StartPage))
        submit_button = tk.Button(self, text="Send Message", command=send_form_data)

        title_label.pack()
        name_label.pack()
        name_entry.pack()

        email_label.pack()
        email_entry.pack()

        message_label.pack()
        message_entry.pack()

        submit_button.pack(pady=10)
        success_label.pack()    

        returnButton.pack(side=TOP, anchor=NW)

app = tkinterApp()
app.resizable(False,False)
app.title("ecoCheck")
app.iconphoto(False,tk.PhotoImage(file='App/images/ecoCheck.png'))
app.mainloop()
