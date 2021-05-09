
def greedyPlacementDistancePriority(stockMarketData, similarityList):
    labeledArray = [0]*len(stockMarketData.close)
    labeled = 0
    for item in similarityList:
        if checkIfAvaliable(labeledArray, item.start, item.end):
            for i in range(item.start, item.end):
                labeledArray[i] = 1
                labeled += 1
                stockMarketData.label[i] = item.formation
    print("Labeled %" + str((labeled/len(labeledArray))*100) + " of the data.")
    return stockMarketData

def greedyPlacementPercentagePriority(stockMarketData, similarityList):
    labeledArray = [0]*len(stockMarketData.close)
    labeled = 0
    start = 0
    while start < len(labeledArray):
        similarityObj = None
        while similarityObj == None:
            similarityObj = bestPlacementForThatPosition(start, similarityList)
            start += 1
            if start >= len(labeledArray):
                print("Labeled %" + str((labeled/len(labeledArray))*100) + " of the data.")
                return stockMarketData
        for i in range(similarityObj.start, similarityObj.end):
            labeledArray[i] = 1
            labeled += 1
            stockMarketData.label[i] = similarityObj.formation
        start = similarityObj.end+1
    print("Labeled %" + str((labeled/len(labeledArray))*100) + " of the data.")
    return stockMarketData
                

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