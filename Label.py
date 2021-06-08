import csv
from StockMarketFormations.StockClass import *
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np
from StockMarketFormations.Similarity import similarity
from StockMarketFormations.Identification import identification
from StockMarketFormations.rulesets import *
import numpy as np
from operator import attrgetter
from StockMarketFormations.Placement import *
import pandas as pd
import os

#TODO similarity hesaplama
#TODO identification
#TODO formasyonun random olup olmaması
#TODO label'leri dynamic programming ile yerleştirme
#TODO excel'e kaydetme formasyonları

def readFileAndFillDictionary(filename):
	myBeautifulDictionary = {}
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		firstRow = True
		for row in csv_reader:
			if firstRow:
				firstRow = False
			else:
				if row[StockIndex.stockName.value] not in myBeautifulDictionary:
					myBeautifulDictionary[row[StockIndex.stockName.value]] = Stock(row[StockIndex.companyName.value], row[StockIndex.stockName.value])
				myBeautifulDictionary[row[StockIndex.stockName.value]].addNewStat(row[StockIndex.high.value], row[StockIndex.low.value], 
																			row[StockIndex.openPrice.value], float(row[StockIndex.closePrice.value]),
																			row[StockIndex.volume.value], row[StockIndex.date.value])
	return myBeautifulDictionary

def getDictionaryData(bigData, start, end):
	data = []
	assert start >= 0 and end < len(bigData)
	for i in range(start, end):
		data.append(bigData[i])
	return data


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])

def createDataFrameObj(stockMarketData):
	dataFrameDict = {}
	dataFrameDict['CompanyName'] = [stockMarketData.companyName]*len(stockMarketData.close)
	dataFrameDict['StockName'] = [stockMarketData.stockName]*len(stockMarketData.close)
	dataFrameDict['High'] = stockMarketData.high
	dataFrameDict['Low'] = stockMarketData.low
	dataFrameDict['Open'] = stockMarketData.open
	dataFrameDict['Close'] = stockMarketData.close
	dataFrameDict['Volume'] = stockMarketData.volume
	dataFrameDict['Date'] = stockMarketData.date
	dataFrameDict['Label'] = stockMarketData.label
	dataFrameDict['Pattern'] = stockMarketData.pattern
	dataFrameObj = pd.DataFrame(data=dataFrameDict)
	print(dataFrameObj.columns)
	return dataFrameObj

def saveLabeledDataToCSV(stockMarketData, filename):
	fileNamelList = filename.split('.')
	labeledFileName = ''
	for i in range(len(fileNamelList)-1):
		labeledFileName += fileNamelList[i]
	if os.path.exists(labeledFileName):
	    os.remove(labeledFileName)
	with open(filename.split('.')[0]+'_labeled.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["CompanyName","StockName","High","Low","Open","Close","Volume","Date","Label","Pattern"])
		for i in range(len(stockMarketData.close)):
			writer.writerow([stockMarketData.companyName,
							stockMarketData.stockName,
							stockMarketData.high[i],
							stockMarketData.low[i],
							stockMarketData.open[i],
							stockMarketData.close[i],
							stockMarketData.volume[i],
							stockMarketData.date[i],
							stockMarketData.label[i],
							stockMarketData.pattern[i]])

def labelDataAsDataFrameObj(filename):
	stockMarketDict = readFileAndFillDictionary(filename)
	for stock in stockMarketDict:
		stockMarketData = stockMarketDict[stock]
		stockData = stockMarketData.close
		similarityList = []
		epoch = 0
		for key in formationList:
			w = 10
			print('formation: ' + str(key))
			epochFormation = 0
			formation = formationList[key](200)
			while w < len(stockData):
				start = 0
				if epoch%10 == 0:
					print('epoch: ' + str(epoch) + ', epoch for this formation: ' + str(epochFormation) + ', window: ' + str(w))
				while start < len(stockData)-w:
					marketData = getDictionaryData(stockData, start, start+w)
					if len(marketData) > len(formation):
						marketDataS, formationS = identification(marketData, formation)
					else:
						formationS, marketDataS = identification(formation, marketData)
					distance = similarity(marketDataS, formationS)
					similarityList.append(FormationCompare(key, formationLabelNumber[key], start, start+w, distance))
					start += 1
				epoch += 1
				w += 5
		similarityList.sort(key=attrgetter('distance'))
		stockMarketData = greedyPlacementDistancePriority(stockMarketData, similarityList)
		saveLabeledDataToCSV(stockMarketData, filename)
		return createDataFrameObj(stockMarketData)

def main():
	stockMarketDict = readFileAndFillDictionary('../datasets/CAC40/Veolia.csv')
	for stock in stockMarketDict:
		stockMarketData = stockMarketDict[stock]
		stockData = stockMarketData.close
		similarityList = []
		for key in formationList:
			w = 10
			while w < len(stockData):
				start = 0
				while start < len(stockData)-w:
					marketData = getDictionaryData(stockData, start, start+w)
					formation = formationList[key](w, float(marketData[0]))
					if len(marketData) > len(formation):
						marketDataS, formationS = identification(marketData, formation)
					else:
						formationS, marketDataS = identification(formation, marketData)
					distance = similarity(marketDataS, formationS)
					similarityList.append(FormationCompare(key, start, start+w, distance))
					start += 1
				w += 5
		similarityList.sort(key=attrgetter('distance'))
		# for item in similarityList:
		# 	print(item)
		stockMarketData = greedyPlacementDistancePriority(stockMarketData, similarityList)
		stockMarketData = greedyPlacementPercentagePriority(stockMarketData, similarityList)
		# for i in range(len(stockMarketData.label)):
		# 	print("index: " + str(i) + " label: " + str(stockMarketData.label[i]))

if __name__ == "__main__":
	main()
