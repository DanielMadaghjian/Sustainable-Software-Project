
# 'python3 -m pip install tkinter'
# 'python3 -m pip install matplotlib'

import tkinter as tk
from tkinter import ttk
import backend_analysis
import matplotlib.pyplot as plt

backgroundColour = '#DAEFD2'
previousScreen = tk.Frame

country = ["Ireland", "France", "Great Britain", "Russia", "Australia", "Brazil", "New Zealand", "United States", "Spain", "Portugal", "Italy","Germany","Poland"]
countryID = ["IE", "FR", "GB", "RU", "AU", "BR", "NZ", "US", "ES", "PT", "IT", "DE","PL"]
intCountry = 0

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
        canvas.create_text(200, 245, text=str(round(carbonEmissions, 2)) + " mgCO₂", font=('Arial Light', 18), fill="gray", justify="center")
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
        while run:
            self.update()
            data = backend_analysis.dataAnalysis(2, countryID[intCountry])
            self.update()
            watt = data[0]
            self.update()
            carbon = (((data[1])/60)/12)*1000000
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

        overallImage = tk.PhotoImage(file='App/overallButton.png')
        overallImage = overallImage.subsample(2)
        overallButton = tk.Button(self,text="Continuous Usage", image = overallImage, height = 100, width = 235, borderwidth = 0, 
                                 command = lambda : controller.show_frame(Page1))
        overallButton.image = overallImage

        singleImage = tk.PhotoImage(file='App/singleButton.png')
        singleImage = singleImage.subsample(2)
        singleButton = tk.Button(self,text="Individual Usage", image = singleImage, height = 100, width = 235, borderwidth = 0, 
                                 command = lambda : controller.show_frame(Page2))
        singleButton.image = singleImage

        bannerImage = tk.PhotoImage(file='App/banner.png')
        bannerImage = bannerImage.subsample(2)
        bannerLabel = ttk.Label(self, image=bannerImage, border=0)
        bannerLabel.image = bannerImage

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsStart(controller))
        #command = lambda : controller.navToSettings())
        settingsButton.image = settingsImage
        
        titleLabel.grid(row = 1, column = 1, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 50, pady = 102)
        bannerLabel.place(x=500,y=85)
        overallButton.grid(row = 2, column = 2,padx = 10, pady = 0)
        singleButton.grid(row = 2, column = 3, padx = 10, pady = 0)
        #settingsButton.grid(row = 4, column = 4, padx = 10, pady = 10, sticky = tk.SE)
  

class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,background=backgroundColour)

        durationLabel = tk.Label(self, text="Measuring Live Data" , font=('Arial Light', 18), bg=backgroundColour, fg="black")
        titleLabel = tk.Label(self, text="Overall Power Usage", font=('Arial Bold', 32), bg=backgroundColour, fg="black")

        returnButton = tk.Button(self, text ="Return",command = lambda : controller.show_frame(StartPage))

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
  
class Page2(tk.Frame):
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
                                 command = lambda : controller.startTest(5,canvas,values,intCountry))
        startButton.image = startImage

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsPage2(controller))
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
        
class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=backgroundColour)

        def changeRegion(i,buttonText):
            countryLabel["text"] = buttonText
            countryLabel.update
            controller.updateCountry(i)

        returnButton = tk.Button(self, text ="Return",command = lambda : controller.show_frame(previousScreen))
        currentLabel = ttk.Label(self, text="Current Country: ", font=('Arial Light', 24), style= 'Test.TLabel')
        countryLabel = ttk.Label(self, text="Ireland", font=('Arial Light', 24), style= 'Test.TLabel')
        selectLabel = ttk.Label(self, text="Select a country: ",font=('Arial Light', 18), style= 'Test.TLabel')

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

        polImage = tk.PhotoImage(file='App/flagPoland.png')
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

        returnButton.grid(row = 0, column = 0,sticky=tk.NW, padx = 5, pady = 5)
        

app = tkinterApp()
app.resizable(False,False)
app.title("Eco Check")
app.mainloop()