from math import sqrt
from operator import attrgetter
import numpy as np
import editdistance as ed

w1 = 0.6
w2 = 0.2
w3 = 0.2

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
    SP[0] = point(1, P[0])
    SP[n-1] = point(m, P[-1])
    adjPointList = maxAdjPoints(P, n) #Bunun yerine başka bir yol düşünülebilir
    for i in range(1, n-1):
        SP[i] = point(adjPointList[i-1].index + 1, P[adjPointList[i-1].index])
    SQ = []
    for i in range(len(Q)):
        SQ.append(point(i+1, Q[i]))
    return SP, SQ

def maxAdjPoints(P, n):
    adjPointList = []
    # maxAdjPointsRec(P,n-2,0,0,len(P)-1,adjPointList)
    p1 = point(0,P[0])
    p2 = point(len(P)-1, P[-1])
    for i in range(1, len(P)-2):
        p3 = point(i,P[i])
        # distance = w1*editDistance(p3, p1, p2) + w2*perpendicularDistance(p3, p1, p2) + w3*verticalDistance(p3, p1, p2)
        # distance = editDistance(p3, p1, p2)
        distance = w1*perpendicularDistance(p3, p1, p2) + (1-w1)*editDistance(p3, p1, p2)
        # distance = verticalDistance(p3, p1, p2)
        adjPointList.append(adjPoint(i, distance))
    adjPointList.sort(key=attrgetter('distance'), reverse=True)
    adjPointList = adjPointList[:n]
    adjPointList.sort(key=attrgetter('index'))
    return adjPointList

def editDistance(p3, p1, p2):
    return sqrt((p2.x - p3.x)*(p2.x - p3.x) + (p2.y - p3.y)*(p2.y - p3.y)) + sqrt((p1.x - p3.x)*(p1.x - p3.x) + (p1.y - p3.y)*(p1.y - p3.y))

def perpendicularDistance(p3, p1, p2):
    # _, xc, yc = slopeXcYc(p1, p2, p3)
    # print(xc)
    # return sqrt((xc-p3.x)*(xc-p3.x) + (yc-p3.y)*(yc-p3.y))
    p1 = (p1.x, p1.y)
    p2 = (p2.x, p2.y)
    p3 = (p3.x, p3.y)
    p1 = np.asarray(p1)
    p2 = np.asarray(p2)
    p3 = np.asarray(p3)
    return np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)

def verticalDistance(p3, p1, p2):
    _, _, yc = slopeXcYc(p1, p2, p3)
    return abs(yc -p3.y)

def slopeXcYc(p1, p2, p3):
    s = (p2.y - p1.y) / (p2.x -p1.x)
    xc = ((p3.x + s*p3.y + s*s*p2.x - s*p2.y) / (1 + s*s)) - (p3.x*p3.x)
    yc = s*xc - s*p2.x + p2.y
    return s, xc, yc

def maxAdjPointsRec(P, n, counter, left, right, SP):
    adjPointList = []
    if counter > n:
        return
    print('n: ' + str(n) + ' counter: ' + str(counter) + ' left:' + str(left) + ' right: ' + str(right))
    p1 = point(left,P[left])
    p2 = point(right, P[right])
    for i in range(left, right):
        p3 = point(i,P[i])
        # distance = w1*editDistance(p3, p1, p2) + w2*perpendicularDistance(p3, p1, p2) + w3*verticalDistance(p3, p1, p2)
        distance = w1*editDistance(p3, p1, p2) + (1-w1)*verticalDistance(p3, p1, p2)
        adjPointList.append(adjPoint(i, distance))
    adjPointList.sort(key=attrgetter('distance'), reverse=True)
    if adjPointList:
        SP.append(adjPointList[0])
        maxAdjPointsRec(P,n,2*counter+1,left,adjPointList[0].index,SP)
        maxAdjPointsRec(P,n,2*counter+2,adjPointList[0].index,right,SP)

if __name__ == '__main__':
    P = [2,3,5,6,10,12,15,14,12,9,8,6,4,7,10,13,16,12,10,5]
    Q = [2,5,10,15,12,9,6,7,10,13,16,12,10,5]
    Q2 = [1,2,3,4,5]
    SP, Q = identification(P,Q)
    print(SP)