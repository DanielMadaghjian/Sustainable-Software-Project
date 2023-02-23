from statistics import mean
import time
import backend_getData

gpuList = [] 
cpuList = [] 
ramList = []

# Method that calculates the average power 
def getPower(gpuList, cpuList, ramList):
  gpuAverage = mean(gpuList)
  cpuAverage = mean(cpuList)
  ramAverage = mean(ramList)
  power = gpuAverage + cpuAverage + ramAverage
  return power


# Method that collects the raw data and filters it
def dataAnalysis(t):
  while t:
      print(t)
      time.sleep(1)
      currentData = backend_getData.fetch_dict()
      gpuList.append(currentData.get("gpu usage"))
      cpuList.append(currentData.get("cpu usage"))
      ramList.append(currentData.get("ram usage"))
      t -= 1
  
  values = []
  power = getPower(gpuList, cpuList, ramList)
  values.append(power)
  print(values[0], "Watts")
  return values


