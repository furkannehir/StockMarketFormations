from enum import IntEnum

epsilon = 0.00001

class Stock:
	def __init__(self, companyName, stockName):
		self.companyName = companyName
		self.stockName = stockName
		self.high = []
		self.low = []
		self.open = []
		self.close = []
		self.volume = []
		self.date = []
		self.trend = [] #increasing 2, decreasing 1, steady 0
		self.label = []
		self.pattern = []

	def addNewStat(self, high, low, openPrice, closePrice, volume, date, label=None, pattern=None):
		self.high.append(high)
		self.low.append(low)
		self.open.append(openPrice)
		self.close.append(closePrice)
		self.volume.append(volume)
		self.date.append(date)
		self.label.append(label)
		self.pattern.append(pattern)

	def stringToDoubleVariables(self):
		self.high = stringToDouble(self.high)
		self.low = stringToDouble(self.low)
		self.open = stringToDouble(self.open)
		self.close = stringToDouble(self.close)
		self.volume = stringToDouble(self.volume)
		self.label = stringToInt(self.label)

class Label:
	def __init__(self, label, pattern):
		self.label = label
		self.pattern = pattern
		self.data = []
	
	def addData(self, item):
		self.data.append(float(item))

def stringToDouble(strList):
	doubleList = []
	for item in strList:
		doubleList.append(float(item))
	return doubleList

def stringToInt(strList):
	intList = []
	for item in strList:
		intList.append(int(item))
	return intList

class StockIndex(IntEnum):
	companyName = 0
	stockName = 1
	high = 2
	low = 3
	openPrice = 4
	closePrice = 5
	volume = 6
	date = 7
	label = 8
	pattern = 9

	def __int__(self):
		return self.value

class FormationCompare():
	def __init__(self, formation, startPoint, endPoint, distance):
		self.formation = formation
		self.start = startPoint
		self.end = endPoint
		self.distance = distance

	def __str__(self):
		return 'formation: ' + str(self.formation) + ', start: ' + str(self.start) + ', end: ' + str(self.end) + ', distance: ' + str(self.distance)