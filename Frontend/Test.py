# NB -  Ensure no GUI are open,
#       Run PowerMeter.py,
#       then run this file in debug mode

import time
import pyautogui as gui
from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll

screenWidth, screenHeight = gui.size()

# def testOpenGUI():
#     gui.moveTo(150,130)
#     gui.click()

#     gui.moveTo(1350,20)
#     gui.click()

def testStartButton():
    #Bug - does not show mouse clicked but shows number change
    gui.moveTo(windowX + 135, windowY + windowHeader + 380)
    gui.sleep(0.5)
    gui.click()
    gui.sleep(0.1)
    # Clicks a window a second time to improve accessibility (In case window is not highlighted)
    gui.click()
    gui.sleep(5.2)

def testSettings():
    gui.sleep(1)
    gui.moveTo(windowX + windowWidth - 75, windowY + windowHeight - 30)
    gui.click()

allWindows = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
windowOnScreen = False
for window in allWindows:
    try:
        if window['kCGWindowOwnerName'] == "Python" and window['kCGWindowIsOnscreen'] == 1:
            print(window)
            windowOnScreen = True
            windowBounds = window['kCGWindowBounds']
    except:
        pass
    if windowOnScreen == True:
        break
# Code using CGWindowListCopyWindowInfo inspired by Suyash Patel (https://stackoverflow.com/users/3706058/suyash-patel)
if windowOnScreen == False:
    print('Unable to find window, please run "PowerMeter.py"')
    quit()

print("Window found! Running tests...")
windowHeight = windowBounds['Height']
windowWidth = windowBounds['Width']
windowX = windowBounds['X']
windowY = windowBounds['Y']
print(windowHeight, windowWidth, windowX, windowY)
windowHeader = 25

# testOpenGUI()
testStartButton()
testSettings()
