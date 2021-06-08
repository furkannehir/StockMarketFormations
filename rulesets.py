from random import uniform, randint
import matplotlib.pyplot as plt

def createSpikeTop(n, startPoint=None):
    assert n >= 10
    maxChange = 60/n
    spikeTop = []
    splits = n//4
    # spikePoint = randint(n//3, 2*n//3)
    if startPoint is None:
        startPoint = uniform(20,30)
    startPoint = steady(spikeTop, splits, startPoint, maxChange)
    startPoint = increase(spikeTop, splits, startPoint, maxChange)
    startPoint = decrease(spikeTop, splits, startPoint, maxChange)
    steady(spikeTop, splits, startPoint, maxChange)
    return spikeTop

def createHeadAndShoulders(n, startPoint=None):
    assert n >= 10
    maxChange = 40/n
    headAndShoulders = []
    if startPoint is None:
        startPoint = uniform(20,30)
    s1 = n//5
    b1 = n//10
    h = n//5
    b2 = n//5
    s2 = n//10
    rest = n - (s1+s2+b1+b2+h)
    startPoint = increase(headAndShoulders, s1, startPoint, maxChange)
    startPoint = decrease(headAndShoulders, b1, startPoint, maxChange)
    startPoint = increase(headAndShoulders, h, startPoint, maxChange)
    startPoint = decrease(headAndShoulders, b2, startPoint, maxChange)
    startPoint = increase(headAndShoulders, s2, startPoint, maxChange)
    startPoint = decrease(headAndShoulders, rest, startPoint, maxChange)
    return headAndShoulders

def createDoubleTop(n, startPoint=None):
    assert n >= 10
    maxChange = 50/n
    doubleTop = []
    if startPoint is None:
        startPoint = uniform(20,30)
    change = n//4
    startPoint = increase(doubleTop, change, startPoint, maxChange)
    startPoint = decrease(doubleTop, change, startPoint, maxChange)
    startPoint = increase(doubleTop, change, startPoint, maxChange)
    startPoint = decrease(doubleTop, change, startPoint, maxChange)
    return doubleTop

def createDoubleBottom(n, startPoint=None):
    assert n >= 10
    maxChange = 50/n
    doubleBottom = []
    if startPoint is None:
        startPoint = uniform(20,30)
    change = n//4
    startPoint = decrease(doubleBottom, change, startPoint, maxChange)
    startPoint = increase(doubleBottom, change, startPoint, maxChange)
    startPoint = decrease(doubleBottom, change, startPoint, maxChange)
    startPoint = increase(doubleBottom, change, startPoint, maxChange)
    return doubleBottom

def createAscending(n, startPoint=None):
    assert n >= 10
    maxChange = 50/n
    ascending = []
    if startPoint is None:
        startPoint = uniform(20,30)
    increase(ascending, n, startPoint, maxChange)
    return ascending

def createDescending(n, startPoint=None):
    assert n >= 10
    maxChange = 50/n
    descending = []
    if startPoint is None:
        startPoint = uniform(30,40)
    decrease(descending, n, startPoint, maxChange)
    return descending

def increase(arr, n, startPoint, maxChange):
    for i in range(n):
        num = randint(1,100)
        incDec = uniform(0,maxChange)
        if num <= 95:
            startPoint += incDec
        else:
            startPoint -= incDec
        arr.append(startPoint)
    return startPoint

def decrease(arr, n, startPoint, maxChange):
    for i in range(n):
        num = randint(1,100)
        incDec = uniform(0,maxChange)
        if num <= 95:
            startPoint -= incDec
        else:
            startPoint += incDec
        arr.append(startPoint)
    return startPoint

def steady(arr, n, startPoint, maxChange):
    for i in range(n):
        num = randint(1,100)
        incDec = uniform(0,maxChange)
        if num <= 50:
            startPoint -= incDec
        else:
            startPoint += incDec
        arr.append(startPoint)
    return startPoint

formationList = 	{
						"Spike Top"				: createSpikeTop,
						"Head and Shoulder" 	: createHeadAndShoulders,
						"Double Top" 			: createDoubleTop, 
						"Double Bottom" 		: createDoubleBottom,
						"Ascending"				: createAscending,
						"Descending"			: createDescending
}

formationLabelNumber = {
						"None"					: 1,
						"Spike Top"				: 2,
						"Head and Shoulder" 	: 3,
						"Double Top" 			: 4, 
						"Double Bottom" 		: 5,
						"Ascending"				: 6,
						"Descending"			: 7
}


if __name__=='__main__':
    has = createHeadAndShoulders(500,30)
    st = createSpikeTop(500,30)
    dt = createDoubleTop(500,30)
    bt = createDoubleBottom(500,30)
    asc = createAscending(500,30)
    dsc = createDescending(500,30)
    plt.plot(has, label='headAndShoulders')
    plt.plot(st, label='spikeTop')
    plt.plot(dt, label='doubleTop')
    plt.plot(bt, label='doubleBottom')
    # plt.plot(asc, label='ascending')
    # plt.plot(dsc, label='descending')
    plt.legend()
    plt.show()
