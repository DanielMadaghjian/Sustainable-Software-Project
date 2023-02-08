import clr #package pythonnet, not clr
import os

def initialize_openhardwaremonitor():

    file = os.getcwd() + '/Backend/OpenHardwareMonitorLib'
    clr.AddReference(file)
    from OpenHardwareMonitor import Hardware

    c = Hardware.Computer()
    c.MainboardEnabled = True
    c.CPUEnabled = True
    ##c.RAMEnabled = True
    ##c.GPUEnabled = True
    ##c.HDDEnabled = True
    c.Open()
    return c


def fetch_stats(c):
    CPU = c.Hardware[1]
    CPU.Update()
    sensor = CPU.Sensors[5]
    print(sensor.Value)
   
if __name__ == "__main__":
    print("CPU Power Draw:")
    c = initialize_openhardwaremonitor()
    fetch_stats(c)