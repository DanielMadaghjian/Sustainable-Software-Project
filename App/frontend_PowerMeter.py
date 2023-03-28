# 'python3 -m pip install tkinter'
# 'python3 -m pip install matplotlib'

import tkinter as tk
from tkinter import ttk
import backend_analysis
import matplotlib.pyplot as plt

backgroundColour = '#DAEFD2'
previousScreen = tk.Frame

country = ["Ireland", "France", "Great Britain", "Russia", "Australia", "Brazil", "New Zealand", "United States", "Spain", "Portugal", "Italy","Germany"]
countryID = ["IE", "FR", "GB", "RU", "AU", "BR", "NZ", "US", "ES", "PT", "IT", "DE"]
intCountry = 0

global isRunning
isRunning = False

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {} 

        for F in (StartPage, Page1, Page2, SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
  
    def show_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()

    

    def updateCountry(self, newCountry):
        global intCountry
        intCountry = newCountry
    
    def startTest(self,durationInput,canvas,values,currentCountry):
    ##Calling the analysis function
        backendData = backend_analysis.dataAnalysis(durationInput, countryID[currentCountry])
        wattInput = backendData[0]
        carbonEmissions = (((backendData[1])/60)/12)*1000000
        print(wattInput)
        print(carbonEmissions)
        canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        canvas.create_text(200, 200, text=str(round(wattInput, 2)) + " W", font=('Arial Bold', 40+16), fill="black", justify="center")
        canvas.create_text(200, 245, text=str(round(carbonEmissions, 2)) + " mgCO₂eq", font=('Arial Light', 18), fill="gray", justify="center")
        canvas.create_text(200, 160, text="CARBON", font=('Arial Light', 18), fill="gray", justify="center")
        canvas.create_arc(5, 5, 395, 395, outline='#93A78A', style=tk.ARC, width=6, start=315, extent="270")
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
        
        
    def settingsStart(self,controller):
        global previousScreen
        previousScreen = StartPage
        controller.show_frame(SettingsPage)

    def settingsPage1(self,controller):
        global previousScreen
        previousScreen = Page1
        controller.show_frame(SettingsPage)

    def settingsPage2(self,controller):
        global previousScreen
        previousScreen = Page2
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
            carbonImage = tk.PhotoImage(file='App/images/Carbon.png')
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

    # def start(self):
    #     global run
    #     run = True
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        backgroundColour = '#DAEFD2'
        tk.Frame.__init__(self, parent, background=backgroundColour)

        titleLabel = ttk.Label(self, text="Sustainable Software",style= 'Test.TLabel',font=('Arial Bold', 28))

        overallImage = tk.PhotoImage(file='App/images/OverallUsage.png')
        overallImage = overallImage.subsample(4)
        overallButton = tk.Button(self,text="Continuous Usage", image = overallImage, height = 148, width = 382, borderwidth = 0, 
                                 command = lambda : controller.show_frame(Page1))
        overallButton.image = overallImage

        singleImage = tk.PhotoImage(file='App/images/SingleApp.png')
        singleImage = singleImage.subsample(4)
        singleButton = tk.Button(self,text="Individual Usage", image = singleImage, height = 148, width = 382, borderwidth = 0, 
                                 command = lambda : controller.show_frame(Page2))
        singleButton.image = singleImage

        bannerImage = tk.PhotoImage(file='App/images/TrinityCisco.png')
        bannerImage = bannerImage.subsample(4)
        bannerLabel = ttk.Label(self, image=bannerImage, border=0)
        bannerLabel.image = bannerImage

        settingsImage = tk.PhotoImage(file='App/images/Settings.png')
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
  

class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,background=backgroundColour)

        stopImage = tk.PhotoImage(file='App/images/Stop.png')
        stopImage = stopImage.subsample(2)
        startImage = tk.PhotoImage(file='App/images/Start.png')
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

        backImage = tk.PhotoImage(file='App/images/Return.png')
        backImage = backImage.subsample(2)
        backButton = tk.Button(self, image=backImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.show_frame(StartPage))
        backButton.image = backImage

        startImage = tk.PhotoImage(file='App/images/Start.png')
        startImage = startImage.subsample(2)
        toggleButton = tk.Button(self, text="Start", image=startImage, height = 150, width = 150, borderwidth=0,command = lambda : toggleButtonTest(toggleButton, controller, canvas, values, powerBreakdownImage))
        
        



        graphImage = tk.PhotoImage(file='App/images/Graph.png')
        graphImage = graphImage.subsample(2)
        graphButton = tk.Button(self, text="View Graph", image=graphImage, height = 150, width = 150, borderwidth=0,command = lambda : controller.graphToDisplay(data))
        graphButton.image = graphImage

        powerBreakdownImage = tk.PhotoImage(file='App/images/PowerBreakdown.png')
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
        carbonImage = tk.PhotoImage(file='App/images/Carbon.png')
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
  
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Test.TLabel', background= backgroundColour)

        titleLabel = ttk.Label(self, text="Power Consumption",style= 'Test.TLabel',font=('Arial Bold', 32))
        durationLabel = ttk.Label(self, text="5 SECOND", font=('Arial Light', 18), style= 'Test.TLabel')

        startImage = tk.PhotoImage(file='App/images/Test.png')
        startImage = startImage.subsample(2)
        startButton = tk.Button(self,text="Start", image = startImage, height = 150, width = 150, borderwidth = 0, 
                                 command = lambda : controller.startTest(5,canvas,values,intCountry))
        startButton.image = startImage

        settingsImage = tk.PhotoImage(file='App/images/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsPage2(controller))
        #command = lambda : controller.navToSettings())
        settingsButton.image = settingsImage

        backImage = tk.PhotoImage(file='App/images/Return.png')
        backImage = backImage.subsample(2)
        backButton = tk.Button(self, image=backImage, height = 50, width = 100, borderwidth = 0,
                                   command = lambda : controller.show_frame(StartPage))
        backButton.image = backImage

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
        backButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
        values.grid(row = 2, column = 1, sticky = tk.W, padx = 0, pady = 2)
        
class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)

        def changeRegion(i,buttonText):
            countryLabel["text"] = buttonText
            countryLabel.update
            controller.updateCountry(i)

        backImage = tk.PhotoImage(file='App/images/Return.png')
        backImage = backImage.subsample(2)
        backButton = tk.Button(self, image=backImage, height = 50, width = 100, borderwidth = 0,
                                   command = lambda : controller.show_frame(StartPage))
        backButton.image = backImage

        currentLabel = ttk.Label(self, text="Current Country: ", font=('Arial Light', 24), style= 'Test.TLabel')
        countryLabel = ttk.Label(self, text="Ireland", font=('Arial Light', 24), style= 'Test.TLabel')
        selectLabel = ttk.Label(self, text="Select a country: ",font=('Arial Light', 18), style= 'Test.TLabel')

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

        #currentLabel.grid(row = 0, column = 2, sticky=tk.NW, padx = 5, pady = 5)
        #countryLabel.grid(row = 0, column = 3, sticky=tk.NW, padx = 5, pady = 5)
        selectLabel.grid(row = 1, column = 0, stick = tk.NW, padx = 5, pady = 30)

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

        backButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        

app = tkinterApp()
app.resizable(False,False)
app.title("ecoCheck")
app.iconphoto(False,tk.PhotoImage(file='App/images/ecoCheck.png')) #ecoCheck.png?
app.mainloop()
