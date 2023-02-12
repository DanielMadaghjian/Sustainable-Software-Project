# NB -  Install pyautogui by running:
#       macOS/Linux: 'python3 -m pip install pyautogui'
#       Windows:     'py -m pip install pyautogui'
#       If you are using macOS, install Quartz with 'python3 -m pip install pyobjc-framework-Quartz'
#       Ensure no GUI are open,
#       Run PowerMeter.py,
#       then run this file in debug mode

import time
import pyautogui as gui
macOS = False
try:
    from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll
    print("Using macOS, importing Quartz...")
    macOS = True
except:
    print("Using Windows, using pygetwindow instead of Quartz...")
    import pygetwindow as pgw

screenWidth, screenHeight = gui.size()

# def testOpenGUI():
#     gui.moveTo(150,130)
#     gui.click()

#     gui.moveTo(1350,20)
#     gui.click()

def testStartButton():
    #Bug - does not show mouse clicked but shows number change
    gui.moveTo((windowX + 140) * offset, (windowY + 380) * offset + windowHeader)
    gui.sleep(0.5)
    gui.click()
    gui.sleep(0.1)
    # Clicks a window a second time to improve accessibility (In case window is not highlighted)
    gui.click()
    gui.sleep(5.2)

def testSettings():
    gui.sleep(1)
    gui.moveTo((windowX + windowWidth) - 75 * offset, (windowY + windowHeight) - 30 * offset)
    gui.click()

if macOS == True:
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
    windowHeader = 25
    offset = 1 
    # The offset is in place as the pixel measurements are smaller on macOS
else:
    try:
        window = pgw.getWindowsWithTitle('Power Meter')[0]
        window.moveTo(30,30)
        print("Window found! Running tests...")
        
    except:
        print('Unable to find window, please run "PowerMeter.py"')
        quit()
    
    windowHeader = 35
    windowHeight = window.height
    windowWidth = window.width
    windowX = 30
    windowY = 30
    offset = 1.5
    # The offset is in place as the pixel measurements are bigger on Windows

# testOpenGUI()
testStartButton()
testSettings()
