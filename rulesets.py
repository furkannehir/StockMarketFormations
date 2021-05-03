from random import uniform, randint
import matplotlib.pyplot as plt

def createSpikeTop(n):
    assert n > 20
    maxChange = 40/n
    spikeTop = []
    spikePoint = randint(n//4, 3*n//4)
    startPoint = uniform(10,20)
    startPoint = increase(spikeTop, spikePoint, startPoint, maxChange)
    spikeTop.append(startPoint*1.003)
    decrease(spikeTop, n-spikePoint, startPoint, maxChange)
    return spikeTop

def createHeadAndShoulders(n):
    assert n > 20
    maxChange = 40/n
    headAndShoulders = []
    startPoint = uniform(10,20)
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

def createDoubleTop(n):
    assert n > 20
    maxChange = 50/n
    doubleTop = []
    startPoint = uniform(10,20)
    change = n//4
    startPoint = increase(doubleTop, change, startPoint, maxChange)
    startPoint = decrease(doubleTop, change, startPoint, maxChange)
    startPoint = increase(doubleTop, change, startPoint, maxChange)
    startPoint = decrease(doubleTop, change, startPoint, maxChange)
    return doubleTop

def createDoubleBottom(n):
    assert n > 20
    maxChange = 50/n
    doubleBottom = []
    startPoint = uniform(20,30)
    change = n//4
    startPoint = decrease(doubleBottom, change, startPoint, maxChange)
    startPoint = increase(doubleBottom, change, startPoint, maxChange)
    startPoint = decrease(doubleBottom, change, startPoint, maxChange)
    startPoint = increase(doubleBottom, change, startPoint, maxChange)
    return doubleBottom

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

if __name__=='__main__':
    has = createHeadAndShoulders(500)
    st = createSpikeTop(500)
    dt = createDoubleTop(500)
    bt = createDoubleBottom(500)
    plt.plot(has, label='headAndShoulders')
    plt.plot(st, label='spikeTop')
    plt.plot(dt, label='doubleTop')
    plt.plot(bt, label='doubleBottom')
    plt.legend()
    plt.show()
