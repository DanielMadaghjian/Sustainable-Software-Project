from analysis import dataAnalysis, getPower


def testFunction():
    gpuList = []
    cpuList = []
    ramList = []


    sample1 = {
        "gpu usage": 5,
        "cpu usage": 5,
        "ram usage": 5
    }
    
    gpuList.append(sample1.get("gpu usage"))
    cpuList.append(sample1.get("cpu usage"))
    ramList.append(sample1.get("ram usage"))
    
    sample2 = {
        "gpu usage": 5,
        "cpu usage": 5,
        "ram usage": 5
    }
    
    gpuList.append(sample2.get("gpu usage"))
    cpuList.append(sample2.get("cpu usage"))
    ramList.append(sample2.get("ram usage"))
    
    sample3 = {
        "gpu usage": 5,
        "cpu usage": 5,
        "ram usage": 5
    }
    
    gpuList.append(sample3.get("gpu usage"))
    cpuList.append(sample3.get("cpu usage"))
    ramList.append(sample3.get("ram usage"))
    
    sample4 = {
        "gpu usage": 5,
        "cpu usage": 5,
        "ram usage": 5
    }
    
    gpuList.append(sample4.get("gpu usage"))
    cpuList.append(sample4.get("cpu usage"))
    ramList.append(sample4.get("ram usage"))
    
    sample5 = {
        "gpu usage": 5,
        "cpu usage": 5,
        "ram usage": 5
    }
    
    gpuList.append(sample5.get("gpu usage"))
    cpuList.append(sample5.get("cpu usage"))
    ramList.append(sample5.get("ram usage"))
    
    sample6 = {
        "gpu usage": 5,
        "cpu usage": 5,
        "ram usage": 5
    }
    
    gpuList.append(sample6.get("gpu usage"))
    cpuList.append(sample6.get("cpu usage"))
    ramList.append(sample6.get("ram usage"))
    
    sample7 = {
        "gpu usage": 5,
        "cpu usage": 5,
        "ram usage": 5
    }
    
    gpuList.append(sample7.get("gpu usage"))
    cpuList.append(sample7.get("cpu usage"))
    ramList.append(sample7.get("ram usage"))
    
    sample8 = {
        "gpu usage": 5,
        "cpu usage": 5,
        "ram usage": 5
    }
    
    gpuList.append(sample8.get("gpu usage"))
    cpuList.append(sample8.get("cpu usage"))
    ramList.append(sample8.get("ram usage"))
    
    sample9 = {
        "gpu usage": 5,
        "cpu usage": 5,
        "ram usage": 5
    }
    
    gpuList.append(sample9.get("gpu usage"))
    cpuList.append(sample9.get("cpu usage"))
    ramList.append(sample9.get("ram usage"))
    
    sample10 = {
        "gpu usage": 5,
        "cpu usage": 5,
        "ram usage": 5
    }
    
    gpuList.append(sample10.get("gpu usage"))
    cpuList.append(sample10.get("cpu usage"))
    ramList.append(sample10.get("ram usage"))
    
    result = getPower(gpuList, cpuList, ramList)
    assert result == 15  # add assertion here
