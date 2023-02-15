import clr #package pythonnet, not clr
import os
file = os.getcwd() + '/Backend/OpenHardwareMonitorLib'
clr.AddReference(file)
from OpenHardwareMonitor import Hardware

def initialize_openhardwaremonitor():
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
    #if CPU.HardwareType == HardwareType.CPU:
    #    CPU.Update()
    #    for sensor in CPU.Sensors:
    #            if(sensor.SensorType == SensorType.Power and sensor.Name.Contains("CPU Package")):
    #                print(sensor.Value)
    CPU.Update()
    sensor = CPU.Sensors[5]
    print(sensor.Value)
    RAM = c.Hardware[2]
    #if RAM.HardwareType == HardwareType.RAM:
    #    RAM.Update()
    #    for sensor in RAM.Sensors:
    #        if (sensor.SensorType == SensorType.Power and sensor.Name.Contains("RAM Package")):
    #            print(sensor.Value)
    RAM.Update()
    sensor = RAM.Sensors[0]
    print(round(sensor.Value,2))
    GPU = c.Hardware[3]
    #if (GPU.HardwareType == HardwareType.GpuAti or HardwareType.GpuNvidia):
    #    GPU.Update() 
    #    for sensor in GPU.Sensors:
    #        if (sensor.SensorType==SensorType.Clock and sensor.Name.Constains("GPU Memory")):
    #            if ((sensor.Value != None) and (sensor.Value != 0)):
    #                print (sensor.Value) 
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
    c = initialize_openhardwaremonitor()

    for hardware in c.Hardware:
        if hardware.HardwareType == Hardware.HardwareType.CPU:
            hardware.Update()
            for sensor in hardware.Sensors:
                if(sensor.SensorType == Hardware.SensorType.Power and "CPU Package" in sensor.Name):
                    cpu = sensor.Value
        elif hardware.HardwareType == Hardware.HardwareType.RAM:
            hardware.Update()
            for sensor in hardware.Sensors:
                RAM_mem=0
                current_RAM_usage=0
                if(sensor.SensorType == Hardware.SensorType.Data and "Used Memory" in sensor.Name):
                    RAM_mem += sensor.Value()
                elif(sensor.SensorType == Hardware.SensorType.Data and "Available Memory" in sensor.Name):
                    RAM_mem+= sensor.Value()
                elif(sensor.SensorType == Hardware.SensorType.Load and "Memory" in sensor.Name):
                    current_RAM_usage=sensor.Value()
            max_RAM_power = (3/8) * RAM_mem
            RAM_power = max_RAM_power * (current_RAM_usage/100)
        elif(hardware.HardwareType == Hardware.HardwareType.GpuAti or hardware.HardwareType == Hardware.HardwareType.GpuNvidia):
            hardware.Update()
            for sensor in hardware.Sensors:
                if(sensor.SensorType == Hardware.SensorType.Clock and "GPU Core" in sensor.Name):
                    if sensor != None:
                        if ((sensor.Value != None) and (sensor.Value != 0)):
                            GPU_power = sensor.Value
                        else:
                            GPU_power = None
                    else: 
                        GPU_power = None
   #CPU = c.Hardware[1]
    #CPU.Update()

    #RAM = c.Hardware[2]
    #RAM.Update()
    #RAM_mem = RAM.Sensors[1].Value + RAM.Sensors[2].Value
    #max_RAM_power = (3/8) * RAM_mem #3w per 8gb of ddr3, 4.5w per 8gb of ddr2, 5.5 per 8gb of ddr1 (worst cases)
    #current_RAM_usage = RAM.Sensors[0].Value
    #RAM_power = max_RAM_power * (current_RAM_usage/100)

    #GPU = c.Hardware[3]
    #GPU.Update()
    #sensor = GPU.Sensors[1]     ##need error handling 
    #if sensor != None:
    #    if ((sensor.Value != None) and (sensor.Value != 0)):
    #        GPU_power = sensor.Value
    #    else:
    #        GPU_power = None
    #else: 
    #    GPU_power = None

    stats_dict = {
        "cpu usage" : cpu, #Power Usage
        "ram usage" : RAM_power, #Approx Power Usage
        "gpu usage" : GPU_power #Power Usage
    }
    print(stats_dict)
    return (stats_dict)

   
if __name__ == "__main__":
    print("CPU Power Draw:")
    c = initialize_openhardwaremonitor()
    ##fetch_stats(c)
    fetch_dict()