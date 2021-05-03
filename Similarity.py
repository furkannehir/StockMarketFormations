from Identification import *
from matplotlib import pyplot as plt
from rulesets import *

w1 = 0.5

#TODO temporal distance
#TODO point objects for temporal distance

def similarity(SP,Q):
    assert len(SP) == len(Q)
    return w1*amplitudeDistance(SP,Q) + (1-w1)*temporalDistance(SP,Q)
    # return amplitudeDistance(SP,Q)

def amplitudeDistance(SP, Q):
    ad = 0
    n = len(SP)
    for i in range(n):
        ad += (SP[i].y-Q[i].y)*(SP[i].y-Q[i].y)
    return sqrt((1/n)*ad)

def temporalDistance(SP,Q):
    td = 0
    n = len(SP)
    for i in range(1,n):
        td += (SP[i].x-Q[i].x)*(SP[i].x-Q[i].x)
    return sqrt((1/(n-1))*td)

if __name__=='__main__':
    P = createDoubleTop(500)
    Q = createDoubleTop(100)
    Q2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    SP, Q = identification(P,Q)
    print(similarity(SP,Q))

    SP, Q2 = identification(P,Q2)
    print(similarity(SP,Q2))