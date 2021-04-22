from Identification import *

w1 = 0.5

#TODO temporal distance
#TODO point objects for temporal distance

def similarity(SP,Q):
    assert len(SP) == len(Q)
    # return w1*amplitudeDistance(SP,Q) + (1-w1)*temporalDistance(SP,Q)
    return amplitudeDistance(SP,Q)

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
    P = [2,3,5,6,10,12,15,14,12,9,8,6,4,7,10,13,16,12,10,5]
    Q = [2,5,10,15,12,9,6,7,10,13,16,12,10,5]
    Q2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    SP, Q = identification(P,Q)
    print(similarity(SP,Q))

    SP, Q2 = identification(P,Q2)
    print(similarity(SP,Q2))