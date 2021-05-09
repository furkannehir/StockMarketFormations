import csv
from StockClass import *
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np
from Similarity import similarity
from Identification import identification
from rulesets import *
import numpy as np
from operator import attrgetter
from Placement import *


#TODO similarity hesaplama
#TODO identification
#TODO formasyonun random olup olmaması
#TODO label'leri dynamic programming ile yerleştirme

formationList = 	{
						"Spike Top"				: createSpikeTop,
						"Head and Shoulder" 	: createHeadAndShoulders,
						"Double Top" 			: createDoubleTop, 
						"Double Bottom" 		: createDoubleBottom,
						"Ascending"				: createAscending,
						"Descending"			: createDescending
						}

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
