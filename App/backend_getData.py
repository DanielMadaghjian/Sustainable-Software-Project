import clr #package pythonnet, not clr
import os
import psutil
file = os.getcwd() + '/App/OpenHardwareMonitorLib'
clr.AddReference(file)
from OpenHardwareMonitor import Hardware

def initialize_openhardwaremonitor():
    c = Hardware.Computer()
    c.MainboardEnabled = True
    c.CPUEnabled = True
    ##Dedicated RAM produces power usage
    c.RAMEnabled = True
    c.GPUEnabled = True
    c.HDDEnabled = True
    c.Open()
    return c
def get_disk_usage(disk_type):
    Disk_power = 0
    counts = psutil.disk_io_counters(perdisk=False, nowrap=True)
    read_count = counts[0]
    write_count = counts[1]
    if write_count!=0:
        if(disk_type == "HDD"):
            Disk_power = 8.5 #Average power use of the most common hdd disks while write or/and read
        elif(disk_type=="SSD"):
            Disk_power = 6 #Average state of power use of the most common ssd disks while write or/and read
    elif read_count!=0 and write_count==0:
        if(disk_type == "HDD"):
            Disk_power = 7.5 #Average power use of the most common hdd disks while read
        elif(disk_type=="SSD"):
            Disk_power = 4.75 #Average state of power use of the most common ssd disks while read
    else:
        if(disk_type == "HDD"):
            Disk_power = 6.5 #Average power use of the most common hdd disks while idle
        elif(disk_type=="SSD"):
            Disk_power = 1.5 #Average state of power use of the most common ssd disks while idle
    return Disk_power


def fetch_dict():
    c = initialize_openhardwaremonitor()
    CPU_power = 0
    GPU_power = 0
    RAM_power = 0
    RAM_Umem = 0
    RAM_Amem = 0
    RAM_Load = 0
    HDD_Load = 0
    Disk_power=0
    for hardware in c.Hardware:
        if hardware.HardwareType == Hardware.HardwareType.CPU:
    
            hardware.Update()
            for sensor in hardware.Sensors:
                if(sensor.SensorType == Hardware.SensorType.Power and "CPU Package" in sensor.Name):
                    CPU_power = CPU_power + sensor.Value
                elif (sensor.SensorType == Hardware.SensorType.Power and "CPU Cores" in sensor.Name):
                    CPU_power = CPU_power + sensor.Value
                elif (sensor.SensorType == Hardware.SensorType.Power and "CPU DRAM" in sensor.Name):
                    RAM_power = sensor.Value

        elif hardware.HardwareType == Hardware.HardwareType.RAM:
            
            hardware.Update()
            if(RAM_power == 0):
                for sensor in hardware.Sensors:
                    if(sensor.SensorType == Hardware.SensorType.Power and "RAM Package" in sensor.Name):
                        RAM_power = sensor.Value
                        break
                    elif(sensor.SensorType == Hardware.SensorType.Data and "Used Memory" in sensor.Name):
                        RAM_Umem = sensor.Value
                    elif(sensor.SensorType == Hardware.SensorType.Data and "Available Memory" in sensor.Name):
                        RAM_Amem = sensor.Value
                    elif(sensor.SensorType == Hardware.SensorType.Load and "Memory" in sensor.Name):
                        RAM_Load = sensor.Value

                    RAM_mem = RAM_Amem + RAM_Umem
                    max_RAM_power = (3/8) * RAM_mem #3w per 8gb of ddr3, 4.5w per 8gb of ddr2, 5.5 per 8gb of ddr1 (worst cases)
                    RAM_power = max_RAM_power * (RAM_Load/100)

        
        elif(hardware.HardwareType == Hardware.HardwareType.GpuAti or hardware.HardwareType == Hardware.HardwareType.GpuNvidia):
            hardware.Update()
            for sensor in hardware.Sensors:
                if(sensor.SensorType == Hardware.SensorType.Power and "GPU Power" in sensor.Name):
                    GPU_power = sensor.Value
        elif(hardware.HardwareType == Hardware.HardwareType.HDD):
            hardware.Update()
            for sensor in hardware.Sensors:
                if(sensor.SensorType == Hardware.SensorType.Load and "Used Space" in sensor.Name):
                    HDD_Load=sensor.Value
    
    Disk_power = get_disk_usage("SSD") #Parameter is the type of disk - user input
    stats_dict = {
        "cpu usage" : CPU_power, #Power Usage
        "ram usage" : RAM_power, #Approx Power Usage
        "gpu usage" : GPU_power, #Power Usage
        "disk usage" : Disk_power   #Approx Power Usage
    }
    print(stats_dict)
    return (stats_dict)

   
##Main Function For Testing 
if __name__ == "__main__":
    c = initialize_openhardwaremonitor()
    fetch_dict()