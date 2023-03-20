# 'python3 -m pip install tkinter'
# 'python3 -m pip install matplotlib'

import tkinter as tk
from tkinter import ttk
from random import randint
# import time
import matplotlib.pyplot as plt
import platform as os
import backend_analysis

global intCountry
global boldFontSize
boldFontSize = 40
#boldFontSize = 48
#        if Windows:
#            boldFontSize = 40
class screenSetup(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Power Meter')
        self.resizable(False,False)
        self._mainCanvas = None
        self._allCanvases = dict() #Not continuously "creating and destroying" screens
        self.switch_Canvas(Home)

    def switch_Canvas(self, Canvas_class):
        if self._mainCanvas:    #Hides current frame (canvas)
            self._mainCanvas.pack_forget() 

        canvas = self._allCanvases.get(Canvas_class, False) #Checks to see if class is in dict
        if not canvas:
            canvas = Canvas_class(self) #Creating new screen if screen has not been used yet
            self._allCanvases[Canvas_class] = canvas.pack()
            self._mainCanvas= canvas

class Home(tk.Canvas, tk.Tk):
    def __init__(self, master, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)
        tk.Frame(self)
        tk.Label(self, text="Choose screen").grid(column = 0, row = 0)
        tk.Button(self, text="Overall performance",
              command=lambda: master.switch_Canvas(Screen1)).grid(column = 0, row = 1)
        tk.Button(self, text="Individual Application",
              command=lambda: master.switch_Canvas(Screen2)).grid(column = 0, row = 2)
        
class Screen1(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self,master, *args, **kwargs)
        backgroundColour = '#DAEFD2'
        #self.canvas = tk.Canvas(self,bg=backgroundColour)
        self.configure(background=backgroundColour)

        durationLabel = tk.Label(self, text="%d SECOND" %durationInput, font=('Arial Light', 18), bg=backgroundColour, fg="black")
        titleLabel = tk.Label(self, text="Power Consumption", font=('Arial Bold', 32), bg=backgroundColour, fg="black")
        durationLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
        titleLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 40, pady = 0)
        buttonWidth = 10
        if Windows: 
            buttonWidth = 15

        canvas = tk.Canvas(self, background=backgroundColour, height=400, width=400, highlightthickness=0)
        intCircle = canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
        backArc = canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")
        # wattText = canvas.create_text(200, 210, text='Click "Start" to run\na 5-second test', font=('Arial Bold', 28), fill="black", justify="center")
        startText = canvas.create_text(200, 200, text='Press "Start"', font=('Arial Bold', boldFontSize), fill="black", justify="center")
        subtitleText = canvas.create_text(200, 245, text="TO START A 5-SECOND TEST", font=('Arial Light', 18), fill="gray", justify="center")
        canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)


        startImage = tk.PhotoImage(file='App/Test.png')
        startImage = startImage.subsample(2)

        carbonButton = tk.Button(self, text="Start", image=startImage, height=150, width=150, borderwidth=0)
        carbonButton['command'] = lambda: startTest(5, canvas)
        carbonButton.image = startImage
        carbonButton.grid(row = 2, column = 0, sticky = tk.E, padx = 40, pady = 2)

        graphImage = tk.PhotoImage(file='App/Graph.png')
        graphImage = graphImage.subsample(2)
        # graphButton = tk.Button(root, text="View Graph", image=graphImage, height=150, width=150, borderwidth=0,command=graphToDisplay)
        # graphButton.grid(row = 2, column = 1, sticky = tk.W, padx = 0, pady = 2)

        # value 2 = GPU
        # value 3 = CPU 
        # value 4 = ram 
        values = tk.Canvas(self, background=backgroundColour,height=150, width=150, highlightthickness=0)
        hardware = values.create_rectangle(5, 5, 150, 250, outline=backgroundColour,fill=backgroundColour)
        GPU = values.create_text(40,40,text = "GPU : ",font =('Arial Bold', 18),fill="black", justify="center")
        CPU = values.create_text(40,80,text = "CPU :",font =('Arial Bold', 18),fill="black", justify="center")
        GPU = values.create_text(40,120,text = "RAM :",font =('Arial Bold', 18),fill="black", justify="center")
        GPU_values = values.create_text(100,40,text = "TBC",font =('Arial Light', 12),fill="black", justify="center")
        CPU_values = values.create_text(100,80,text = "TBC",font =('Arial Light', 12),fill="black", justify="center")
        GPU_values = values.create_text(100,120,text = "TBC",font =('Arial Light', 12),fill="black", justify="center")
        values.grid(row = 2, column = 1, sticky = tk.W, padx = 0, pady = 2)

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)

        settingsButton = tk.Button(self, text="Settings", image=settingsImage, borderwidth=0, command=lambda: navToSettings(canvas))
        settingsButton.image = settingsImage
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)


