from statistics import mean
import time

gpuList = [] 
cpuList = [] 
ramList = []

sample1 = {
  "gpu usage": 2.556562,
  "cpu usage": 4.515381,
  "ram usage": 3.591832
}

gpuList.append(sample1.get("gpu usage"))
cpuList.append(sample1.get("cpu usage"))
ramList.append(sample1.get("ram usage"))

sample2 = {
  "gpu usage": 2.656562,
  "cpu usage": 4.615381,
  "ram usage": 3.691832
}

gpuList.append(sample2.get("gpu usage"))
cpuList.append(sample2.get("cpu usage"))
ramList.append(sample2.get("ram usage"))

sample3 = {
  "gpu usage": 2.756562,
  "cpu usage": 4.715381,
  "ram usage": 3.791832
}

gpuList.append(sample3.get("gpu usage"))
cpuList.append(sample3.get("cpu usage"))
ramList.append(sample3.get("ram usage"))

sample4 = {
  "gpu usage": 2.856562,
  "cpu usage": 4.815381,
  "ram usage": 3.891832
}

gpuList.append(sample4.get("gpu usage"))
cpuList.append(sample4.get("cpu usage"))
ramList.append(sample4.get("ram usage"))

sample5 = {
  "gpu usage": 2.956562,
  "cpu usage": 4.915381,
  "ram usage": 3.991832
}

gpuList.append(sample5.get("gpu usage"))
cpuList.append(sample5.get("cpu usage"))
ramList.append(sample5.get("ram usage"))

sample6 = {
  "gpu usage": 2.956562,
  "cpu usage": 5.015381,
  "ram usage": 4.021832
}

gpuList.append(sample6.get("gpu usage"))
cpuList.append(sample6.get("cpu usage"))
ramList.append(sample6.get("ram usage"))

sample7 = {
  "gpu usage": 2.556562,
  "cpu usage": 4.515381,
  "ram usage": 3.591832
}

gpuList.append(sample7.get("gpu usage"))
cpuList.append(sample7.get("cpu usage"))
ramList.append(sample7.get("ram usage"))

sample8 = {
  "gpu usage": 2.356562,
  "cpu usage": 5.415381,
  "ram usage": 4.291832
}

gpuList.append(sample8.get("gpu usage"))
cpuList.append(sample8.get("cpu usage"))
ramList.append(sample8.get("ram usage"))

sample9 = {
  "gpu usage": 2.856562,
  "cpu usage": 5.215381,
  "ram usage": 3.163832
}

gpuList.append(sample9.get("gpu usage"))
cpuList.append(sample9.get("cpu usage"))
ramList.append(sample9.get("ram usage"))

sample10 = {
  "gpu usage": 2.346562,
  "cpu usage": 5.535381,
  "ram usage": 4.012832
}

gpuList.append(sample10.get("gpu usage"))
cpuList.append(sample10.get("cpu usage"))
ramList.append(sample10.get("ram usage"))

#print(cpuList)


def dataAnalysis(t):
  # integrated gpu will be part of cpu
  '''while t:
      print(t)
      time.sleep(1)
      currentData = fetch_dict(t)
      gpuList.append(currentData.get("gpu usage"))
      cpuList.append(currentData.get("cpu usage"))
      ramList.append(currentData.get("ram usage"))
      t -= 1
  '''
  values = []
  gpuAverage = mean(gpuList)
  cpuAverage = mean(cpuList)
  ramAverage = mean(ramList)
  power = gpuAverage + cpuAverage + ramAverage
  values.append(power)
  print(values[0], "Watts")
  return values

dataAnalysis(5)