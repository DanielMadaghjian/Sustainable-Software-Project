from statistics import mean
import time
import backend_getData
import requests
import json

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


headers = {
    'Authorization': 'Bearer VDK57KAYZ7MT1AM7NQD1MPX6PMQQ',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = '{\n  "emission_factor": {\n    "id": "electricity-energy_source_grid_mix",\n    "region": "IE"\n  },\n  "parameters": {\n    "energy": 0.001,\n    "energy_unit": "kWh"\n  }\n}'

response = requests.post('https://beta3.api.climatiq.io/estimate', headers=headers, data=data)
output = response.json()

with open('{}.json'.format("test"), 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

print(output)