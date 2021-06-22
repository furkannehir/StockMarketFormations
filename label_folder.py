import os
from Label import labelByTwenty

files = os.listdir('./dataset')
datadir = 'dataset/'
labeled = []
for filepath in files:
    if filepath.__contains__('_labeled'):
        print('added', filepath)
        labeled.append(filepath.split('_')[0])
print(labeled)
for filepath in files:
    stockname = filepath.split('.')[0]
    filepath = datadir + filepath
    print('stockname',stockname)
    if not filepath.__contains__('_labeled') and not labeled.__contains__(stockname):
        print('working on', filepath)
        labelByTwenty(filepath)
    else:
        print('skipped', stockname)

def getStockNameList(fileList, dir):
	stocks = []
	for filepath in fileList:
		if filepath.__contains__('_labeled'):
			stocks.append((filepath.split('_')[0], dir + filepath))
	return stocks


datadir = './dataset_CAC40'
files = os.listdir(datadir)

stocks = getStockNameList(files, 'dataset_CAC40/')
print(stocks)