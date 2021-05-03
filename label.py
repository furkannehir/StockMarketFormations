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

differentFormations = 	{
						"Spike Top"				: createSpikeTop,
						"Head and Shoulder" 	: createHeadAndShoulders,
						"Double Top" 			: createDoubleTop, 
						"Double Bottom" 		: createDoubleBottom
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
																			row[StockIndex.openPrice.value], row[StockIndex.closePrice.value],
																			row[StockIndex.volume.value], row[StockIndex.date.value],
																			row[StockIndex.label.value], row[StockIndex.pattern.value])
	return myBeautifulDictionary

def increaseDecrease(dictionary):
	for key in dictionary:
		item = dictionary[key]
		item.stringToDoubleVariables()
		for i in range(len(item.close)):
			if i == 0:
				item.trend.append(0)
			else:
				if item.close[i] > item.close[i-1] + epsilon:
					item.trend.append(2)
				elif item.close[i] < item.close[i-1] - epsilon:
					item.trend.append(1)
				else:
					item.trend.append(0)

def splitDictionary(stockMarketDict):
	doubleBottom = Label(0, 'double bottom')
	doubleTop = Label(1, 'double top')
	invHeAndSho = Label(2, 'inverse head and shoulders')
	ascending = Label(3, 'ascending')
	cupWHandle = Label(4, 'cup with handle')
	descending = Label(5, 'descending')
	wedge = Label(6, 'wedge')
	ascending2 = Label(3, 'ascending')
	doubleTop2 = Label(1, 'double top')
	descending2 = Label(5, 'descending')
	stockCloseData = stockMarketDict['VIE'].close
	for i in range(len(stockCloseData)):
		if i < 27:
			doubleBottom.addData(stockCloseData[i])
		if i < 44:
			doubleTop.addData(stockCloseData[i])
		if i < 66:
			invHeAndSho.addData(stockCloseData[i])
		if i < 106:
			ascending.addData(stockCloseData[i])
		if i < 146:
			cupWHandle.addData(stockCloseData[i])
		if i < 186:
			descending.addData(stockCloseData[i])
		if i < 249:
			wedge.addData(stockCloseData[i])
		if i < 274:
			ascending2.addData(stockCloseData[i])
		if i < 304:
			doubleTop2.addData(stockCloseData[i])
		else:
			descending2.addData(stockCloseData[i])
	return doubleTop.data, doubleTop2.data, invHeAndSho.data

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
    # print (matrix)
    return (matrix[size_x - 1, size_y - 1])

def main():
	stockMarketDict = readFileAndFillDictionary('../datasets/CAC40/Veolia.csv')
	for stock in stockMarketDict:
		stockData = stockMarketDict[stock].close
		similarityList = []
		for key in differentFormations:
			formation = differentFormations[key](500)
			w = 10
			while w < len(stockData):
				start = 0
				while start < len(stockData)-w:
					marketData = getDictionaryData(stockData, start, start+w)
					if len(marketData) > len(formation):
						marketDataS, formationS = identification(marketData, formation)
					else:
						formationS, marketDataS = identification(formation, marketData)
					distance = similarity(marketDataS, formationS)
					similarityList.append(FormationCompare(key, start, start+w, distance))
					start += w
				w += 1
		similarityList.sort(key=attrgetter('distance'))
		for item in similarityList:
			print(item)
		plt.plot(stockData, label=similarityList[0].formation)
		plt.legend()
		plt.show()


	# stockMarketDict = readFileAndFillDictionary('../datasets/CAC40/Veolia.csv')
	# print(stockMarketDict.keys())
	# sameOne, sameTwo, different = splitDictionary(stockMarketDict)
	# increaseDecrease(stockMarketDict)
	# print(len(sameOne), len(sameTwo), len(different))
	# sameTwoS, sameOne = identification(sameTwo, sameOne)
	# result = similarity(sameOne, sameTwoS)
	# print("same: ", result)
	# sameTwoS, different = identification(sameTwo, different)
	# result = similarity(different, sameTwoS)
	# print("different: ", result)
	# doubleTop = createDoubleTop(500)
	# doubleTopS, sameOne3 = identification(doubleTop, sameOne)
	# print(type(doubleTopS[0]), type(sameOne[0]))
	# result = similarity(doubleTopS, sameOne)
	# print("artificial: ", result)

if __name__ == "__main__":
	main()
