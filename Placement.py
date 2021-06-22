
from rulesets import formationLabelNumber

correctPoint = 5

def greedyPlacementDistancePriority(stockMarketData, similarityList):
    log = ''
    labeledArray = [0]*len(stockMarketData.close)
    labeled = 0
    correct = 0
    total = 0
    for item in similarityList:
        if checkIfAvaliable(labeledArray, item.start, item.end):
            for i in range(item.start, item.end):
                total += 1
                if item.distance < correctPoint:
                    correct += 1
                labeledArray[i] = 1
                labeled += 1
                stockMarketData.label[i] = item.formationNo
                stockMarketData.pattern[i] = item.formation
    log += "Labeled %" + str((labeled/len(labeledArray))*100) + " of the data."
    log += "Accuracy: %" + str((correct/total)*100)
    for i in range(len(labeledArray)):
        if labeledArray[i] == 0:
            stockMarketData.label[i] = formationLabelNumber["None"]
            stockMarketData.pattern[i] = "None"
    return stockMarketData, log

def greedyPlacementPercentagePriority(stockMarketData, similarityList):
    log = ''
    labeledArray = [0]*len(stockMarketData.close)
    labeled = 0
    start = 0
    while start < len(labeledArray):
        similarityObj = None
        while similarityObj == None:
            similarityObj = bestPlacementForThatPosition(start, similarityList)
            start += 1
            if start >= len(labeledArray):
                for i in range(len(labeledArray)):
                    if labeledArray[i] == 0:
                        stockMarketData.label[i] = stockMarketData.label[i-1]
                        stockMarketData.pattern[i] = stockMarketData.pattern[i-1]
                        labeled +=1
                log += "Labeled %" + str((labeled/len(labeledArray))*100) + " of the data."
                return stockMarketData
        for i in range(similarityObj.start, similarityObj.end):
            labeledArray[i] = 1
            labeled += 1
            stockMarketData.label[i] = similarityObj.formationNo
            stockMarketData.pattern[i] = similarityObj.formation
        start = similarityObj.end
    for i in range(len(labeledArray)):
        if labeledArray[i] == 0:
            stockMarketData.label[i] = stockMarketData.label[i-1]
            stockMarketData.pattern[i] = stockMarketData.pattern[i-1]
            labeled +=1
    log += "Labeled %" + str((labeled/len(labeledArray))*100) + " of the data."
    return stockMarketData, log
                

def checkIfAvaliable(array, start, end):
    assert start >= 0
    assert end < len(array)
    for i in range(start, end):
        if array[i] != 0:
            return False
    return True

def bestPlacementForThatPosition(start, similarityList):
    for item in similarityList:
        if item.start == start:
            return item
    return None