#root = tk.Tk()
# root.geometry("878x535")
#root.title("Power Meter")
#backgroundColour = '#DAEFD2'
#root.configure(background=backgroundColour)
# root.configure(background='white')
#root.resizable(False, False)

durationInput = 5
wattInput = 175
peakWattInput = 200
country = ["Ireland", "France", "Great Britain", "Russia", "Australia", "Brazil", "New Zealand", "United States", "Spain", "Portugal", "Italy","Germany"]
countryID = ["IE", "FR", "GB", "RU", "AU", "BR", "NZ", "US", "ES", "PT", "IT", "DE"]
intCountry = 0

Windows = False
if os.platform().__contains__("Windows"):
    Windows = True
    

def navToSettings(canvas):
    # navSettings = tk.Toplevel(root)
    # navSettings.geometry("878x535")
    # navSettings.configure(background="white")
    # navSettings.title("Settings")
    # settingsLabel = tk.Label(navSettings, text ="<", font=('Arial Light', 18), bg=backgroundColour, fg="gray")
    # settingsLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 40, pady = 0)
    # tk.Label(navSettings, text ="Settings", font=('Arial Bold', 32), bg="white", fg="black").pack()
    canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
    canvas.create_text(200, 130, text="↑", font=('Arial',45),fill="grey", justify="center")
    canvas.create_text(200, 290, text="↓", font=('Arial',45),fill="grey", justify="center")
    updateCountry(intCountry, canvas)
    canvas.create_text(200, 245, text="SELECTED COUNTRY", font=('Arial Light', 18), fill="gray", justify="center")
    # button = tk.Button(canvas, text="Settings", image=settingsImage, height=50, width=100, borderwidth=0)
    root.bind('<Up>', nextCountry())
    root.bind('<Down>', previousCountry())

def nextCountry(event):
    global intCountry
    if intCountry == len(country)-1:
        intCountry = 0
    else:
        intCountry += 1
    navToSettings()

def previousCountry(event):
    global intCountry
    if intCountry == 0:
        intCountry = len(country)-1
    else:
        intCountry -= 1
    navToSettings()

def updateCountry(index,canvas):
    for x in country:
        canvas.create_text(200, 200, text=country[intCountry], font=('Arial Bold', boldFontSize), fill="black", justify="center")

def graphToDisplay():
    # graphScreen = tk.Toplevel(root)
    # graphScreen.geometry("878x535")
    # graphScreen.configure(background="white")
    # graphScreen.title("Graph")
    # graphScreen.resizable(False, False)

    # get data points

    #line graph
    time = ['1','2','3','4','5']
    power = [randint(0,50), randint(0,50), randint(0,50), randint(0,50), randint(0,50)]
    plt.title('Graph')
    plt.plot(time, power)
    plt.title('Displaying Power Usage',font=('Arial'),fontsize=14)
    plt.xlabel('Time (Seconds)',fontsize=12)
    plt.ylabel('Power (Watts)',fontsize=12)
    plt.show()

# def calculatingScreen():
#     canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
#     canvas.create_text(200, 200, text='Calculating ... ', font=('Arial Bold', boldFontSize), fill="black", justify="center")
#     canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")


    
def startTest(durationInput, canvas):
    ##Calling the analysis function
    backendData = backend_analysis.dataAnalysis(durationInput, countryID[intCountry])
    wattInput = backendData[0]
    carbonEmissions = (((backendData[1])/60)/12)*1000
    ##
    canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
    canvas.create_text(200, 200, text=str(round(wattInput, 2)) + " W", font=('Arial Bold', boldFontSize+16), fill="black", justify="center")
    canvas.create_text(200, 245, text=str(round(carbonEmissions, 2)) + " gCO₂", font=('Arial Light', 18), fill="gray", justify="center")
    canvas.create_text(200, 160, text="Ø", font=('Arial Light', 18), fill="gray", justify="center")
    # backArc
    canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")
    # The arc starts from the right and is a total of 270°, so 270-((avg/peak) * 270) in grey will give the percentage visually
    # progressArc
    canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=8, start=315, extent="%d" % round(270-((wattInput/peakWattInput)*270)))
    print(round(270-((wattInput/peakWattInput)*270)))

root = screenSetup()
root.mainloop()