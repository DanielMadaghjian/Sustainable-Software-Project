import clr #package pythonnet, not clr
import os

def initialize_openhardwaremonitor():

    file = os.getcwd() + '/Backend/OpenHardwareMonitorLib'
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


def fetch_stats(c):
    for i in c.Hardware:
        print (i)
    CPU = c.Hardware[1]
    CPU.Update()
    sensor = CPU.Sensors[5]
    print(sensor.Value)
    RAM = c.Hardware[2]
    RAM.Update()
    sensor = RAM.Sensors[0]
    print(round(sensor.Value,2))
    GPU = c.Hardware[3]
    GPU.Update()
    sensor = GPU.Sensors[12]
    if ((sensor.Value != None) and (sensor.Value != 0)):
        print (sensor.Value) 
    #total = 0
    #for i in GPU.Sensors:
    #    total += 1
    #j = 0
    #while j < total:
    #    print(GPU.Sensors[j].Name)
    #    j += 1
        

def fetch_dict():
    c = initialize_openhardwaremonitor()
    CPU = c.Hardware[1]
    CPU.Update()
    RAM = c.Hardware[2]
    RAM.Update()
    GPU = c.Hardware[3]
    GPU.Update()
    sensor = GPU.Sensors[1]     ##need error handling 
    if sensor != None:
        if ((sensor.Value != None) and (sensor.Value != 0)):
            GPU_power = sensor.Value
        else:
            GPU_power = None
    else: 
        GPU_power = None

    stats_dict = {
        "cpu usage" : CPU.Sensors[5].Value, #Power Usage
        "ram usage" : RAM.Sensors[0].Value, #Memory Usage
        "gpu usage" : GPU_power #Power Usage
    }
    return (stats_dict)

   
if __name__ == "__main__":
    print("CPU Power Draw:")
    c = initialize_openhardwaremonitor()
    fetch_stats(c)
    fetch_dict()