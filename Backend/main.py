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
    #for i in c.Hardware:
    #    print (i)
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
    #for i in RAM.Sensors:
    #    total += 1
    #j = 0
    #while j < total:
    #    print(RAM.Sensors[j].Name)
    #    j += 1

    #ram generally 3w per 8 gb
        

def fetch_dict():
    initialize_openhardwaremonitor()
    CPU = c.Hardware[1]
    CPU.Update()

    RAM = c.Hardware[2]
    RAM.Update()
    RAM_mem = RAM.Sensors[1].Value + RAM.Sensors[2].Value
    max_RAM_power = (3/8) * RAM_mem #3w per 8gb of ddr3, 4.5w per 8gb of ddr2, 5.5 per 8gb of ddr1 (worst cases)
    current_RAM_usage = RAM.Sensors[0].Value
    RAM_power = max_RAM_power * (current_RAM_usage/100)

    GPU = c.Hardware[3]
    GPU.Update()
    sensor = GPU.Sensors[12]
    if sensor != None:
        if ((sensor.Value != None) and (sensor.Value != 0)):
            GPU_power = sensor.Value
        else:
            GPU_power = None
    else: 
        GPU_power = None

    stats_dict = {
        "cpu usage" : CPU.Sensors[5].Value, #Power Usage
        "ram usage" : RAM_power, #Approx Power Usage
        "gpu usage" : GPU_power #Power Usage
    }
    print(stats_dict)
    return (stats_dict)

   
if __name__ == "__main__":
    print("CPU Power Draw:")
    c = initialize_openhardwaremonitor()
    fetch_stats(c)
    fetch_dict()