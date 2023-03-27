from statistics import mean
import time
import backend_getData
import requests
import json

graphList = []

# Method that calculates the average power 
def getPower(gpuList, cpuList, ramList):
  gpuAverage = mean(gpuList)
  cpuAverage = mean(cpuList)
  ramAverage = mean(ramList)
  power = gpuAverage + cpuAverage + ramAverage
  return power

def getCarbon(region):#add a country here
  headers = {
    'Authorization': 'Bearer ZF80SPH7WHM6CJQG0J9KQ4QR3Q5Z',
    'Content-Type': 'application/x-www-form-urlencoded',
  }

  data = '{\n  "emission_factor": {\n    "id": "electricity-energy_source_grid_mix",\n    "region": "' + region + '"\n  },\n  "parameters": {\n    "energy": 0.001,\n    "energy_unit": "kWh"\n  }\n}'

  #remove after finish
  response = requests.post('https://beta3.api.climatiq.io/estimate', headers=headers, data=data)
  output = response.json()

  with open('{}.json'.format("test"), 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)
  f = open('test.json')
  carbon = json.load(f)
  emission = carbon.get("co2e")
  #print(emission)
  return emission

# Method that collects the raw data and filters it
def dataAnalysis(t, country):#add a country here
  gpuList = [] 
  cpuList = [] 
  ramList = []
  if len(graphList) == 40:
    graphList.clear()
  while t:
      print(t)
      #time.sleep(0.01)
      currentData = backend_getData.fetch_dict()
      graphList.append(currentData.get("gpu usage") + currentData.get("cpu usage") + currentData.get("ram usage"))
      #gpuList.append(currentData.get("gpu usage"))
      #cpuList.append(currentData.get("cpu usage"))
      #ramList.append(currentData.get("ram usage"))
      t -= 2    

  currentData = backend_getData.fetch_dict()
  graphList.append(currentData.get("gpu usage") + currentData.get("cpu usage") + currentData.get("ram usage"))
  gpuList.append(currentData.get("gpu usage"))
  cpuList.append(currentData.get("cpu usage"))
  ramList.append(currentData.get("ram usage"))    
  
  values = []
  power = getPower(gpuList, cpuList, ramList)
  values.append(power)
  emission = getCarbon(country) * power
  values.append(emission)

  values.append(mean(gpuList)) # adds gpu value (position 2)
  values.append(mean(cpuList)) # adds cpu value (position 3)
  values.append(mean(ramList)) # adds gpu value (position 4)
  values.append(len(graphList))
  values = values + graphList


  #print(values[0])
  #print(values[1])
  #print("Auxiliary Values")
  #print(values[2])
  #print(values[3])
  #print(values[4])
  #print(values)
  return values

dataAnalysis(2,'IE')