from math import sqrt
from operator import attrgetter

w1 = 0.3
w2 = 0.3
w3 = 0.4

class point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class adjPoint():
    def __init__(self, index, distance):
        self.index = index
        self.distance = distance

    def __str__(self):
        return 'index: ' + str(self.index) + ', distance: ' + str(self.distance)

def identification(P, Q):
    assert len(P) >= len(Q)
    m = len(P)
    n = len(Q)
    SP = [None]*n
    SP[0] = P[0]
    SP[n-1] = P[m-1]
    adjPointList = maxAdjPoints(P, n) #Bunun yerine başka bir yol düşünülebilir
    for i in range(1, n-1):
        SP[i] = P[adjPointList[i].index]
    return SP

def maxAdjPoints(P, n):
    adjPointList = []
    p1 = point(0,P[0])
    p2 = point(len(P)-1, P[-1])
    for i in range(1, len(P)-1):
        p3 = point(i,P[i])
        distance = w1*editDistance(p3, p1, p2) + w2*perpendicularDistance(p3, p1, p2) + w3*verticalDistance(p3, p1, p2)
        adjPointList.append(adjPoint(i, distance))
    adjPointList.sort(key=attrgetter('distance'), reverse=True)
    adjPointList = adjPointList[:n]
    adjPointList.sort(key=attrgetter('index'))
    return adjPointList

def editDistance(p3, p1, p2):
    return sqrt((p2.x - p3.x)*(p2.x - p3.x) + (p2.y - p3.y)*(p2.y - p3.y)) + sqrt((p1.x - p3.x)*(p1.x - p3.x) + (p1.y - p3.y)*(p1.y - p3.y))

def perpendicularDistance(p3, p1, p2):
    _, xc, yc = slopeXcYc(p1, p2, p3)
    return sqrt((xc-p3.x)*(xc-p3.x) + (yc-p3.y)*(yc-p3.y))

def verticalDistance(p3, p1, p2):
    _, _, yc = slopeXcYc(p1, p2, p3)
    return abs(yc -p3.y)

def slopeXcYc(p1, p2, p3):
    s = (p2.y - p1.y) / (p2.x -p1.x)
    xc = ((p3.x + s*p3.y + s*s*p2.x + s*p2.y) / (1 + s*s)) - (p3.x*p3.x)
    yc = s*xc - s*p2.x + p2.y
    return s, xc, yc


if __name__ == '__main__':
    P = [2,3,5,6,10,12,15,14,12,9,8,6,4,7,10,13,16,12,10,5]
    Q = [2,5,10,15,12,9,6,7,10,13,16,12,10,5]
    SP = identification(P,Q)
    print(SP)