#NB-Ensure no GUI are open

import pyautogui as gui

screenWidth, screenHeight = gui.size()

def testOpenGUI():
    gui.moveTo(150,130)
    gui.click()

    gui.moveTo(1350,20)
    gui.click()

def testStartButton():
    #Bug - does not show mouse clicked but shows number change
    gui.moveTo(200,425)
    gui.sleep(1)
    gui.click()
    gui.sleep(5)

def testSettings():
    gui.sleep(1)
    gui.moveTo(875,525)
    gui.click()

testOpenGUI()
testStartButton()
testSettings()
