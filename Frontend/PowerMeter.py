import random
import time
import tkinter as tk
import platform as os
root = tk.Tk()
# root.geometry("878x535")
root.title("Power Meter")
root.configure(background="white")
root.resizable(False, False)

durationInput = 5
wattInput = 175
peakWattInput = 200

Windows = False
if os.platform().__contains__("Windows"):
    Windows = True

def navToSettings():
    navSettings = tk.Toplevel(root)
    navSettings.geometry("878x535")
    navSettings.configure(background="white")
    navSettings.title("Settings")
    settingsLabel = tk.Label(navSettings, text ="<", font=('Arial Light', 18), bg="white", fg="gray")
    settingsLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 40, pady = 0)
    tk.Label(navSettings, text ="Settings", font=('Arial Bold', 32), bg="white", fg="black").pack()

def start5SecondTest():
    durationInput = 5
    wattInput = random.randint(50,120)
    peakWattInput = wattInput + random.randint(0,50)
    time.sleep(5)
    canvas.create_oval(15, 15, 385, 385, outline="white", fill="#EEEEEE")
    canvas.create_text(200, 200, text="%d W" %wattInput, font=('Arial Bold', 64), fill="black", justify="center")
    canvas.create_text(200, 245, text="PEAK %d W" %peakWattInput, font=('Arial Light', 18), fill="gray", justify="center")
    # backArc
    canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")
    # The arc starts from the right and is a total of 270°, so 270-((avg/peak) * 270) in grey will give the percentage visually
    # progressArc
    canvas.create_arc(5, 5, 395, 395, outline="#EEEEEE", style=tk.ARC, width=8, start=315, extent="%d" % round(270-((wattInput/peakWattInput)*270)))
    print(round(270-((wattInput/peakWattInput)*270)))

durationLabel = tk.Label(root, text="%d SECOND" %durationInput, font=('Arial Light', 18), bg="white", fg="gray")
titleLabel = tk.Label(root, text="Power Consumption", font=('Arial Bold', 32), bg="white", fg="black")
durationLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
titleLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 40, pady = 0)
buttonWidth = 10
if Windows: 
    buttonWidth = 15
carbonButton = tk.Button(root, text="Start", height=6, width=buttonWidth, command=start5SecondTest)
graphButton = tk.Button(root, text="View Graph", height=6, width=buttonWidth)
carbonButton.grid(row = 2, column = 0, sticky = tk.E, padx = 40, pady = 2)
graphButton.grid(row = 2, column = 1, sticky = tk.W, padx = 0, pady = 2)
canvas = tk.Canvas(root, background="white", height=400, width=400, highlightthickness=0)
intCircle = canvas.create_oval(15, 15, 385, 385, outline="white", fill="#EEEEEE")
backArc = canvas.create_arc(5, 5, 395, 395, outline="black", style=tk.ARC, width=6, start=315, extent="270")
# wattText = canvas.create_text(200, 210, text='Click "Start" to run\na 5-second test', font=('Arial Bold', 28), fill="black", justify="center")
startFontSize = 48
if Windows:
    startFontSize = 40
startText = canvas.create_text(200, 200, text='Press "Start"', font=('Arial Bold', startFontSize), fill="black", justify="center")
subtitleText = canvas.create_text(200, 245, text="TO START A 5-SECOND TEST", font=('Arial Light', 18), fill="gray", justify="center")
canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
settingsButton = tk.Button(root, text = "Settings", height = 2, width = 10, bg="white", fg="black", command=navToSettings)
settingsButton.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = tk.SE)

root.mainloop()

