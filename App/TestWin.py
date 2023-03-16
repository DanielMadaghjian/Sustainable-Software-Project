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
    gui.moveTo((windowX + 140) * offset, (windowY + 380) * offset + windowHeader) # noqa: F821
    gui.sleep(0.5)
    gui.click()
    gui.sleep(0.1)
    # Clicks a window a second time to improve accessibility (In case window is not highlighted)
    gui.click()
    gui.sleep(5.2)

def testSettings():
    gui.sleep(1)
    gui.moveTo((windowX + windowWidth) - 75 * offset, (windowY + windowHeight) - 30 * offset)# noqa: F821
    gui.click()

    print("Window found! Running tests...")
    windowHeight = windowBounds['Height'] # noqa: F821
    windowWidth = windowBounds['Width'] # noqa: F821
    windowX = windowBounds['X'] # noqa: F821
    windowY = windowBounds['Y'] # noqa: F821
    windowHeader = 25 # noqa: F821
    offset = 1 # noqa: F821

    try:
        window = pgw.getWindowsWithTitle('Power Meter')[0] # noqa: F821
        window.moveTo(30,30) # noqa: F821
        print("Window found! Running tests...")
        
    except:
        print('Unable to find window, please run "PowerMeter.py"')
        quit()

# testOpenGUI()
testStartButton()
testSettings()
print("Tests complete!")
