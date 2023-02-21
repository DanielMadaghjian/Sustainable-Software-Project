# 'python3 -m pip install tkinter'
import tkinter as tk
from random import randint
import time
import platform as os
import backend_analysis
root = tk.Tk()
# root.geometry("878x535")
root.title("Power Meter")
backgroundColour = '#DAEFD2'
root.configure(background=backgroundColour)
# root.configure(background='white')
root.resizable(False, False)

durationInput = 5
wattInput = 175
peakWattInput = 200

Windows = False
if os.platform().__contains__("Windows"):
    Windows = True

def navToSettings():
    # navSettings = tk.Toplevel(root)
    # navSettings.geometry("878x535")
    # navSettings.configure(background="white")
    # navSettings.title("Settings")
    # settingsLabel = tk.Label(navSettings, text ="<", font=('Arial Light', 18), bg=backgroundColour, fg="gray")
    # settingsLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 40, pady = 0)
    # tk.Label(navSettings, text ="Settings", font=('Arial Bold', 32), bg="white", fg="black").pack()
    canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
    canvas.create_text(200, 200, text="Ireland", font=('Arial Bold', boldFontSize+16), fill="black", justify="center")
    canvas.create_text(200, 245, text="SELECTED COUNTRY", font=('Arial Light', 18), fill="gray", justify="center")
    # button = tk.Button(canvas, text="Settings", image=settingsImage, height=50, width=100, borderwidth=0)
    



durationLabel = tk.Label(root, text="%d SECOND" %durationInput, font=('Arial Light', 18), bg=backgroundColour, fg="black")
titleLabel = tk.Label(root, text="Power Consumption", font=('Arial Bold', 32), bg=backgroundColour, fg="black")
durationLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
titleLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 40, pady = 0)
buttonWidth = 10
if Windows: 
    buttonWidth = 15

startImage = tk.PhotoImage(file='App/Test.png')
startImage = startImage.subsample(2)

carbonButton = tk.Button(root, text="Start", image=startImage, height=150, width=150, borderwidth=0)
carbonButton['command'] = lambda: startTest(5)

graphImage = tk.PhotoImage(file='App/Graph.png')
graphImage = graphImage.subsample(2)

graphButton = tk.Button(root, text="View Graph", image=graphImage, height=150, width=150, borderwidth=0)
carbonButton.grid(row = 2, column = 0, sticky = tk.E, padx = 40, pady = 2)
graphButton.grid(row = 2, column = 1, sticky = tk.W, padx = 0, pady = 2)
canvas = tk.Canvas(root, background=backgroundColour, height=400, width=400, highlightthickness=0)
intCircle = canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
backArc = canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")
# wattText = canvas.create_text(200, 210, text='Click "Start" to run\na 5-second test', font=('Arial Bold', 28), fill="black", justify="center")
boldFontSize = 48
if Windows:
    boldFontSize = 40
startText = canvas.create_text(200, 200, text='Press "Start"', font=('Arial Bold', boldFontSize), fill="black", justify="center")
subtitleText = canvas.create_text(200, 245, text="TO START A 5-SECOND TEST", font=('Arial Light', 18), fill="gray", justify="center")
canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)

settingsImage = tk.PhotoImage(file='App/Settings.png')
settingsImage = settingsImage.subsample(3)

settingsButton = tk.Button(root, text="Settings", image=settingsImage, height=50, width=100, borderwidth=0, command=lambda: navToSettings())
settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)

def startTest(durationInput):
    ##Calling the analysis function
    wattInput = backend_analysis.dataAnalysis(durationInput)[0]
    peakWattInput = wattInput + randint(0,25)
    ##
    canvas.create_oval(15, 15, 385, 385, outline="white", fill="white")
    canvas.create_text(200, 200, text=str(round(wattInput, 2)) + " W", font=('Arial Bold', boldFontSize+16), fill="black", justify="center")
    canvas.create_text(200, 245, text="PEAK " + str(round(peakWattInput, 2)) + " W", font=('Arial Light', 18), fill="gray", justify="center")
    canvas.create_text(200, 160, text="Ø", font=('Arial Light', 18), fill="gray", justify="center")
    # backArc
    canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")
    # The arc starts from the right and is a total of 270°, so 270-((avg/peak) * 270) in grey will give the percentage visually
    # progressArc
    canvas.create_arc(5, 5, 395, 395, outline="white", style=tk.ARC, width=8, start=315, extent="%d" % round(270-((wattInput/peakWattInput)*270)))
    print(round(270-((wattInput/peakWattInput)*270)))

root.mainloop()

