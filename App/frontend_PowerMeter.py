
# 'python3 -m pip install tkinter'
# 'python3 -m pip install matplotlib'

import tkinter as tk
from tkinter import ttk
import backend_analysis

LARGEFONT =('Arial',45)
backgroundColour = '#DAEFD2'
previousScreen = tk.Frame

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
    
    def startTest(self,durationInput,canvas,values):
    ##Calling the analysis function
        backendData = backend_analysis.dataAnalysis(durationInput, 'IE')
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

    def settingsPage1(self,controller):
        global previousScreen
        previousScreen = Page1
        controller.show_frame(SettingsPage)

    def settingsPage2(self,controller):
        global previousScreen
        previousScreen = Page2
        controller.show_frame(SettingsPage)
  
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        backgroundColour = '#DAEFD2'
        tk.Frame.__init__(self, parent, background=backgroundColour)

        button1 = tk.Button(self, text ="Continuous Usage",command = lambda : controller.show_frame(Page1))
        button2 = tk.Button(self, text ="Individual Usage",command = lambda : controller.show_frame(Page2))

        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsStart(controller))
        #command = lambda : controller.navToSettings())
        settingsButton.image = settingsImage

        button1.grid(row = 1, column = 1,padx = 10, pady = 10)
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
  

class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
        # backgroundColour = '#DAEFD2' 
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text ="StartPage",command = lambda : controller.show_frame(StartPage))
        settingsImage = tk.PhotoImage(file='App/Settings.png')
        settingsImage = settingsImage.subsample(3)
        settingsButton = tk.Button(self, text="Settings", image=settingsImage, height = 50, width = 100, borderwidth = 0, 
                                   command = lambda : controller.settingsPage1(controller))
        #command = lambda : controller.navToSettings())
        settingsButton.image = settingsImage
     
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
        settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)
  
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
                                 command = lambda : controller.startTest(5,canvas,values))
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


