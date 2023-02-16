from statistics import mean
import time
import backend_getData

gpuList = [] 
cpuList = [] 
ramList = []




#print(cpuList)


def dataAnalysis(t):
  # integrated gpu will be part of cpu
  while t:
      print(t)
      time.sleep(1)
      currentData = backend_getData.fetch_dict()
      gpuList.append(currentData.get("gpu usage"))
      cpuList.append(currentData.get("cpu usage"))
      ramList.append(currentData.get("ram usage"))
      t -= 1
  
  values = []
  gpuAverage = mean(gpuList)
  cpuAverage = mean(cpuList)
  ramAverage = mean(ramList)
  power = gpuAverage + cpuAverage + ramAverage
  values.append(power)
  print(values[0], "Watts")
  return values
