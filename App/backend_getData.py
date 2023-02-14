import clr #package pythonnet, not clr
import os

def initialize_openhardwaremonitor():

    file = os.getcwd() + '/Frontend/OpenHardwareMonitorLib'
    clr.AddReference(file)
    from OpenHardwareMonitor import Hardware

    c = Hardware.Computer()
    c.MainboardEnabled = True
    c.CPUEnabled = True
    ##Dedicated RAM produces power usage
    c.RAMEnabled = True
    c.GPUEnabled = True
    ##c.HDDEnabled = True
    c.Open()
    return c
        
def fetch_dict():
    c = initialize_openhardwaremonitor()
    CPU = c.Hardware[1]
    CPU.Update()
    RAM = c.Hardware[2]
    RAM.Update()
         ##need error handling 


    ## Just returning dummy data for ease of integration on different OS'
    stats_dict = {
        "cpu usage" : 20, #Power Usage
        "ram usage" : 30, #Memory Usage
        "gpu usage" : 40 #Power Usage
    }
    return (stats_dict)

   
if __name__ == "__main__":
    print("CPU Power Draw:")
    c = initialize_openhardwaremonitor()
    fetch_dict()