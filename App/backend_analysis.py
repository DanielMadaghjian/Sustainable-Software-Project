from statistics import mean
import time
import backend_getData
import requests
import json

graphList = []

baseLineData = []
gpuBaseLine = []
cpuBaseLine = []
ramBaseLine = []

# Method that calculates the average power usaage from gpu, cpu and ram
def getPower(gpuList, cpuList, ramList):
  gpuAverage = mean(gpuList)
  cpuAverage = mean(cpuList)
  ramAverage = mean(ramList)
  power = gpuAverage + cpuAverage + ramAverage
  return power

## Method that gets the carbon emissions from the Climatiq API

def getCarbon(region):#add a country here
  headers = {
    'Authorization': 'Bearer ZF80SPH7WHM6CJQG0J9KQ4QR3Q5Z',
    'Content-Type': 'application/x-www-form-urlencoded',
  }

  data = '{\n  "emission_factor": {\n    "id": "electricity-energy_source_grid_mix",\n    "region": "' + region + '"\n  },\n  "parameters": {\n    "energy": 0.001,\n    "energy_unit": "kWh"\n  }\n}'

  #remove after finish
  try:
    response = requests.post('https://beta3.api.climatiq.io/estimate', headers=headers, data=data)
    if(str(response)=='<Response [400]>'):
      print("The request was unacceptable, probably due to missing a required parameter")
      exit()
    if(str(response)=='<Response [401]>'):
      print("No valid API key was provided")
      exit()
    if(str(response)=='<Response [404]>'):
      print("The requested resource doesn't exist")
      exit()
    if(str(response)=='<Response [5xx]>'):
      print("Something went wrong on our servers")
      exit()
    output = response.json()
    with open('{}.json'.format("test"), 'w', encoding='utf-8') as f:
      json.dump(output, f, ensure_ascii=False, indent=4)
    f = open('test.json')
    carbon = json.load(f)
    emission = carbon.get("co2e")
    #print(emission)
  except:
    emission = "API CONNECTION ERROR"
  print(emission)
  return emission

## Method that measures the power and emissions of laptop, used to get a baseline
def getBaseLine(region):
  baseLineData.clear()
  power = getPower(gpuBaseLine, cpuBaseLine, ramBaseLine)
  
  carbon = getCarbon(region)
  if isinstance(carbon, int):
    emission = carbon * power
  else:
    emission = carbon

  baseLineData.append(power)
  baseLineData.append(emission)
  baseLineData.append(mean(gpuBaseLine)) # adds gpu value (position 2)
  baseLineData.append(mean(cpuBaseLine)) # adds cpu value (position 3)
  baseLineData.append(mean(ramBaseLine)) # adds gpu value (position 4)
  gpuBaseLine.clear()
  cpuBaseLine.clear()
  ramBaseLine.clear()

  return baseLineData

## Method that measures the power and emissions of an app, baseline has to be called first
def getApp(region):

  data2 = []
  power = getPower(gpuBaseLine, cpuBaseLine, ramBaseLine)
  
  carbon = getCarbon(region)
  if isinstance(carbon, int):
    emission = carbon * power
  else:
    emission = carbon
    
  data2.append(power)
  data2.append(emission)
  data2.append(mean(gpuBaseLine)) # adds gpu value (position 2)
  data2.append(mean(cpuBaseLine)) # adds cpu value (position 3)
  data2.append(mean(ramBaseLine)) # adds gpu value (position 4)

  appData = []
  appData.append(data2[0]- baseLineData[0]) ## overall power for the app
  if isinstance(data2[1], str) or isinstance(baseLineData[1],str):
    appData.append("API Connection Error")
  else:
    appData.append(data2[1]-baseLineData[1]) ## emissions
  appData.append(data2[2]-baseLineData[2]) ## gpu
  appData.append(data2[3]- baseLineData[3]) ## cpu
  appData.append(data2[4]-baseLineData[4]) ## ram

  gpuBaseLine.clear()
  cpuBaseLine.clear()
  ramBaseLine.clear()

  return appData, baseLineData, data2
  
## Method that collects the raw data and filters it
def dataGathering():
  currentData = backend_getData.fetch_dict()
  gpuBaseLine.append(currentData.get("gpu usage"))
  cpuBaseLine.append(currentData.get("cpu usage"))
  ramBaseLine.append(currentData.get("ram usage"))

## Method that calls functions to get data, and converts it to emissions and power, also returns the raw data from graphing
def dataAnalysis(t, country):#add a country here
  gpuList = [] 
  cpuList = [] 
  ramList = []
  if len(graphList) == 40:
    graphList.clear()
  while t:
      print(t)
      currentData = backend_getData.fetch_dict()
      graphList.append(currentData.get("gpu usage") + currentData.get("cpu usage") + currentData.get("ram usage"))
      t -= 2    

  currentData = backend_getData.fetch_dict()
  graphList.append(currentData.get("gpu usage") + currentData.get("cpu usage") + currentData.get("ram usage"))
  gpuList.append(currentData.get("gpu usage"))
  cpuList.append(currentData.get("cpu usage"))
  ramList.append(currentData.get("ram usage"))    
  
  values = []
  power = getPower(gpuList, cpuList, ramList)
  values.append(power)
  carbon = getCarbon(country)
  if isinstance(carbon, int):
    emission = carbon * power
  else:
    emission = carbon
  values.append(emission)

  values.append(mean(gpuList)) # adds gpu value (position 2)
  values.append(mean(cpuList)) # adds cpu value (position 3)
  values.append(mean(ramList)) # adds gpu value (position 4)
  values.append(len(graphList))
  values = values + graphList

  return values

##dataAnalysis(2,'IE')
