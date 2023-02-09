import random
import time
import tkinter as tk
root = tk.Tk()
root.geometry("878x535")
root.title("Power Meter")
root.configure(background="white")
root.resizable(False, False)

durationInput = 5
wattInput = 175
peakWattInput = 200

def navToSettings():
    navSettings = tk.Toplevel(root)
    navSettings.geometry("878x535")
    navSettings.configure(background="white")
    navSettings.title("Settings")
    tk.Label(navSettings, text ="<", font=('Arial Light', 18), bg="white", fg="gray").pack()
    tk.Label(navSettings, text ="Settings", font=('Arial Bold', 32), bg="white", fg="black").pack()

def start5SecondTest():
    durationInput = 5
    wattInput = random.randint(50,100)
    peakWattInput = random.randint(50,100)
    time.sleep(5)
    
    canvas.create_oval(15, 15, 385, 385, outline="white", fill="#EEEEEE")
    wattText = canvas.create_text(200, 200, text="%d W" %wattInput, font=('Arial Bold', 64), fill="black", justify="center")
    peakWattText = canvas.create_text(200, 245, text="PEAK %d W" %peakWattInput, font=('Arial Light', 18), fill="gray", justify="center")

durationLabel = tk.Label(root, text="%d SECOND" %durationInput, font=('Arial Light', 18), bg="white", fg="gray")
titleLabel = tk.Label(root, text="Power Consumption", font=('Arial Bold', 32), bg="white", fg="black")
durationLabel.grid(row = 0, column = 0, columnspan = 2, rowspan = 1, sticky = tk.SW, padx = 40, pady = 0)
titleLabel.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = tk.NW, padx = 40, pady = 0)
carbonButton = tk.Button(root, text="Start 5-\nSecond Test", height=6, width=10, command=start5SecondTest)
graphButton = tk.Button(root, text="View Graph", height=6, width=10)
carbonButton.grid(row = 2, column = 0, sticky = tk.E, padx = 40, pady = 2)
graphButton.grid(row = 2, column = 1, sticky = tk.W, padx = 0, pady = 2)
canvas = tk.Canvas(root, background="white", height=400, width=400, highlightthickness=0)
intCircle = canvas.create_oval(15, 15, 385, 385, outline="white", fill="#EEEEEE")
extCircle = canvas.create_oval(5, 5, 395, 395, outline="black", width=5)
wattText = canvas.create_text(200, 200, text="%d W" %wattInput, font=('Arial Bold', 64), fill="black", justify="center")
peakWattText = canvas.create_text(200, 245, text="PEAK %d W" %peakWattInput, font=('Arial Light', 18), fill="gray", justify="center")
canvas.grid(row = 0, column = 2, columnspan = 2, rowspan = 3, padx = 40, pady = 40)
settingsButton = tk.Button(root, text = "Settings", height = 2, width = 10, bg="white", fg="black", command=navToSettings)
settingsButton.grid(row = 3, column = 3, padx = 10, pady = 0, sticky = tk.SE)

root.mainloop()

