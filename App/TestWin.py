# NB -  Install required libraries by running:
#       macOS/Linux: PyAutoGUI - 'python3 -m pip install pyautogui'
#                    Quartz    - 'python3 -m pip install pyobjc-framework-Quartz'
#       Windows:     PyAutoGUI - 'py -m pip install pyautogui'
#       Ensure no other GUIs are blocking the "Start" button,
#       Run PowerMeter.py,
#       Finally, run this file in debug mode.

import pyautogui as gui
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

    print("Window found! Running tests...")
    windowHeight = windowBounds['Height']
    windowWidth = windowBounds['Width']
    windowX = windowBounds['X']
    windowY = windowBounds['Y']
    windowHeader = 25
    offset = 1 

    try:
        window = pgw.getWindowsWithTitle('Power Meter')[0]
        window.moveTo(30,30)
        print("Window found! Running tests...")
        
    except:
        print('Unable to find window, please run "PowerMeter.py"')
        quit()

# testOpenGUI()
testStartButton()
testSettings()
print("Tests complete!")
